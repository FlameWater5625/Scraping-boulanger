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

# Liste des marques connues (en majuscules pour la détection)
MARQUES = ["SONY", "MICROSOFT", "NINTENDO", "SEGA", "LOGITECH", "RAZER", "STEELSERIES", "XBOX", "PLAYSTATION", "ASUS"]

# Mots-clés pour identifier les marques des jeux
MARQUE_JEUX = {
    "PS5": "Sony",
    "PS4": "Sony",
    "PS3": "Sony",
    "Xbox": "Microsoft",
    "Switch": "Nintendo"
}

# Liste des types spécifiques
TYPES_SPECIFIQUES = {
    "Console Portable": "Console portable",
    "Jeu": "Jeu",
    "Casque": "Accessoire",
    "Manette": "Accessoire",
    "Volant": "Accessoire",
    "Chargeur": "Accessoire",
    "Accessoire": "Accessoire"
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
    """ Supprime et recrée la table nettoyée pour les consoles """
    cursor.execute("DROP TABLE IF EXISTS boulanger_console_clean")
    
    query = """
    CREATE TABLE boulanger_console_clean (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type_console VARCHAR(50),
        marque VARCHAR(50),
        modele VARCHAR(255),
        note FLOAT(2),
        avis INT,
        prix FLOAT(2)
    )
    """
    cursor.execute(query)
    conn.commit()
    print("🔄 Table `boulanger_console_clean` supprimée et recréée.")

def clean_product_name(product_name):
    """ Sépare le type, la marque et le modèle d'une console """
    type_console = "Console"  # Type par défaut

    # Identifier un type spécifique si présent
    for key, value in TYPES_SPECIFIQUES.items():
        if key.lower() in product_name.lower():
            type_console = value
            product_name = product_name.replace(key, "").replace(value, "").strip()
            break

    # Trouver la marque dans le produit, même si elle n'est pas au début
    marque = "Inconnu"
    for brand in MARQUES:
        if brand in product_name.upper():
            marque = brand.capitalize() if brand not in ["XBOX", "PLAYSTATION"] else brand  # Xbox et PlayStation restent en majuscules
            product_name = product_name.replace(brand, "").strip()
            break

    if type_console == "Console":
        product_name = product_name.replace("Console", "").strip()
        
    # Extraire le modèle en supprimant la marque détectée du produit
    modele = product_name.replace(marque, "").strip() if marque != "Inconnu" else product_name

    # Détecter la marque des jeux à partir du modèle
    if type_console == "Jeu":
        for key, value in MARQUE_JEUX.items():
            if key in product_name:
                marque = value
                break


    
    # Nettoyer le modèle : supprimer les espaces inutiles et les sauts de ligne
    modele = modele.replace("\n", " ")  # Remplacer les sauts de ligne par des espaces
    modele = " ".join(modele.split())  # Supprimer les espaces multiples et normaliser

    return type_console, marque, modele

def clean_consoles():
    """ Nettoie les données de boulanger_console et les insère dans boulanger_console_clean """
    conn = connect_db()
    cursor = conn.cursor()

    # Supprimer et recréer la table clean
    reset_clean_table(cursor, conn)
    
    # Récupérer les données brutes
    cursor.execute("SELECT produit, note, avis, prix FROM boulanger_console")
    rows = cursor.fetchall()

    cleaned_data = []
    for row in rows:
        produit, note, avis, prix = row

        # Séparer le type, la marque et le modèle
        type_console, marque, modele = clean_product_name(produit)

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

        cleaned_data.append((type_console, marque, modele, note, avis, prix))

    # Insérer les données nettoyées
    insert_query = """
    INSERT INTO boulanger_console_clean (type_console, marque, modele, note, avis, prix) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, cleaned_data)
    conn.commit()

    print(f"✅ {len(cleaned_data)} consoles nettoyées et insérées dans `boulanger_console_clean`.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    clean_consoles()
