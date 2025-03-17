import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Connexion MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DATABASE = "scraping_data"


# Connexion à la base de données
def connect_db():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT,
        database=MYSQL_DATABASE
    )


def toCSV():
    conn = connect_db()

    # Définition des tables et des catégories associées
    tables = {
        "console": "boulanger_console_clean",
        "ordinateur": "boulanger_ordinateurs_clean",
        "telephone": "boulanger_telephone_clean",
        "televiseur": "boulanger_tele_clean"
    }

    for categorie, table in tables.items():
        query = f"SELECT marque, modele, note, avis, prix FROM {table}"
        df = pd.read_sql(query, conn)
        df.to_csv(f"{categorie}.csv", index=False)
        print("✅ Sauvegard de" + table + "en CSV teminer !")

    conn.close()

if __name__ == "__main__":
    toCSV()