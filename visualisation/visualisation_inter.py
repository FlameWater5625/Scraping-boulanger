import mysql.connector
import numpy as np
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


# Récupérer les données de toutes les catégories
def fetch_all_data():
    conn = connect_db()

    # Définition des tables et des catégories associées
    tables = {
        "console": "boulanger_console_clean",
        "ordinateur": "boulanger_ordinateurs_clean",
        "telephone": "boulanger_telephone_clean",
        "televiseur": "boulanger_tele_clean"
    }

    # Liste pour stocker les DataFrames
    dataframes = []

    for categorie, table in tables.items():
        query = f"SELECT marque, modele, note, avis, prix FROM {table}"
        df = pd.read_sql(query, conn)
        df["categorie"] = categorie  # Ajouter une colonne pour identifier la catégorie
        dataframes.append(df)

    conn.close()

    # Fusionner tous les DataFrames
    full_df = pd.concat(dataframes, ignore_index=True)

    return full_df


# Charger toutes les données
def visualize_inter():

    df = fetch_all_data()


    # 🔹 1. Comparaison des Prix Moyens par Catégorie

    plt.figure(figsize=(8,5))
    sns.barplot(x="categorie", y="prix", data=df, estimator=np.mean, palette="coolwarm")
    plt.title("Comparaison des prix moyens par catégorie de produit")
    plt.ylabel("Prix moyen (€)")
    plt.xticks(rotation=45)
    plt.show()

    # 🔹 2. Comparaison des Notes Moyennes par Catégorie

    plt.figure(figsize=(8,5))
    sns.barplot(x="categorie", y="note", data=df, estimator=np.mean, palette="viridis")
    plt.title("Notes moyennes par catégorie de produit")
    plt.ylabel("Note moyenne (sur 5)")
    plt.xticks(rotation=45)
    plt.show()

    # 🔹 3 . Corrélation entre prix et note selon la catégorie
    plt.figure(figsize=(8,5))
    sns.scatterplot(x="prix", y="note", hue="categorie", data=df, alpha=0.7, palette="tab10")
    plt.title("Corrélation entre prix et note par catégorie de produit")
    plt.xlabel("Prix (€)")
    plt.ylabel("Note moyenne")
    plt.legend(title="Catégorie")
    plt.show()

    # 🔹 4 . Marques les Plus Présentes par Catégorie
    plt.figure(figsize=(10,6))
    sns.countplot(y="marque", hue="categorie", data=df, palette="pastel", order=df["marque"].value_counts().index)
    plt.title("Répartition des marques par catégorie de produit")
    plt.xlabel("Nombre de produits")
    plt.legend(title="Catégorie")
    plt.show()

    # 🔹 5 .  Boxplot des prix par marque et par catégorie

    plt.figure(figsize=(12, 6))
    sns.boxplot(x="marque", y="prix", hue="categorie", data=df, palette="Set2")
    plt.title("Distribution des prix par marque et par catégorie")
    plt.xlabel("Marque")
    plt.ylabel("Prix (€)")
    plt.xticks(rotation=45)
    plt.legend(title="Catégorie", bbox_to_anchor=(1, 1))
    plt.show()

if __name__ == "__main__":
    visualize_inter()