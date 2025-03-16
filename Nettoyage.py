import nettoyage_tele
import nettoyage_console
import nettoyage_telephone
import nettoyage_ordinateur

def menu_nettoyage():
    """ Menu permettant de choisir quel type de données nettoyer """
    while True:
        print("\n📌 Menu Nettoyage :")
        print("1️⃣ Nettoyer les téléviseurs")
        print("2️⃣ Nettoyer les consoles")
        print("3️⃣ Nettoyer les téléphones")
        print("4️⃣ Nettoyer les ordinateurs")
        print("5️⃣ Nettoyer tout")
        print("6️⃣ Retour au menu principal")

        choix = input("👉 Choisissez une option : ")

        if choix == "1":
            print("🔍 Nettoyage des téléviseurs en cours...")
            nettoyage_tele.clean_teles()
            print("✅ Nettoyage des téléviseurs terminé !")

        elif choix == "2":
            print("🔍 Nettoyage des consoles en cours...")
            nettoyage_console.clean_consoles()
            print("✅ Nettoyage des consoles terminé !")

        elif choix == "3":
            print("🔍 Nettoyage des téléphones en cours...")
            nettoyage_telephone.clean_telephones()
            print("✅ Nettoyage des téléphones terminé !")

        elif choix == "4":
            print("🔍 Nettoyage des ordinateurs en cours...")
            nettoyage_ordinateur.clean_ordinateurs()
            print("✅ Nettoyage des ordinateurs terminé !")

        elif choix == "5":
            print("🔍 Nettoyage de toutes les catégories en cours...")
            nettoyage_tele.clean_teles()
            nettoyage_console.clean_consoles()
            nettoyage_telephone.clean_telephones()
            nettoyage_ordinateur.clean_ordinateurs()
            print("✅ Tous les nettoyages sont terminés !")

        elif choix == "6":
            print("🔙 Retour au menu principal...")
            break

        else:
            print("❌ Option invalide, réessayez.")