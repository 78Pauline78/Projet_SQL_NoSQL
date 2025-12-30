import os
import zipfile
import pandas as pd
import gc
from pymongo import MongoClient
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv("/app/.env")

# Connexion à MongoDB
db_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
db_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
mongo_host = "mongodb_delinquance"
mongo_port = 27017

client = MongoClient(
    host=mongo_host,
    port=mongo_port,
    username=db_user,
    password=db_password,
    authSource='admin'
)

db = client[os.getenv("MONGO_DB", "valeursfoncieres")]
collection = db['idf_2023_2024']

# Vérifier si la collection contient déjà des données
if collection.count_documents({}) > 0:
    print("✅ Les données existent déjà dans MongoDB. Import annulé.")
    exit(0)

# Dictionnaire des années et fichiers locaux
urls = {
    2023: "/app/data/raw/valeursfoncieres-2023.txt.zip",
    2024: "/app/data/raw/valeursfoncieres-2024.txt.zip"
}

# Codes des départements d'Île-de-France
idf_codes = ['75', '92', '93', '94']
total_lines = 0

for year, zip_path in urls.items():
    print(f"\nTraitement de l'année {year}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("/app/data/raw/")

    file_path = f"/app/data/raw/ValeursFoncieres-{year}.txt"
    for chunk in pd.read_csv(
        file_path,
        sep='|',
        encoding='latin1',
        low_memory=True,
        chunksize=5000
    ):
        dept_col = [col for col in chunk.columns if 'departement' in col.lower()][0]
        idf_data = chunk[chunk[dept_col].astype(str).isin(idf_codes)]
        idf_data['annee'] = year
        data = idf_data.to_dict('records')
        if data:
            collection.insert_many(data)
            total_lines += len(idf_data)
            print(f"Lignes insérées pour {year} : {len(idf_data)}")

        del chunk
        gc.collect()

    os.remove(file_path)  # Supprimer le fichier extrait
    print(f"Fichier source pour {year} supprimé.")

print(f"\nInsertion terminée : {total_lines} documents insérés.")
