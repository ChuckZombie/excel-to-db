# Excel to DB (SQLite)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Application CLI moderne et interactive pour convertir des fichiers Excel (.xlsx, .xls) en base de données SQLite **et inversement** avec détection automatique des types de données.

## 🎯 Fonctionnalités

### Conversion Excel → SQLite (commande `convert`)

- ✨ **Interface interactive** : Menus et prompts élégants avec Rich et Questionary
- 📊 **Détection automatique** : Scan de toutes les feuilles et détection des types de données
- 🎯 **Sélection flexible** : Choix des feuilles à convertir
- ⚡ **Gestion des conflits** : Options multiples si une table existe déjà
- 🧹 **Nettoyage automatique** : Noms de colonnes et tables nettoyés pour SQLite

### Conversion SQLite → Excel (commande `reverse`)

- 🔄 **Export complet** : Convertit une base SQLite en fichier Excel
- 📑 **Une feuille par table** : Chaque table devient une feuille Excel
- 🎨 **Mise en forme automatique** : En-têtes stylés (gras, fond coloré)
- 📏 **Colonnes auto-ajustées** : Largeur optimale pour chaque colonne
- 🎯 **Sélection des tables** : Choix des tables à exporter

### Fonctionnalités communes

- 📈 **Progression en temps réel** : Barres de progression pour chaque opération
- 📝 **Logging détaillé** : Fichier de log complet pour chaque conversion
- 🚀 **Mode batch** : Option `--yes` pour automatiser les confirmations

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

Cela créera un fichier `data/sample_data.xlsx` avec 4 feuilles :

- Groupes (1 lignes)
- Membres (4 lignes)
- Albums (5 lignes)
- Concerts (1000 lignes)

> **💡 Note** : Les fichiers Excel sont créés dans le répertoire `data`

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

#### 📊 Convertir Excel → SQLite (convert)

```powershell
# Mode interactif
python main.py convert
# ou : e2db convert

# Avec options
python main.py convert --file data/sample_data.xlsx --database ma_base.db
# ou : e2db convert --file data/sample_data.xlsx --database ma_base.db

# Mode automatique (accepte toutes les confirmations)
python main.py convert --file data/sample_data.xlsx --yes
# ou : e2db convert --file data/sample_data.xlsx --yes
```

#### 🔄 Convertir SQLite → Excel (reverse)

```powershell
# Mode interactif
python main.py reverse
# ou : e2db reverse

# Avec options
python main.py reverse --database data/ma_base.db --output export.xlsx
# ou : e2db reverse --database data/ma_base.db --output export.xlsx

# Mode automatique (exporte toutes les tables)
python main.py reverse --database data/ma_base.db --output export.xlsx --yes
# ou : e2db reverse --database data/ma_base.db --output export.xlsx --yes
```

#### ℹ️ Afficher les informations d'une base

```powershell
python main.py info data/db/ma_base.db
# ou : e2db info data/db/ma_base.db
```

#### 📌 Afficher la version

```powershell
python main.py version
# ou : e2db version
```

#### ❓ Aide

```powershell
# Aide générale
python main.py --help

# Aide pour une commande spécifique
python main.py convert --help
python main.py reverse --help

# ou avec e2db :
e2db --help
e2db convert --help
e2db reverse --help
```

### Options des commandes

#### Commande `convert` (Excel → SQLite)

- `--file, -f` : Chemin vers le fichier Excel
- `--database, -d` : Nom de la base de données de destination
- `--yes, -y` : Mode automatique (accepter toutes les confirmations)

#### Commande `reverse` (SQLite → Excel)

- `--database, -d` : Chemin vers la base de données SQLite
- `--output, -o` : Nom du fichier Excel de sortie
- `--yes, -y` : Mode automatique (exporter toutes les tables sans confirmation)

### Exemples d'utilisation

#### Conversion Excel → SQLite

```powershell
# Conversion simple
python main.py convert --file data/donnees.xlsx

# Conversion vers une base spécifique
python main.py convert --file data/donnees.xlsx --database ma_base.db

# Conversion automatique
python main.py convert --file data/donnees.xlsx --database ma_base.db --yes
```

#### Conversion SQLite → Excel

```powershell
# Export simple
python main.py reverse --database data/ma_base.db

# Export vers un fichier spécifique
python main.py reverse --database data/ma_base.db --output backup.xlsx

# Export automatique de toutes les tables
python main.py reverse --database data/ma_base.db --output backup.xlsx --yes
```

#### Workflow complet (Aller-Retour)

```powershell
# 1. Convertir Excel → SQLite
python main.py convert --file data/source.xlsx --database data/travail.db

# 2. Travailler avec la base SQLite (requêtes, modifications, etc.)
sqlite3 data/travail.db

# 3. Exporter le résultat vers Excel
python main.py reverse --database data/travail.db --output data/resultat.xlsx
```

### Mode interactif

#### Mode interactif pour `convert` (Excel → SQLite)

```powershell
python main.py convert
# ou : e2db convert
```

L'application vous guidera pas à pas :

1. 📁 Sélection du fichier Excel (avec auto-complétion)
2. 🔍 Analyse des feuilles
3. 💾 Configuration de la base de données
4. 📋 Sélection des feuilles à convertir
5. ⚙️ Gestion des conflits (si tables existantes)
6. ⏳ Conversion avec barres de progression
7. ✅ Résumé final avec statistiques

#### Mode interactif pour `reverse` (SQLite → Excel)

```powershell
python main.py reverse
# ou : e2db reverse
```

L'application vous guidera :

1. 📁 Sélection de la base de données (avec auto-complétion)
2. 🔍 Analyse des tables
3. 📋 Sélection des tables à exporter
4. 📊 Configuration du fichier Excel de sortie
5. ⏳ Export avec barres de progression
6. ✅ Résumé final avec statistiques

## 🏗️ Architecture du projet

```
excel-to-db/
├── data/                       # Répertoire pour fichiers de test
│   ├── sample_data.xlsx
│   └── sample_data.db
├── src/
│   ├── __init__.py
│   ├── core/                   # 📦 Module métier (logique de conversion)
│   │   ├── __init__.py
│   │   ├── excel_reader.py     # Lecture fichiers Excel
│   │   ├── database_reader.py  # Lecture bases SQLite
│   │   ├── excel_writer.py     # Écriture fichiers Excel
│   │   ├── type_detector.py    # Détection automatique des types
│   │   └── db_manager.py       # Gestion bases de données SQLite
│   ├── ui/                     # 🎨 Interface utilisateur
│   │   ├── __init__.py
│   │   ├── display.py          # Affichage commun (Rich)
│   │   ├── convert/            # UI pour Excel → SQLite
│   │   │   ├── __init__.py
│   │   │   ├── display.py      # Affichage spécifique
│   │   │   └── prompts.py      # Prompts interactifs
│   │   └── reverse/            # UI pour SQLite → Excel
│   │       ├── __init__.py
│   │       ├── display.py      # Affichage spécifique
│   │       └── prompts.py      # Prompts interactifs
│   └── utils/                  # 🛠️ Utilitaires
│       ├── __init__.py
│       ├── logger.py           # Configuration logging
│       └── name_cleaner.py     # Nettoyage noms SQLite
├── main.py                     # 🚀 Point d'entrée CLI
├── requirements.txt            # 📋 Dépendances Python
├── setup.py                    # ⚙️ Configuration installation
└── README.md                   # 📖 Documentation
```

### 🎨 Architecture modulaire

Le projet suit une architecture claire avec séparation des responsabilités :

- **`core/`** : Logique métier centralisée
  - `excel_reader.py` : Lecture et analyse des fichiers Excel
  - `database_reader.py` : Lecture des bases SQLite
  - `excel_writer.py` : Création de fichiers Excel
  - `type_detector.py` : Détection automatique des types de données
  - `db_manager.py` : Gestion des bases de données SQLite
- **`ui/convert/`** : Interface utilisateur pour Excel → SQLite
- **`ui/reverse/`** : Interface utilisateur pour SQLite → Excel
- **`ui/display.py`** : Fonctions d'affichage communes (Rich)
- **`utils/`** : Utilitaires réutilisables (logger, nettoyage)

## 🔧 Types de données supportés

### Conversion Excel → SQLite

| Type Pandas      | Type SQLite | Description             |
| ---------------- | ----------- | ----------------------- |
| object           | TEXT        | Texte, chaînes          |
| int64, int32     | INTEGER     | Nombres entiers         |
| float64, float32 | REAL        | Nombres décimaux        |
| datetime64       | TEXT        | Dates (format ISO 8601) |
| bool             | INTEGER     | Booléens (0/1)          |
| timedelta        | TEXT        | Durées                  |

### Conversion SQLite → Excel

| Type SQLite | Type Excel     | Description               |
| ----------- | -------------- | ------------------------- |
| TEXT        | Texte          | Chaînes de caractères     |
| INTEGER     | Nombre         | Nombres entiers           |
| REAL        | Nombre         | Nombres décimaux          |
| BLOB        | Texte (Base64) | Données binaires encodées |

Les données sont préservées lors de la conversion dans les deux sens.

## ⚙️ Gestion des conflits et fichiers existants

### Conflits de tables (commande `convert`)

Lorsqu'une table existe déjà dans la base de données :

- **Écraser** : Supprimer la table existante et recréer
- **Ajouter** : Insérer les nouvelles données à la suite
- **Ignorer** : Passer à la feuille suivante
- **Annuler** : Arrêter l'opération

### Fichiers existants

**Base de données existante (convert) :**

- **Utiliser** : Utiliser la base existante (gérer les conflits table par table)
- **Écraser** : Supprimer complètement la base et la recréer
- **Renommer** : Créer une nouvelle base avec un autre nom
- **Annuler** : Arrêter l'opération

**Fichier Excel existant (reverse) :**

- **Écraser** : Remplacer le fichier Excel existant
- **Renommer** : Créer un nouveau fichier avec un autre nom
- **Annuler** : Arrêter l'opération

## 📝 Fichier de log

Chaque opération (convert ou reverse) génère des entrées dans `excel_to_db.log` contenant :

**Pour `convert` (Excel → SQLite) :**

- Timestamp de chaque opération
- Informations sur les feuilles converties
- Types de données détectés
- Nombre de lignes insérées
- Durée des opérations
- Erreurs éventuelles

**Pour `reverse` (SQLite → Excel) :**

- Timestamp de chaque opération
- Informations sur les tables exportées
- Nombre de lignes exportées par table
- Durée des opérations
- Taille du fichier Excel créé
- Erreurs éventuelles

## 🔍 Vérifier les fichiers créés

### Vérifier une base de données SQLite

**Avec l'outil e2db :**

```powershell
python main.py info data/test.db
# ou : e2db info data/test.db
```

**Avec SQLite en ligne de commande :**

```powershell
# Ouvrir la base de données
sqlite3 data/test.db

# Lister les tables
.tables

# Voir le schéma d'une table
.schema clients

# Requête SQL
SELECT * FROM clients LIMIT 10;

# Quitter
.quit
```

**Avec un outil graphique :**

Utilisez [DB Browser for SQLite](https://sqlitebrowser.org/) pour une interface graphique.

### Vérifier un fichier Excel créé

**Ouvrir avec Excel/LibreOffice :**

```powershell
# Windows
start data/export.xlsx

# Ou double-cliquer sur le fichier
```

**Caractéristiques du fichier généré :**

- ✅ Une feuille par table
- ✅ En-têtes formatés (gras, fond bleu)
- ✅ Colonnes auto-ajustées
- ✅ Compatible Excel, LibreOffice, Google Sheets

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

### Erreur lors de l'export Excel

Si l'export vers Excel échoue :

1. Vérifiez que le répertoire de destination existe
2. Fermez le fichier Excel s'il est déjà ouvert
3. Vérifiez les permissions d'écriture du répertoire
4. Utilisez un chemin absolu si nécessaire :

```powershell
python main.py reverse --database data/ma_base.db --output C:\Users\VotreNom\Documents\export.xlsx
```

### Problèmes de performance

Pour de très grandes bases de données ou fichiers Excel :

- La commande `convert` utilise le chunking automatique (10 000 lignes par lot)
- La commande `reverse` charge les tables en mémoire (peut être lent pour des tables > 100 000 lignes)
- Utilisez le mode `--yes` pour éviter les pauses interactives

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Soumettre des pull requests

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails

## 🎯 Cas d'usage

### Scénario 1 : Analyse de données Excel dans Python/SQL

```powershell
# 1. Convertir Excel vers SQLite
python main.py convert -f ventes.xlsx -d ventes.db

# 2. Analyser avec SQL
sqlite3 ventes.db
SELECT categorie, SUM(montant) FROM ventes GROUP BY categorie;

# 3. Exporter le résultat vers Excel
python main.py reverse -d ventes.db -o rapport_ventes.xlsx
```

### Scénario 2 : Backup et restauration

```powershell
# Backup : SQLite → Excel
python main.py reverse -d production.db -o backup_$(date +%Y%m%d).xlsx -y

# Restauration : Excel → SQLite
python main.py convert -f backup_20231031.xlsx -d production_restored.db -y
```

### Scénario 3 : Migration de données

```powershell
# Exporter depuis une ancienne base
python main.py reverse -d ancienne_base.db -o donnees.xlsx

# Modifier dans Excel, puis importer dans la nouvelle base
python main.py convert -f donnees.xlsx -d nouvelle_base.db
```

## 👤 Auteur

Développé avec ❤️ en suivant les meilleures pratiques Python du moment

## 🆘 Support

Pour toute question ou problème :

- Consultez la documentation
- Vérifiez les logs dans `excel_to_db.log`
- Ouvrez une issue sur le dépôt
