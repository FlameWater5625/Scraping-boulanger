import nettoyage.nettoyage_tele as nettoyage_tele
import nettoyage.nettoyage_console as nettoyage_console
import nettoyage.nettoyage_telephone as nettoyage_telephone
import nettoyage.nettoyage_ordinateur as nettoyage_ordinateur

def menu_nettoyage():
    """ Menu permettant de choisir quel type de données nettoyer """
    while True:
        print("\n📌 Menu Nettoyage :")
        print("1️⃣ Nettoyer les ordinateurs")
        print("2️⃣ Nettoyer les consoles")
        print("3️⃣ Nettoyer les téléphones")
        print("4️⃣ Nettoyer les téléviseurs")
        print("5️⃣ Nettoyer tout")
        print("6️⃣ Retour au menu principal")

        choix = input("👉 Choisissez une option : ")

        if choix == "1":
            print("🔍 Nettoyage des ordinateurs en cours...")
            nettoyage_ordinateur.clean_ordinateurs()
            print("✅ Nettoyage des ordinateurs terminé !")

        elif choix == "2":
            print("🔍 Nettoyage des consoles en cours...")
            nettoyage_console.clean_consoles()
            print("✅ Nettoyage des consoles terminé !")

        elif choix == "3":
            print("🔍 Nettoyage des téléphones en cours...")
            nettoyage_telephone.clean_telephones()
            print("✅ Nettoyage des téléphones terminé !")

        elif choix == "4":
            print("🔍 Nettoyage des téléviseurs en cours...")
            nettoyage_tele.clean_teles()
            print("✅ Nettoyage des téléviseurs terminé !")
            
        elif choix == "5":
            print("🔍 Nettoyage de toutes les catégories en cours...")
            try:
                nettoyage_ordinateur.clean_ordinateurs()
            except: Exception
            try:
                nettoyage_console.clean_consoles()
            except: Exception
            try:
                nettoyage_telephone.clean_telephones()
            except: Exception
            try:
                nettoyage_tele.clean_teles()
            except: Exception       
            print("✅ Tous les nettoyages sont terminés !")

        elif choix == "6":
            print("🔙 Retour au menu principal...")
            break

        else:
            print("❌ Option invalide, réessayez.")
