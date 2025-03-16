import mysql.connector
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Connexion MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DATABASE = "scraping_data"

# Liste des marques connues (en majuscule pour la détection)
MARQUES = ["APPLE", "HP", "ASUS", "MSI", "LENOVO", "DELL", "ACER", "SAMSUNG", "HUAWEI", "MICROSOFT", "GIGABYTE"]

# Liste des types spécifiques d'ordinateurs
TYPES_SPECIFIQUES = {
    "PC Gamer": "PC Gamer",
    "PC Hybride": "PC Hybride"
}

def connect_db():
    """ Connexion à MySQL """
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT,
        database=MYSQL_DATABASE
    )
    return conn

def reset_clean_table(cursor, conn):
    """ Supprime et recrée la table nettoyée pour les ordinateurs """
    cursor.execute("DROP TABLE IF EXISTS boulanger_ordinateurs_clean")
    
    query = """
    CREATE TABLE boulanger_ordinateurs_clean (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type_ordinateur VARCHAR(50),
        marque VARCHAR(50),
        modele VARCHAR(255),
        note FLOAT(2),
        avis INT,
        prix FLOAT(2)
    )
    """
    cursor.execute(query)
    conn.commit()
    print("🔄 Table `boulanger_ordinateurs_clean` supprimée et recréée.")

def clean_product_name(product_name):
    """ Sépare le type, la marque et le modèle d'un ordinateur """
    words = product_name.split()  # Découper en mots

    # Déterminer le type spécifique si présent (PC Gamer, PC Hybride)
    type_ordinateur = "Ordinateur portable"  # Type par défaut

    for key, value in TYPES_SPECIFIQUES.items():
        if key in product_name:
            type_ordinateur = value
            break

    # Trouver la marque et le modèle
    marque = "Inconnu"
    modele = " ".join(words)  # Si pas de marque trouvée, tout est modèle

    for i, word in enumerate(words):
        if word.upper() in MARQUES:  # Vérifier si c'est une marque connue
            marque = word.upper() if word.upper() == "HP" else word.capitalize()  # HP en majuscules, autres en capitalized
            modele = " ".join(words[i+1:])  # Tout ce qui suit est le modèle
            break

    # Si la marque détectée est "Apple", modifier le type en "Mac"
    if marque == "Apple":
        type_ordinateur = "Mac"

    return type_ordinateur, marque, modele

def clean_ordinateurs():
    """ Nettoie les données de boulanger_ordinateurs et les insère dans boulanger_ordinateurs_clean """
    conn = connect_db()
    cursor = conn.cursor()

    # Supprimer et recréer la table clean
    reset_clean_table(cursor, conn)
    
    # Récupérer les données brutes
    cursor.execute("SELECT produit, note, avis, prix FROM boulanger_ordinateurs")
    rows = cursor.fetchall()

    cleaned_data = []
    for row in rows:
        produit, note, avis, prix = row

        # Séparer le type, la marque et le modèle
        type_ordinateur, marque, modele = clean_product_name(produit)

        # Nettoyer les notes (arrondir à 2 décimales)
        try:
            note = round(float(note), 2)
        except ValueError:
            note = 0.0  # Si problème, mettre une valeur par défaut
        
        # Nettoyer les avis (convertir en int)
        try:
            avis = int(avis)
        except ValueError:
            avis = 0  # Si problème, mettre 0 avis
        
        # Nettoyer le prix (convertir en float avec 2 décimales)
        try:
            prix = round(float(prix), 2)
        except ValueError:
            prix = None  # Si problème, laisser vide

        cleaned_data.append((type_ordinateur, marque, modele, note, avis, prix))

    # Insérer les données nettoyées
    insert_query = """
    INSERT INTO boulanger_ordinateurs_clean (type_ordinateur, marque, modele, note, avis, prix) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, cleaned_data)
    conn.commit()

    print(f"✅ {len(cleaned_data)} ordinateurs nettoyés et insérés dans `boulanger_ordinateurs_clean`.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    clean_ordinateurs()