import visualisation.visualisation_console as visualisation_console
import visualisation.visualisation_ordi as visualisation_ordi
import visualisation.visualisation_tele as visualisation_tele
import visualisation.visualisation_telephone as visualisation_telephone
import visualisation.visualisation_inter as visualisation_inter

import os


def menu_visu():
    """ Menu permettant de choisir quel type de données Visualiser """
    while True:
        print("\n📌 Menu Visualisation :")
        print("1️⃣ Visualiser les ordinateurs")
        print("2️⃣ Visualiser les consoles")
        print("3️⃣ Visualiser les téléphones")
        print("4️⃣ Visualiser les téléviseurs")
        print("5️⃣ Visualiser inter-produits")
        print("6️⃣ Retour au menu principal")

        choix = input("👉 Choisissez une option : ")

        if choix == "1":
            print("🔍 Visualisation des ordinateurs en cours...")
            visualisation_ordi.visualize_ordi()
            print("✅ Visualisation des ordinateurs les terminé !")

        if choix == "2":
           print("🔍 Visualisation des consoles en cours...")
           visualisation_console.visualize_console()
           print("✅ Visualisation des consoles terminé !")

        elif choix == "3":
            print("🔍  Visualisation des téléphones en cours...")
            visualisation_telephone.visualize_telephone()
            print("✅ Visualisation des téléphones terminé !")

        elif choix == "4":
            print("🔍 Visualisation des téléviseurs en cours...")
            visualisation_tele.visualize_tele()
            print("✅ Visualisation des téléviseurs terminé !")

        elif choix == "5":
            print("🔍 Visualisation inter-produits en cours...")
            visualisation_inter.visualize_inter()
            print("✅ Visualisation inter-produits terminé !")


        elif choix == "6":
           print("🔙 Retour au menu principal...")
           break

        else:
           print("❌ Option invalide, réessayez.")
