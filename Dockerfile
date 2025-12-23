# Utiliser l'image Jupyter PySpark comme base
FROM jupyter/pyspark-notebook:latest

# Installer les dépendances Python supplémentaires
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer wget et copier les JARs nécessaires
USER root
RUN apt-get update && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /home/jovyan/.ivy2/jars/ && \
    # Télécharger les JARs pour MongoDB
    wget https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/3.0.1/mongo-spark-connector_2.12-3.0.1.jar -P /home/jovyan/.ivy2/jars/ && \
    wget https://repo1.maven.org/maven2/org/mongodb/mongo-java-driver/3.12.11/mongo-java-driver-3.12.11.jar -P /home/jovyan/.ivy2/jars/ && \
    wget https://repo1.maven.org/maven2/org/mongodb/bson/3.12.11/bson-3.12.11.jar -P /home/jovyan/.ivy2/jars/ && \
    # Télécharger le JAR pour PostgreSQL
    wget https://repo1.maven.org/maven2/org/postgresql/postgresql/42.6.0/postgresql-42.6.0.jar -P /home/jovyan/.ivy2/jars/ && \
    # Donner les permissions de lecture à tous les JARs
    chmod a+r /home/jovyan/.ivy2/jars/*.jar

# Revenir à l'utilisateur jovyan
USER jovyan

# Lancer Jupyter Lab par défaut
CMD ["start-notebook.sh"]