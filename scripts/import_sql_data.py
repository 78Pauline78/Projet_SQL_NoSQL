import os
import gzip
import pandas as pd
from sqlalchemy import create_engine, types, inspect, text
import numpy as np
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv("/app/.env")  # Chemin dans le conteneur data_processing

# Récupérer les variables d'environnement
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = "postgres_dvf"  # Nom du conteneur PostgreSQL dans docker-compose.yml
db_port = os.getenv("DB_PORT", "5432")  # Valeur par défaut si non définie
db_name = os.getenv("POSTGRES_DB")

# Construire l'URL de connexion
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Créer le moteur SQLAlchemy
engine = create_engine(db_url)

# Vérifier si la table existe et contient des données
inspector = inspect(engine)
if inspector.has_table("delinquance_idf"):
    with engine.connect() as conn:
        # Utiliser text() pour convertir la chaîne en objet exécutable
        result = conn.execute(text("SELECT COUNT(*) FROM delinquance_idf"))
        count = result.scalar()
        if count > 0:
            print("✅ Les données existent déjà dans PostgreSQL. Import annulé.")
            exit(0)  # Quitter le script si des données existent

#Chemins des fichiers dans le conteneur
gz_path = "/app/data/raw/donnee-data.gouv-2024-geographie2025-produit-le2025-06-04.csv.gz"
csv_path = "/app/data/raw/donnees_delinquance.csv"
commune_csv_path ="/app/data/raw/019HexaSmal.csv"

#Décompresser le fichier .gz
with gzip.open(gz_path, 'rb') as f_in:
    with open(csv_path, 'wb') as f_out:
        f_out.writelines(f_in)
print(f"Fichier décompressé : {csv_path}")

#Lire le CSV avec les bons paramètres
df = pd.read_csv(
    csv_path,
    sep=';',
    encoding='utf-8',
    quotechar='"',
    doublequote=True,
    escapechar='\\',
    low_memory=False,
    on_bad_lines='warn',
)

#Lire le CSV des communes (ajuste le séparateur si nécessaire)
df_communes = pd.read_csv(
    commune_csv_path,
    sep=';',
    encoding='latin1',  # ou 'iso-8859-1'
    dtype={'#Code_commune_INSEE': str, 'Nom_de_la_commune': str, 'Code_postal': str}
)
print("Colonnes dans df_communes :", df_communes.columns.tolist())

#Afficher les infos sur les colonnes (optionnel, pour débogage)
na_percent = df.isna().mean() * 100
columns_info = pd.DataFrame({
    'Type': df.dtypes,
    'NA (%)': na_percent.round(2)
}).sort_values(by='NA (%)', ascending=False)
print("Infos sur les colonnes :")
print(columns_info)

#Filtrer pour l'Île-de-France
idf_codes = ['75', '92', '93', '94']
idf_data = df[df['CODGEO_2025'].astype(str).str[:2].isin(idf_codes)]
print(f"Nombre de lignes pour la petite couronne : {len(idf_data)}")

#Nettoyer les données
idf_data = idf_data.replace({np.nan: None})
idf_data["nombre"] = pd.to_numeric(idf_data["nombre"], errors="coerce")
idf_data["taux_pour_mille"] = pd.to_numeric(idf_data["taux_pour_mille"], errors="coerce")

#Fusionner avec les informations des communes
idf_data = idf_data.merge(
    df_communes,
    left_on='CODGEO_2025',
    right_on='#Code_commune_INSEE',
    how='left'
)

print(idf_data.head(5))


# Définir les types pour SQLAlchemy
dtype = {
    "CODGEO_2025": types.VARCHAR(10),
    "annee": types.INTEGER,
    "indicateur": types.VARCHAR(100),
    "unite_de_compte": types.VARCHAR(50),
    "nombre": types.NUMERIC(15, 2),
    "taux_pour_mille": types.NUMERIC(10, 2),
    "est_diffuse": types.TEXT,
    "insee_pop": types.INTEGER,
    "insee_pop_millesime": types.INTEGER,
    "insee_log": types.INTEGER,
    "insee_log_millesime": types.INTEGER,
    "complement_info_nombre": types.TEXT,
    "complement_info_taux": types.TEXT
}



# Importer les données par lots
batch_size = 10000
for i in range(0, len(idf_data), batch_size):
    batch = idf_data[i:i + batch_size]
    batch.to_sql(
        "delinquance_idf",
        engine,
        if_exists="append" if i > 0 else "replace",
        index=False,
        dtype=dtype
    )
    print(f"Importé {min(i + batch_size, len(idf_data))}/{len(idf_data)} lignes...")

print("Import SQL terminé avec succès !")
