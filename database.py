import mysql.connector
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Récupération des variables MySQL depuis .env
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DATABASE = "scraping_data"

# Fonction pour créer la base de données si elle n'existe pas
def create_database():
    """ Vérifie et crée la base de données si elle n'existe pas """
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
        print(f"✅ Base de données '{MYSQL_DATABASE}' vérifiée/créée.")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"❌ Erreur lors de la création de la base de données : {err}")

# Connexion à MySQL avec création automatique de la base
def connect_db():
    """ Établit la connexion à la base de données MySQL après vérification """
    create_database()

    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT,
            database=MYSQL_DATABASE
        )
        cursor = conn.cursor()
        print("🔌 Connexion à la base de données établie.")
        return conn, cursor
    except mysql.connector.Error as err:
        print(f"❌ Erreur MySQL : {err}")
        return None, None

# Création dynamique de la table pour chaque site + catégorie
def create_table(site, categorie, cursor, conn):
    """ Crée une table spécifique pour chaque site et catégorie """
    table_name = f"{site}_{categorie}".replace("-", "_")  # Nettoyage du nom de table

    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        produit VARCHAR(255),
        note FLOAT,
        avis INT,
        prix FLOAT
    )
    """
    cursor.execute(query)
    conn.commit()
    print(f"✅ Table '{table_name}' vérifiée/créée avec succès.")

# Vérifier si un produit existe déjà dans la table
def produit_existe(produit, site, categorie, cursor):
    """ Vérifie si un produit est déjà dans la table correspondante """
    table_name = f"{site}_{categorie}".replace("-", "_")
    query = f"SELECT COUNT(*) FROM {table_name} WHERE produit = %s"
    cursor.execute(query, (produit,))
    result = cursor.fetchone()
    return result[0] > 0  # Retourne True si le produit existe déjà

# Insertion des données dans la bonne table
def insert_into_mysql(produits, cursor, conn, categorie, site):
    """ Insère les produits scrappés dans la table du site et de la catégorie """
    table_name = f"{site}_{categorie}".replace("-", "_")  # Ex: boulanger_ordinateurs

    try:
        for produit in produits:
            if not produit_existe(produit["Produit"], site, categorie, cursor):
                sql = f"INSERT INTO {table_name} (produit, note, avis, prix) VALUES (%s, %s, %s, %s)"
                val = (produit["Produit"], produit["Note"], produit["Avis"], produit["Prix"])
                cursor.execute(sql, val)

        conn.commit()
        print(f"✅ Données insérées avec succès dans la table '{table_name}'.")
    except mysql.connector.Error as err:
        print(f"❌ Erreur lors de l'insertion : {err}")