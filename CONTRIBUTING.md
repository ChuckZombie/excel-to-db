# Guide de Contribution

Merci de votre intérêt pour contribuer à Excel to DB !

## Comment contribuer

### Signaler un bug

1. Vérifiez que le bug n'a pas déjà été signalé dans les Issues
2. Créez une nouvelle Issue avec :
   - Description claire du problème
   - Étapes pour reproduire
   - Comportement attendu vs réel
   - Version de Python et des dépendances

- Logs pertinents (depuis `excel_to_db.log`)

### Proposer une fonctionnalité

1. Créez une Issue pour discuter de la fonctionnalité
2. Expliquez le cas d'usage et la valeur ajoutée
3. Attendez les retours avant de commencer le développement

### Soumettre du code

1. **Fork** le projet
2. **Créez une branche** : `git checkout -b feature/ma-fonctionnalite`
3. **Développez** en suivant les standards du projet
4. **Testez** votre code
5. **Committez** : `git commit -m "feat: description claire"`
6. **Pushez** : `git push origin feature/ma-fonctionnalite`
7. **Créez une Pull Request**

## Standards de code

### Style Python

- Suivre **PEP 8**
- Utiliser **type hints** partout
- Docstrings pour toutes les fonctions publiques
- Noms en anglais pour le code, français acceptable pour les messages utilisateur

### Exemple de fonction bien documentée

```python
def clean_column_name(name: str) -> str:
    """
    Nettoyer un nom de colonne pour SQLite.

    Règles appliquées :
    - Strip des espaces en début/fin
    - Remplacement des espaces et caractères spéciaux par underscore
    - Conversion en minuscules

    Args:
        name: Nom de colonne brut

    Returns:
        Nom de colonne nettoyé

    Examples:
        >>> clean_column_name("  Prénom Client  ")
        'prenom_client'
    """
    # Implémentation...
    pass
```

### Commits

Format des messages de commit :

```
type: description courte

Description détaillée si nécessaire

Référence à l'issue: #123
```

**Types** :

- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage, pas de changement de code
- `refactor`: Refactoring sans changement de comportement
- `test`: Ajout ou modification de tests
- `chore`: Maintenance, dépendances, etc.

### Tests

- Ajouter des tests pour toute nouvelle fonctionnalité
- Maintenir ou améliorer la couverture de tests
- Les tests doivent passer avant toute PR

```bash
# Lancer les tests
python -m unittest discover tests
```

### Documentation

- Mettre à jour le README si nécessaire
- Documenter les nouvelles fonctionnalités
- Ajouter des exemples d'utilisation

## Architecture

Respecter l'architecture modulaire :

```
excel_to_sqlite/
├── core/       # Logique métier (pas d'UI ici)
├── ui/         # Interface utilisateur uniquement
└── utils/      # Utilitaires généraux
```

**Règles** :

- `core/` ne doit pas importer de `ui/`
- Toutes les classes doivent accepter un logger optionnel
- Préférer la composition à l'héritage
- Fonctions pures quand possible

## Checklist avant PR

- [ ] Le code respecte PEP 8
- [ ] Type hints ajoutés
- [ ] Docstrings à jour
- [ ] Tests écrits et passent
- [ ] Documentation mise à jour
- [ ] Pas de warnings/erreurs
- [ ] Commits bien formatés
- [ ] Branch à jour avec main

## Environnement de développement

### Installation en mode développement

```bash
# Cloner votre fork
git clone https://github.com/votre-username/excel-to-db.git
cd excel-to-db

# Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

# Installer en mode éditable avec dépendances dev
pip install -e .
pip install -r requirements.txt
pip install black pylint mypy  # Outils de dev
```

### Outils recommandés

- **Black** : Formatage automatique

  ```bash
  black excel_to_sqlite/
  ```

- **Pylint** : Analyse statique

  ```bash
  pylint excel_to_sqlite/
  ```

- **Mypy** : Vérification de types
  ```bash
  mypy excel_to_sqlite/
  ```

## Questions ?

N'hésitez pas à :

- Ouvrir une Issue pour poser des questions
- Consulter la documentation technique dans `... oups, il n'y en à pas`
- Regarder les exemples de code existants
