import scraping
import database

def main():
    conn, cursor = database.connect_db()
    if not conn or not cursor:
        return

    site = "boulanger"  # 🔥 Tu peux changer cela si tu veux scraper un autre site

    while True:
        print("\n Menu:")
        print("1️⃣ Scraper les ordinateurs portables")
        print("2️⃣ Scraper les électroménagers")
        print("3️⃣ Scraper les consoles de jeux")
        print("4️⃣ Scraper les téléphones")
        print("5️⃣ Scraper les téléviseurs")
        print("6️⃣ Quitter")

        choix = input("Choisissez une option : ")

        categories = {
            "1": "ordinateurs",
            "2": "electromenagers",
            "3": "console",
            "4": "telephone",
            "5": "tele"
        }

        if choix in categories:
            categorie = categories[choix]
            print(f"🔍 Scraping de {categorie} en cours sur {site}...")
            
            data = scraping.scrape_boulanger(categorie, max_pages=3)
            if data is not None:
                print("✅ Scraping terminé.")
                
                produits = data.to_dict(orient="records")  # Convertir DataFrame en liste de dictionnaires
                database.create_table(site, categorie, cursor, conn)  # Création dynamique de la bonne table
                database.insert_into_mysql(produits, cursor, conn, categorie, site)  # Insérer dans la bonne table
        elif choix == "6":
            print("Bye !")
            break
        else:
            print("Option invalide, réessayez.")

    cursor.close()
    conn.close()
    print("🔌 Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()