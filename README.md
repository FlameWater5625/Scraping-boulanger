📂 README.md

# 📊 Scraping & Analyse de Produits Boulanger

🚀 **Scraping, Nettoyage et Visualisation de Produits Boulanger**  
Un projet complet de **scraping de produits**, **stockage en base de données**, **nettoyage des données** et **analyse via visualisation**.

---

## 📌 **Fonctionnalités**
✅ **Scraping Web** 🕷️ → Extraction de produits depuis [Boulanger](https://www.boulanger.com).  
✅ **Base de données MySQL** 🗄️ → Stockage structuré des produits scrappés.  
✅ **Nettoyage des données** 🧹 → Traitement des incohérences et structuration des données.  
✅ **Analyse et Visualisation** 📊 → Graphiques interactifs pour explorer les données.  

---

## 🔧 **Installation & Configuration**
Le projet peut être installé avec **pip** (environnement classique) ou **conda** (environnement virtuel Anaconda).  

### **1️⃣ Cloner le projet**
```bash
git clone https://github.com/ton-repo/scraping_project.git
cd scraping_project

2️⃣ Installer les dépendances

🟢 Si vous utilisez pip

Assurez-vous d’avoir Python 3+ et pip installés.

pip install -r requirements.txt

🔵 Si vous utilisez conda

conda env create -f environment.yml
conda activate scraping_env

3️⃣ Configurer MySQL

Créer un fichier .env dans le dossier config/ avec :

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_PORT=3306
MYSQL_DATABASE=scraping_data

💡 Modifier les valeurs si besoin (ex: port = 8889 pour macOS avec MAMP).

4️⃣ Lancer le projet

python3 main.py

⸻

🚀 Utilisation

📌 1️⃣ Menu Principal

Le projet permet de scraper, nettoyer et visualiser les données en un seul menu.

📌 Menu Principal :
1️⃣ Scraper les ordinateurs portables
2️⃣ Scraper les consoles de jeux
3️⃣ Scraper les téléphones
4️⃣ Scraper les téléviseurs
5️⃣ Passer au nettoyage des données
6️⃣ Visualiser les données
7️⃣ Quitter

📌 2️⃣ Scraping Web

→ Sélectionne une catégorie pour scraper les produits de Boulanger.
→ Les produits sont automatiquement stockés dans MySQL.

💡 Si le scraping a déjà été fait, il supprime et recrée la table pour garantir des données fraîches.

📌 3️⃣ Nettoyage des Données

→ Après le scraping, sélectionne 5️⃣ Nettoyage pour corriger et structurer les données.

📌 4️⃣ Visualisation

→ Une fois les données nettoyées, sélectionne 6️⃣ Visualisation pour afficher les graphiques :
✅ Moyenne des notes et avis par catégorie.
✅ Comparaison des prix entre id=1 et le reste.
✅ Analyse des produits les plus populaires.
✅ Corrélation entre prix et note.

⸻

📊 Exemples de Visualisation

✅ Graphique des Moyennes de Notes par Catégorie
✅ Histogramme des Prix
✅ Scatter Plot (Prix vs Note)
✅ Analyse des Produits id=1 vs Autres Produits

📍 Exemple de résultat :

🔍 Scraping des téléphones en cours...
🗑️ Table `boulanger_telephone` supprimée avec succès.
✅ Scraping terminé.
📥 Données mises à jour dans la base avec succès !

📊 Visualisation :
✅ Produit `id=1` est-il toujours le mieux noté ?
✅ Comparaison des prix
✅ Distribution des avis


