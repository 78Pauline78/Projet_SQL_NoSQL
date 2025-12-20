import os
import zipfile
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv("/app/.env")

# Connexion à MongoDB
db_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
db_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
mongo_host = "mongodb_delinquance"  # Nom du conteneur MongoDB dans docker-compose.yml
mongo_port = 27017

client = MongoClient(
    host=mongo_host,
    port=mongo_port,
    username=db_user,
    password=db_password,
    authSource='admin'
)

# Accéder à la base et à la collection (créée automatiquement si inexistante)
db = client[os.getenv("MONGO_DB", "valeursfoncieres")]
collection = db['idf_2023_2024']  # Nom mis à jour pour correspondre à ton projet

# Vérifier si la collection contient déjà des données
if collection.count_documents({}) > 0:
    print("✅ Les données existent déjà dans MongoDB. Import annulé.")
    exit(0)  # Quitter le script si des données existent

# Dictionnaire des années et fichiers locaux (pas d'URLs car les fichiers sont déjà téléchargés)
urls = {
    2023: "/app/data/raw/valeursfoncieres-2023.txt.zip",
    2024: "/app/data/raw/valeursfoncieres-2024.txt.zip"
}

# Codes des départements d'Île-de-France
idf_codes = ['75', '92', '93', '94']

# Initialiser une liste pour stocker les DataFrames filtrés
dfs = []
total_lines = 0

# Boucle sur chaque année
for year, zip_path in urls.items():
    print(f"\nTraitement de l'année {year}...")

    # Chemin du fichier extrait
    file_path = f"/app/data/raw/ValeursFoncieres-{year}.txt"

    # Extraire le fichier ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("/app/data/raw/")

    # Lire le fichier DVF
    df = pd.read_csv(
        file_path,
        sep='|',
        encoding='latin1',
        low_memory=False,
    )

    # Trouver la colonne "département"
    dept_col = [col for col in df.columns if 'departement' in col.lower()]
    if not dept_col:
        raise ValueError(f"Colonne 'département' introuvable dans le fichier {year}.")
    dept_col = dept_col[0]

    # Filtrer les données pour l'Île-de-France
    idf_data = df[df[dept_col].astype(str).isin(idf_codes)]
    idf_data['annee'] = year  # Ajouter une colonne pour l'année
    dfs.append(idf_data)
    total_lines += len(idf_data)
    print(f"Lignes pour {year} : {len(idf_data)}")

    # Supprimer le fichier extrait (garder le ZIP pour référence)
    try:
        os.remove(file_path)
        print(f"Fichier source pour {year} supprimé : {file_path}")
    except OSError as e:
        print(f"Erreur lors de la suppression du fichier pour {year} : {e}")

# Concaténer tous les DataFrames
final_df = pd.concat(dfs, ignore_index=True)
print(f"\nNombre total de lignes pour l'Île-de-France : {total_lines}")

# Nettoyer les colonnes avec 100% de NaN
df_clean = final_df.dropna(axis=1, how='all')

# Afficher les infos sur les colonnes (optionnel)
na_percent = df_clean.isna().mean() * 100
columns_info = pd.DataFrame({
    'Type': df_clean.dtypes,
    'NA (%)': na_percent.round(2)
}).sort_values(by='NA (%)', ascending=False)
print("\nInfos sur les colonnes :")
print(columns_info)



# Créer la collection avec validation de schéma (optionnel)
if 'idf_2023_2024' not in db.list_collection_names():
    db.create_collection('idf_2023_2024')
    print("Collection 'idf_2023_2024' créée.")

# Insérer les données
data = df_clean.to_dict('records')
result = collection.insert_many(data)
print(f"\nInsertion terminée : {len(data)} documents insérés (ID: {result.inserted_ids[0]}).")
