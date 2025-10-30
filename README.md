# Excel to DB (SQLite)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Application CLI moderne et interactive pour convertir des fichiers Excel (.xlsx, .xls) en base de données SQLite avec détection automatique des types de données.

## 🎯 Fonctionnalités

- ✨ **Interface interactive** : Menus et prompts élégants avec Rich et Questionary
- 📊 **Détection automatique** : Scan de toutes les feuilles et détection des types de données
- 🎯 **Sélection flexible** : Choix des feuilles à convertir
- ⚡ **Gestion des conflits** : Options multiples si une table existe déjà
- 📈 **Progression en temps réel** : Barres de progression pour chaque feuille
- 📝 **Logging détaillé** : Fichier de log complet pour chaque conversion
- 🧹 **Nettoyage automatique** : Noms de colonnes et tables nettoyés pour SQLite

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)
- Git (pour récupérer le code)

## 🚀 Installation rapide

### 1. Récupérer le code

```powershell
# Cloner le dépôt
git clone https://github.com/votre-username/excel-to-db.git
cd excel-to-db
```

### 2. Installation des dépendances

**Windows :**

```powershell
# Environnement virtuel (facultatif)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Installation des bibliothèques
pip install -r requirements.txt
```

**Linux/Mac :**

```bash
# Environnement virtuel (facultatif)
python -m venv venv
source venv/bin/activate

# Installation des bibliothèques
pip install -r requirements.txt
```

> **💡 Note** : L'utilisation d'un environnement virtuel est fortement recommandée pour isoler les dépendances du projet.

### 3. Installation de la commande (optionnel)

Pour pouvoir utiliser `excel2db` ou `e2db` directement :

```powershell
pip install -e .
```

Cela crée trois commandes globales :

- `e2db` (commande ultra-courte - **recommandée**)
- `excel2db` (commande courte)
- `excel-to-db` (nom complet)

**Utilisation :**

```powershell
# Au lieu de : python main.py convert
e2db convert --file data/sample_data.xlsx

# Au lieu de : python main.py info data/db/base.db
e2db info data/db/base.db

# Voir l'aide
e2db --help
```

### 4. Créer un fichier Excel de test (optionnel)

```powershell
python create_sample_data.py
```

Cela créera un fichier `data/sample_data.xlsx` avec 3 feuilles :

- Groupes (1 lignes)
- Membres (4 lignes)
- Albums (5 lignes)
- Concerts (1000 lignes)

> **💡 Note** : Les fichiers Excel sont créés dans le même répertoire que le fichier Excel

## 📂 Structure des répertoires

Le projet utilise une structure organisée pour séparer les données :

```
excel-to-db/
├── data/             # Répertoire pour les fichiers de données
│   ├── *.xlsx        # Fichier Excel de test
│   └── *.db          # Bases de données SQLite de test
├── src/              # Code source de l'application
└── main.py           # Point d'entrée
```

**Les fichiers Excel et bases de données seront automatiquement créés/stockés dans ces répertoires.**

## 💻 Utilisation

> **💡 Note** : Assurez-vous que l'environnement virtuel est activé s'il a été créé pour l'installation des bibliothèques.
>
> - Windows : `.\venv\Scripts\Activate.ps1`
> - Linux/Mac : `source venv/bin/activate`

> **⚡ Astuce** : Si vous avez installé avec `pip install -e .`, vous pouvez utiliser `e2db` à la place de `python main.py`

### Commandes disponibles

#### Convertir un fichier Excel

```powershell
# Mode interactif
python main.py convert
# ou : e2db convert

# Avec options
python main.py convert --file data/sample_data.xlsx --database ma_base.db
# ou : e2db convert --file data/sample_data.xlsx --database ma_base.db

# Mode automatique
python main.py convert --file data/sample_data.xlsx --yes
# ou : e2db convert --file data/sample_data.xlsx --yes
```

#### Afficher les informations d'une base

```powershell
python main.py info data/db/ma_base.db
# ou : e2db info data/db/ma_base.db
```

#### Afficher la version

```powershell
python main.py version
# ou : e2db version
```

#### Aide

```powershell
python main.py --help
python main.py convert --help

# ou :
e2db --help
e2db convert --help
```

### Options de la commande convert

- `--file, -f` : Chemin vers le fichier Excel
- `--database, -d` : Nom de la base de données de destination
- `--yes, -y` : Mode automatique (accepter toutes les confirmations)

### Exemples d'utilisation

#### Conversion simple

```powershell
python main.py convert --file data/donnees.xlsx
```

#### Conversion vers une base spécifique

```powershell
python main.py convert --file data/donnees.xlsx --database ma_base.db
```

#### Conversion automatique

```powershell
python main.py convert --file data/donnees.xlsx --database ma_base.db --yes
```

### Mode interactif complet

```powershell
# Avec Python
python main.py convert

# Ou avec la commande installée (recommandé)
e2db convert
```

L'application vous guidera pas à pas à travers 7 écrans clairs :

1. Sélection du fichier Excel
2. Analyse des feuilles
3. Aperçu des données
4. Configuration de la base de données
5. Sélection des feuilles à convertir
6. Conversion avec progression
7. Résumé final

## 🏗️ Architecture du projet

```
excel-to-db/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── excel_reader.py     # Lecture et analyse Excel
│   │   ├── db_manager.py       # Gestion SQLite
│   │   └── type_detector.py    # Détection types pandas → SQLite
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── display.py          # Affichage avec Rich
│   │   └── prompts.py          # Menus interactifs
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # Configuration logging
│       └── name_cleaner.py     # Nettoyage noms
├── main.py                     # Point d'entrée CLI
├── requirements.txt            # Dépendances
└── README.md                   # Documentation
```

## 🔧 Types de données supportés

| Type Pandas      | Type SQLite | Description             |
| ---------------- | ----------- | ----------------------- |
| object           | TEXT        | Texte, chaînes          |
| int64, int32     | INTEGER     | Nombres entiers         |
| float64, float32 | REAL        | Nombres décimaux        |
| datetime64       | TEXT        | Dates (format ISO 8601) |
| bool             | INTEGER     | Booléens (0/1)          |
| timedelta        | TEXT        | Durées                  |

## ⚙️ Options de gestion des conflits

Lorsqu'une table existe déjà dans la base de données :

- **Écraser** : Supprimer la table existante et recréer
- **Ajouter** : Insérer les nouvelles données à la suite
- **Ignorer** : Passer à la feuille suivante
- **Annuler** : Arrêter l'opération

## 📝 Fichier de log

Chaque conversion génère un fichier `excel_to_sqlite.log` contenant :

- Timestamp de chaque opération
- Informations sur les feuilles converties
- Types de données détectés
- Nombre de lignes insérées
- Durée des opérations
- Erreurs éventuelles

## 🔍 Vérifier la base de données créée

### Avec l'outil e2db

```powershell
python main.py info data/db/test.db
# ou : e2db info data/db/test.db
```

### Avec SQLite en ligne de commande

```powershell
# Ouvrir la base de données
sqlite3 data/db/test.db

# Lister les tables
.tables

# Voir le schéma d'une table
.schema clients

# Requête SQL
SELECT * FROM clients LIMIT 10;

# Quitter
.quit
```

### Avec un outil graphique

Utilisez [DB Browser for SQLite](https://sqlitebrowser.org/) pour une interface graphique.

## 🛠️ Résolution de problèmes

### Erreur d'import

Si vous avez une erreur "Module not found", vérifiez que toutes les dépendances sont installées :

```powershell
pip install -r requirements.txt
```

### Fichier Excel non trouvé

Assurez-vous que le chemin vers le fichier Excel est correct. Utilisez des chemins absolus si nécessaire :

```powershell
python main.py convert --file C:\Users\VotreNom\Documents\data.xlsx
```

### Base de données verrouillée

Si la base de données est verrouillée, fermez tous les programmes qui l'utilisent (DB Browser for SQLite, etc.).

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Soumettre des pull requests

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails

## 👤 Auteur

Développé avec ❤️ en suivant les meilleures pratiques Python du moment

## 🆘 Support

Pour toute question ou problème :

- Consultez la documentation
- Vérifiez les logs dans `excel_to_sqlite.log`
- Ouvrez une issue sur le dépôt
