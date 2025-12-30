# Projet_SQL_NoSQL

## Description
Ce projet vise à **collecter, nettoyer, stocker et analyser** des données ouvertes sur la délinquance et les valeurs foncières en Île-de-France, incluant Paris et sa couronne périurbaine (75, 92, 93, 94, 95).

## Prérequis
- Docker et Docker Compose installés


## Initialisation
1. Cloner ce dépôt.
2. Déposer les fichiers suivant dans data/raw:
  - *donnee-data.gouv-2024-geographie2025-produit-le2025-06-04.csv.gz* : https://static.data.gouv.fr/resources/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/20250710-144817/donnee-data.gouv-2024-geographie2025-produit-le2025-06-04.csv.gz
  - *valeursfoncieres-2023.txt.zip* : https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20251018-234851/valeursfoncieres-2023.txt.zip
  - *valeursfoncieres-2024.txt.zip* : https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20251018-234857/valeursfoncieres-2024.txt.zip
  - 019HexaSmal.csv: https://datanova.laposte.fr/data-fair/api/v1/datasets/laposte-hexasmal/raw pour les code postaux (pour base sql délinquance)
  

3. Créer un fichier `.env` à partir du template (voir `.env.example`).
4. Lancer les conteneurs : `docker-compose up -d`.


## Accès aux services
- Jupyter Lab : [http://localhost:8888](http://localhost:8888) (token dans `.env`)
- PostgreSQL : `localhost:5432` (utilisateur/mot de passe dans `.env`)
- MongoDB : `localhost:27017` (utilisateur/mot de passe dans `.env`)
- Spark UI : [http://localhost:8080](http://localhost:8080)

## Structure des dossiers
- `data/` : Données partagées (brutes et traitées).
- `notebooks/` : Notebooks Jupyter.
- `output/` : Résultats et outputs.
- `scripts/` : Scripts Spark ou autres.

## Sécurité
- Les ports sont exposés uniquement sur `localhost`.
- Les volumes des bases de données sont gérés par Docker.
- Ne pas partager `.env`.

## Données du projet

### Délinquance
- **Source** : [data.gouv.fr - SSMSI](https://www.data.gouv.fr/datasets/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/)
- **Licence** : Licence Ouverte 2.0
- **Fichiers** :
  - `raw/delinquance_2022.csv` : Données brutes téléchargées le [date].
  - `processed/delinquance_clean.csv` : Données nettoyées (script : `scripts/clean_delinquance.py`).

### Valeurs foncières (DVF)
- **Source** : [data.gouv.fr - DGFiP](https://www.data.gouv.fr/datasets/demandes-de-valeurs-foncieres/)
- **Licence** : Licence Ouverte 2.0
- **Fichiers** :
  - `raw/dvf_2022.csv` : Données brutes.