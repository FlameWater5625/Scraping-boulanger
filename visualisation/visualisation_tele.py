import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# Récupérer les données
def fetch_data():
    conn = connect_db()
    query = "SELECT type_ecran, marque, modele, note, avis, prix FROM boulanger_tele_clean"
    df = pd.read_sql_query(query, conn)  # Lire les données SQL dans un DataFrame Pandas
    conn.close()
    return df

# Fonction principale pour visualiser les données
def visualize_tele():
    df = fetch_data()

    # 🔹 1. Histogramme des notes moyennes par marque
    plt.figure(figsize=(10, 5))
    sns.barplot(x=df.groupby("marque")["note"].mean().index,
                y=df.groupby("marque")["note"].mean().values,
                palette="viridis")
    plt.title("Note moyenne par marque")
    plt.xlabel("Marque")
    plt.ylabel("Note moyenne")
    plt.xticks(rotation=45)
    plt.show()

    # 🔹 2. Diagramme circulaire de la répartition des marques
    plt.figure(figsize=(8, 8))
    df["marque"].value_counts().plot.pie(autopct="%1.1f%%", cmap="coolwarm", startangle=90, shadow=True)
    plt.title("Répartition des marques")
    plt.ylabel("")  # Supprimer l'étiquette inutile
    plt.show()

    # 🔹 3. Nuage de points Prix vs Avis
    plt.figure(figsize=(10, 5))
    sns.scatterplot(x=df["prix"], y=df["avis"], hue=df["marque"], palette="Set2", alpha=0.7)
    plt.title("Relation entre le prix et le nombre d'avis")
    plt.xlabel("Prix (€)")
    plt.ylabel("Nombre d'avis")
    plt.legend(title="Marque")
    plt.show()

    # 🔹 4. Histogramme des types d'écrans
    plt.figure(figsize=(8, 5))
    sns.countplot(y=df["type_ecran"], palette="pastel", order=df["type_ecran"].value_counts().index)
    plt.title("Répartition des types d'écrans")
    plt.xlabel("Nombre de téléviseurs")
    plt.ylabel("Type d'écran")
    plt.show()

    # 🔹 5. Bar chart des téléviseurs les mieux notés
    top_tvs = df.nlargest(10, "note")
    plt.figure(figsize=(12, 6))
    sns.barplot(y=top_tvs["modele"], x=top_tvs["note"],
                hue=top_tvs["marque"], dodge=False, palette="tab10")
    plt.title("Top 10 des téléviseurs les mieux notés")
    plt.xlabel("Note")
    plt.ylabel("Modèle")
    plt.xlim(0, 5)  # Note max = 5
    plt.legend(title="Marque")
    plt.show()

# Exécuter la visualisation
if __name__ == "__main__":
    visualize_tele()
