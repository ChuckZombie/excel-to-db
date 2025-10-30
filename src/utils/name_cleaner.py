"""
Nettoyage des noms de colonnes et de tables pour la base de données SQLite
"""
import re
from typing import List


def clean_column_name(name: str) -> str:
    """
    Nettoyer un nom de colonne pour le rendre compatible avec SQLite.
    
    Règles appliquées :
    - Suppression des espaces en début et fin
    - Remplacement des espaces et caractères spéciaux par underscore
    - Conversion en minuscules
    - Suppression des underscores multiples consécutifs
    
    Args:
        name: Nom de colonne brut
        
    Returns:
        Nom de colonne nettoyé et compatible SQLite
        
    Examples:
        >>> clean_column_name("  Prénom Client  ")
        'prenom_client'
        >>> clean_column_name("Date de Naissance")
        'date_de_naissance'
    """
    if not name or not isinstance(name, str):
        return "colonne_sans_nom"
    
    # Supprimer les espaces en début et fin
    cleaned = name.strip()
    
    # Remplacer les caractères accentués
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a',
        'ô': 'o', 'ö': 'o',
        'û': 'u', 'ü': 'u', 'ù': 'u',
        'î': 'i', 'ï': 'i',
        'ç': 'c',
        'É': 'e', 'È': 'e', 'Ê': 'e', 'Ë': 'e',
        'À': 'a', 'Â': 'a', 'Ä': 'a',
        'Ô': 'o', 'Ö': 'o',
        'Û': 'u', 'Ü': 'u', 'Ù': 'u',
        'Î': 'i', 'Ï': 'i',
        'Ç': 'c',
    }
    
    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)
    
    # Convertir en minuscules
    cleaned = cleaned.lower()
    
    # Remplacer tous les caractères non alphanumériques par underscore
    cleaned = re.sub(r'[^a-z0-9]+', '_', cleaned)
    
    # Supprimer les underscores au début et à la fin
    cleaned = cleaned.strip('_')
    
    # Remplacer les underscores multiples par un seul underscore
    cleaned = re.sub(r'_+', '_', cleaned)
    
    # Si le nom est vide après le nettoyage, utiliser un nom par défaut
    if not cleaned:
        cleaned = "colonne_sans_nom"
    
    # Si le nom commence par un chiffre, ajouter un préfixe
    if cleaned[0].isdigit():
        cleaned = f"col_{cleaned}"
    
    return cleaned


def clean_table_name(name: str) -> str:
    """
    Nettoyer un nom de table pour le rendre compatible avec SQLite.
    
    Applique les mêmes règles de nettoyage que clean_column_name.
    
    Args:
        name: Nom de table brut (généralement le nom de l'onglet Excel)
        
    Returns:
        Nom de table nettoyé et compatible SQLite
        
    Examples:
        >>> clean_table_name("Données Clients")
        'donnees_clients'
        >>> clean_table_name("Sheet 1")
        'sheet_1'
    """
    if not name or not isinstance(name, str):
        return "table_sans_nom"
    
    return clean_column_name(name)


def ensure_unique_names(names: List[str]) -> List[str]:
    """
    S'assurer que tous les noms dans une liste sont uniques.
    
    Ajoute un suffixe numérique (_2, _3, etc.) en cas de doublons.
    
    Args:
        names: Liste de noms (potentiellement avec des doublons)
        
    Returns:
        Liste de noms uniques et numérotés si nécessaire
        
    Examples:
        >>> ensure_unique_names(['id', 'nom', 'id', 'nom'])
        ['id', 'nom', 'id_2', 'nom_2']
    """
    seen = {}
    unique_names = []
    
    for name in names:
        if name not in seen:
            seen[name] = 1
            unique_names.append(name)
        else:
            seen[name] += 1
            unique_name = f"{name}_{seen[name]}"
            # S'assurer que le nouveau nom généré n'existe pas déjà
            while unique_name in seen:
                seen[name] += 1
                unique_name = f"{name}_{seen[name]}"
            seen[unique_name] = 1
            unique_names.append(unique_name)
    
    return unique_names


def clean_and_ensure_unique(names: List[str]) -> List[str]:
    """
    Nettoyer une liste de noms de colonnes et s'assurer de leur unicité.
    
    Args:
        names: Liste de noms de colonnes bruts
        
    Returns:
        Liste de noms de colonnes nettoyés et uniques
        
    Examples:
        >>> clean_and_ensure_unique(['Nom', 'Prénom', 'NOM'])
        ['nom', 'prenom', 'nom_2']
    """
    cleaned = [clean_column_name(name) for name in names]
    return ensure_unique_names(cleaned)
