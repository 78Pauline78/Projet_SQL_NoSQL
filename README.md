# Projet_SQL_NoSQL

## Description


## Prérequis
- Docker et Docker Compose installés


## Initialisation
1. Cloner ce dépôt.
2. Créer un fichier `.env` à partir du template (voir `.env.example`).
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