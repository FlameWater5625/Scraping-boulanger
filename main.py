import requests
from bs4 import BeautifulSoup
import pandas as pd

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

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    print(f"\n🌍 Tentative de connexion à {url}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("✅ Connexion reussie à Boulanger !")
    else:
        print(f"❌ Erreur de connexion (Code {response.status_code})")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extraire les produits
    produits = []
    articles = soup.find_all("article", class_="grid product-list__product")  # Trouver tous les produits

    if not articles:
        print("⚠️ Aucun produit trouve. Verifie ton html")
        return

    for article in articles:
        #Recup noms
        name_tag = article.find("h2", class_="product-list__product-label")
        name = name_tag.get_text(strip=True) if name_tag else "Nom non disponible"

        #Recup notes, Il faudra utiliser selenium car les notes sont en javascript
        # je n utilise pas chrome et je n ai pas les drivers pour le faire
        rating = "Note non disponible"
        rating_tag = article.find("a", class_="rating ")
        if rating_tag and "aria-label" in rating_tag.attrs:
            rating_text = rating_tag["aria-label"]
            rating_split = rating_text.split(" ")
            if len(rating_split) > 6:
                rating = rating_split[6]  # Je pensais que c etait hard coded en html ....
                                          # Ce splitting ne sert actuelleemnt a rien, mais
                                          #sera utile lorsque selenium sera implementer
                

        #Recup avis en totals
        reviews_tag = article.find("span", class_="rating__count")
        reviews = reviews_tag.get_text(strip=True) if reviews_tag else "Avis non disponible"

        # Ajoute info liste
        produits.append({
            "Produit": name,
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

