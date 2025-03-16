import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import random
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Déterminer quel navigateur utiliser
BROWSER = os.getenv("BROWSER", "Safari")

# URLs des catégories
URLS = {
    "ordinateurs": "https://www.boulanger.com/c/tous-les-ordinateurs-portables",
    "electromenagers": "https://www.boulanger.com/opeco/me0325micb",
    "console": "https://www.boulanger.com/c/console-de-jeux",
    "telephone": "https://www.boulanger.com/c/smartphone-telephone-portable",
    "tele": "https://www.boulanger.com/c/televiseur"
}

def get_driver():
    """ Initialise le bon navigateur selon la configuration dans .env """
    if BROWSER == "Chrome":
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
    elif BROWSER == "Safari":
        driver = webdriver.Safari()
    else:
        raise ValueError("Navigateur non supporté, utilise 'Chrome' ou 'Safari' dans .env")
    
    return driver

def scrape_boulanger(category, max_pages=3):
    """ Scrape les produits d'une catégorie sur Boulanger avec le navigateur défini """
    url = URLS.get(category)
    if not url:
        print("❌ Catégorie invalide.")
        return None

    driver = get_driver()
    produits = []

    for page in range(1, max_pages + 1):
        full_url = f"{url}?page={page}"
        print(f"\n🌍 Connexion à {full_url}...")
        driver.get(full_url)
        time.sleep(random.uniform(3, 6))  # Pause aléatoire pour éviter les blocages

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        articles = soup.find_all("article", class_="grid product-list__product")

        if not articles:
            print(f"⚠️ Fin des pages trouvées à la page {page}.")
            break

        for article in articles:
            # Récupération du nom du produit
            name_tag = article.find("h2", class_="product-list__product-label")
            name = name_tag.get_text(strip=True) if name_tag else "Nom non disponible"

            # Récupération de la note
            rating = "0"
            rating_section = article.find("div", class_="rating__stars")
            if rating_section:
                bl_rating_elem = rating_section.find("bl-rating")
                if bl_rating_elem:
                    rating = bl_rating_elem.get("rating")
                    try:
                        rating = float(rating)
                    except ValueError:
                        rating = 0.0

            # Récupération du nombre d'avis
            reviews_tag = article.find("span", class_="rating__count")
            reviews = reviews_tag.get_text(strip=True) if reviews_tag else "0"
            reviews = reviews.replace("(", "").replace(")", "").strip()
            reviews = int(reviews) if reviews.isdigit() else 0  # Convertir en entier

            # Récupération du prix
            price_tag = article.find("div", class_="price")
            price = price_tag.get_text(strip=True) if price_tag else "Prix non disponible"
            price = price.replace("€", "").replace(",", ".").strip()
            try:
                price = float(price)  # Conversion en float
            except ValueError:
                price = None  # Si le prix est invalide

            # Ajout des données à la liste
            produits.append({
                "Produit": name,
                "Note": rating,
                "Avis": reviews,
                "Prix": price
            })

    driver.quit()
    df = pd.DataFrame(produits)
    print("\n📋 Produits trouvés :\n", df)

    return df