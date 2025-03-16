import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# URLS
URLS = {
    "ordinateurs": "https://www.boulanger.com/c/tous-les-ordinateurs-portables",
    "electromenagers": "https://www.boulanger.com/opeco/me0325micb"
}

# Fonction de scraping main
def scrape_boulanger(category):
    url = URLS.get(category)
    if not url:
        print("❌ Categorie invalide.")
        return

    # Path to your ChromeDriver
    driver = webdriver.Chrome()

    print(f"\n🌍 Tentative de connexion à {url}...")
    driver.get(url)
    time.sleep(4)  # Wait for the page to load completely

    # Get the page source after JavaScript has rendered
    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, "html.parser")

    # Extraire les produits
    produits = []
    articles = soup.find_all("article", class_="grid product-list__product")  # Trouver tous les produits

    if not articles:
        print("⚠️ Aucun produit trouve. Verifie ton html")
        return

    for article in articles:
        # Recup noms
        name_tag = article.find("h2", class_="product-list__product-label")
        name = name_tag.get_text(strip=True) if name_tag else "Nom non disponible"
        name_cleaned = name.replace('\n', ' ').replace('\t', '')  # Clean up the name

        # Recup notes
        rating = "Note non disponible"
        rating_section = article.find("div", class_="rating__stars")
        if rating_section:            
            bl_rating_elem = rating_section.find("bl-rating")
            if bl_rating_elem:
                # Extract the rating value
                rating = bl_rating_elem.get("rating")
                rating = str(round(float(rating), 1))

        # Recup avis en totals
        reviews_tag = article.find("span", class_="rating__count")
        reviews = reviews_tag.get_text(strip=True) if reviews_tag else "Avis non disponible"

        # Ajoute info liste
        produits.append({
            "Produit": name_cleaned,
            "Note": rating,
            "Avis": reviews
        })

    # affichage en tabl
    df = pd.DataFrame(produits)
    print("\n📋 Produits trouves :\n")
    print(df)

    return df

# Main
def menu():
    while True:
        print("\n📌 Menu:")
        print("1️⃣ Scraper les ordinateurs portables")
        print("2️⃣ Scraper les electromenagers")
        print("3️⃣ Quitter")

        choix = input("👉 Choisissez une option : ")

        if choix == "1":
            print("🔍 Scraping des ordinateurs en cours...")
            scrape_boulanger("ordinateurs")

        elif choix == "2":
            print("🔍 Scraping des electromenagers en cours...")
            scrape_boulanger("electromenagers")

        elif choix == "3":
            print("👋 Bye !")
            break

        else:
            print("❌ Option invalide, reessayez.")

# Lancer le programme
if __name__ == "__main__":
    menu()
