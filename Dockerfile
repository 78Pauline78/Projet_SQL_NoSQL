# Utiliser l'image Jupyter PySpark comme base
FROM jupyter/pyspark-notebook:latest

# Installer les dépendances Python supplémentaires
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Lancer Jupyter Lab par défaut
CMD ["start-notebook.sh"]

