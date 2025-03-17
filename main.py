import scraping.scraping as scraping
import database.database as database
import nettoyage.nettoyage as nettoyage
import visualisation.visualisation as visualisation
import toCSV.toCSV as toCSV

def main():
    """ Menu principal : Scraping, Insertion en BDD et Nettoyage """
    conn, cursor = database.connect_db()
    if not conn or not cursor:
        return

    site = "boulanger" 
    
    while True:
        print("\n📌 Menu Principal :")
        print("1️⃣ Scraper les ordinateurs portables")
        print("2️⃣ Scraper les consoles de jeux")
        print("3️⃣ Scraper les téléphones")
        print("4️⃣ Scraper les téléviseurs")
        print("5️⃣ Passer au nettoyage des données")
        print("6️⃣ Passer a la visualisation des données")
        print("7️⃣ Sauvegarder en CSV")
        print("8️⃣ Quitter")

        choix = input("👉 Choisissez une option : ")

        categories = {
            "1": "ordinateurs",
            "2": "console",
            "3": "telephone",
            "4": "tele"
        }

        if choix in categories:
            categorie = categories[choix]
            print(f"\n🔍 Scraping de {categorie} en cours sur {site}...")

            # Supprimer la table si elle existe déjà pour éviter les doublons
            database.drop_table_if_exists(site, categorie, cursor, conn)

            # Scraping des nouvelles données
            max_pages=1
            data = scraping.scrape_boulanger(categorie, max_pages)
            if data is not None:
                print("✅ Scraping terminé.")

                produits = data.to_dict(orient="records")  # Convertir DataFrame en liste de dictionnaires
                database.create_table(site, categorie, cursor, conn)  # Création dynamique de la table
                database.insert_into_mysql(produits, cursor, conn, categorie, site)  # Insertion des données

                print("📥 Données mises à jour dans la base avec succès !")

        elif choix == "5":
            print("\n🔽 Passage au nettoyage des données...")
            nettoyage.menu_nettoyage()  # 🔥 Ajout du menu de nettoyage

        elif choix == "6":
            print("\n🔽 Passage a la visualisation des données...")
            visualisation.menu_visu()  # 🔥 Ajout du menu de visualisation
        
        elif choix == "7":
            print("\n🔽 Passage en CSV...")
            toCSV.toCSV()  # 🔥 Ajout du menu de visualisation

        elif choix == "8":
            print("👋 Bye !")
            break

        else:
            print("❌ Option invalide, réessayez.")

    cursor.close()
    conn.close()
    print("🔌 Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
