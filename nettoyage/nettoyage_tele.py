import mysql.connector
import os
import re
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Connexion MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DATABASE = "scraping_data"

# Types d’écrans
TYPES_ECRANS = ["OLED", "QLED", "LED", "MiniLED"]

# Marques connues
MARQUES = ["SAMSUNG", "SONY", "LG", "TCL", "HISENSE", "PHILIPS", "PANASONIC", "THOMSON", "XIAOMI", "SHARP", "SMART TECH"]

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
    """ Supprime et recrée la table nettoyée pour les téléviseurs """
    cursor.execute("DROP TABLE IF EXISTS boulanger_tele_clean")
    
    query = """
    CREATE TABLE boulanger_tele_clean (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type_ecran VARCHAR(50),
        marque VARCHAR(50),
        modele VARCHAR(255),
        note FLOAT(2),
        avis INT,
        prix FLOAT(2)
    )
    """
    cursor.execute(query)
    conn.commit()
    print("🔄 Table `boulanger_tele_clean` supprimée et recréée.")

def clean_product_name(product_name):
    """ Sépare le type d’écran, la marque et le modèle d'un téléviseur """

    # Détecter le type d'écran
    type_ecran = "LED"  # Par défaut
    for screen_type in TYPES_ECRANS:
        if screen_type in product_name.upper():
            type_ecran = screen_type.upper()
            break

    # Détection de MiniLED
    if "MINILED" in product_name.upper():
        type_ecran = "MiniLED"

    # Trouver la marque en cherchant un mot connu parmi les marques
    marque = "Inconnu"
    for brand in MARQUES:
        if brand in product_name.upper():
            marque = brand.upper()
            break

    # Extraction du modèle
    modele = product_name

    # Supprimer la marque et le type d'écran du modèle
    elements_a_supprimer = [marque, type_ecran, "TV"]
    for elem in elements_a_supprimer:
        if elem and elem in modele:
            modele = modele.replace(elem, "").strip()

    # Vérifier si le modèle contient encore des mots parasites comme "OLED", "QLED"
    modele = re.sub(r"\b(OLED|QLED|LED|MiniLED)\b", "", modele, flags=re.IGNORECASE).strip()

    return type_ecran, marque, modele

def clean_teles():
    """ Nettoie les données de `boulanger_tele` et les insère dans `boulanger_tele_clean` """
    conn = connect_db()
    cursor = conn.cursor()

    # Supprimer et recréer la table clean
    reset_clean_table(cursor, conn)
    
    # Récupérer les données brutes
    cursor.execute("SELECT produit, note, avis, prix FROM boulanger_tele")
    rows = cursor.fetchall()

    cleaned_data = []
    for row in rows:
        produit, note, avis, prix = row

        # Séparer le type d’écran, la marque et le modèle
        type_ecran, marque, modele = clean_product_name(produit)

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

        cleaned_data.append((type_ecran, marque, modele, note, avis, prix))

    # Insérer les données nettoyées
    insert_query = """
    INSERT INTO boulanger_tele_clean (type_ecran, marque, modele, note, avis, prix) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, cleaned_data)
    conn.commit()

    print(f"✅ {len(cleaned_data)} téléviseurs nettoyés et insérés dans `boulanger_tele_clean`.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    clean_teles()