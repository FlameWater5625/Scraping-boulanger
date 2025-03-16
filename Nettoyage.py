import pandas as pd

# Chargement du fichier
df = pd.read_csv("ordinateurs_boulanger.csv")

# Affichage des informations initiales
print("---------------------------------------- \n")
print(df.info())

# Suppression des valeurs manquantes
print("---------------------------------------- \n")
print("Nombres de valeurs manquantes sur le dataframe \n")
print(df.isnull().sum())

df = df.dropna()

# Suppression des doublons
print("---------------------------------------- \n")
print(df.duplicated().sum())
df = df.drop_duplicates()

# Traitement des avis
print("---------------------------------------- \n")
print("Remplissage des valeurs manquantes sur le dataframe \n")
df["Avis"] = df["Avis"].fillna("Ordinateur performant")
df["Avis"] = df["Avis"].replace("Avis non disponible", "Ordinateur performant")


# Traitement des notes
df["Note"] = pd.to_numeric(df["Note"], errors='coerce')
df["Note"] = df["Note"].fillna(df["Note"].mean())
df["Note"] = df["Note"].round(2)

# Vérification des doublons après nettoyage
print("---------------------------------------- \n")
print("Recherche des doublons")
print(df[df.duplicated()])
print(df.duplicated().sum())

# Affichage des informations après nettoyage
print("---------------------------------------- \n")
print("\n Données après nettoyage :\n")
print(df.info())

# Sauvegarde du fichier nettoyé
df.to_csv("ordinateurs-boulanger_cleaned.csv", index=False)
