"""
Détection et mapping des types de données pandas vers SQLite
"""
import pandas as pd
from typing import Dict, Any


def pandas_to_sqlite_type(dtype: Any) -> str:
    """
    Mapper un type pandas vers un type SQLite.
    
    Mapping:
    - object (str) -> TEXT
    - int64, int32, int16, int8 -> INTEGER
    - float64, float32 -> REAL
    - datetime64 -> TEXT (format ISO)
    - bool -> INTEGER (0/1)
    - timedelta -> TEXT
    
    Args:
        dtype: Type pandas (dtype)
        
    Returns:
        Type SQLite correspondant (TEXT, INTEGER, REAL)
        
    Examples:
        >>> import pandas as pd
        >>> pandas_to_sqlite_type(pd.Int64Dtype())
        'INTEGER'
        >>> pandas_to_sqlite_type(object)
        'TEXT'
    """
    dtype_str = str(dtype).lower()
    
    # Types entiers
    if 'int' in dtype_str:
        return 'INTEGER'
    
    # Types flottants
    if 'float' in dtype_str or 'double' in dtype_str:
        return 'REAL'
    
    # Types datetime
    if 'datetime' in dtype_str or 'timestamp' in dtype_str:
        return 'TEXT'  # Stocké au format ISO 8601
    
    # Types booléens
    if 'bool' in dtype_str:
        return 'INTEGER'  # Stocké comme 0/1
    
    # Types timedelta
    if 'timedelta' in dtype_str:
        return 'TEXT'
    
    # Par défaut: TEXT (pour object, string, etc.)
    return 'TEXT'


def infer_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    Analyser un DataFrame pandas et retourner les types SQLite pour chaque colonne.
    
    Args:
        df: DataFrame pandas à analyser
        
    Returns:
        Dictionnaire {nom_colonne: type_sqlite}
        
    Examples:
        >>> df = pd.DataFrame({'nom': ['Alice', 'Bob'], 'age': [25, 30]})
        >>> types = infer_column_types(df)
        >>> types['nom']
        'TEXT'
        >>> types['age']
        'INTEGER'
    """
    column_types = {}
    
    for column in df.columns:
        dtype = df[column].dtype
        sqlite_type = pandas_to_sqlite_type(dtype)
        column_types[str(column)] = sqlite_type
    
    return column_types


def get_type_stats(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Obtenir des statistiques détaillées sur les types de colonnes.
    
    Retourne pour chaque colonne:
    - Type pandas
    - Type SQLite
    - Nombre de valeurs non-nulles
    - Nombre de valeurs nulles
    - Pourcentage de valeurs nulles
    
    Args:
        df: DataFrame pandas à analyser
        
    Returns:
        Dictionnaire {colonne: {stats}}
    """
    stats = {}
    
    for column in df.columns:
        non_null = df[column].count()
        null_count = df[column].isna().sum()
        total = len(df)
        null_percentage = (null_count / total * 100) if total > 0 else 0
        
        stats[str(column)] = {
            'pandas_type': str(df[column].dtype),
            'sqlite_type': pandas_to_sqlite_type(df[column].dtype),
            'non_null_count': int(non_null),
            'null_count': int(null_count),
            'null_percentage': round(null_percentage, 2),
            'total_rows': total
        }
    
    return stats


def convert_datetime_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convertir les colonnes datetime en format ISO 8601 (chaîne de caractères).
    
    SQLite n'ayant pas de type datetime natif, on convertit en TEXT.
    
    Args:
        df: DataFrame pandas
        
    Returns:
        DataFrame avec les colonnes datetime converties en string
    """
    df_copy = df.copy()
    
    for column in df_copy.columns:
        if pd.api.types.is_datetime64_any_dtype(df_copy[column]):
            # Convertir au format ISO 8601
            df_copy[column] = df_copy[column].dt.strftime('%Y-%m-%d %H:%M:%S')
            # Remplacer NaT (Not a Time) par None
            df_copy[column] = df_copy[column].replace('NaT', None)
        elif pd.api.types.is_timedelta64_dtype(df_copy[column]):
            # Convertir timedelta en string
            df_copy[column] = df_copy[column].astype(str)
            df_copy[column] = df_copy[column].replace('NaT', None)
    
    return df_copy
