"""
Lecture des données depuis une base de données SQLite
"""
import sqlite3
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
import logging


class DatabaseReader:
    """
    Classe pour lire les données d'une base de données SQLite.
    """
    
    def __init__(self, db_path: Path, logger: Optional[logging.Logger] = None):
        """
        Initialiser le lecteur de base de données.
        
        Args:
            db_path: Chemin vers le fichier de base de données SQLite
            logger: Logger optionnel
        """
        self.db_path = Path(db_path)
        self.logger = logger
        self._validate_database()
        self.conn: Optional[sqlite3.Connection] = None
        
    def _validate_database(self) -> None:
        """
        Valider que le fichier de base de données existe et est accessible.
        
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            ValueError: Si le fichier n'est pas une base SQLite valide
        """
        if not self.db_path.exists():
            raise FileNotFoundError(f"La base de données {self.db_path} n'existe pas")
        
        if self.db_path.suffix.lower() not in ['.db', '.sqlite', '.sqlite3']:
            if self.logger:
                self.logger.warning(
                    f"Extension de fichier inhabituelle: {self.db_path.suffix}"
                )
    
    def connect(self) -> sqlite3.Connection:
        """
        Établir une connexion à la base de données.
        
        Returns:
            Connexion SQLite
        """
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            if self.logger:
                self.logger.info(f"Connexion établie à la base: {self.db_path}")
        return self.conn
    
    def close(self) -> None:
        """
        Fermer la connexion à la base de données.
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            if self.logger:
                self.logger.info("Connexion fermée")
    
    def get_table_names(self) -> List[str]:
        """
        Obtenir la liste de toutes les tables dans la base de données.
        
        Returns:
            Liste des noms de tables
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        
        tables = [row[0] for row in cursor.fetchall()]
        
        if self.logger:
            self.logger.info(f"Tables détectées: {len(tables)}")
        
        return tables
    
    def get_table_info(self, table_name: str) -> Dict:
        """
        Obtenir les informations sur une table.
        
        Args:
            table_name: Nom de la table
            
        Returns:
            Dictionnaire avec les informations de la table:
            - name: nom de la table
            - rows: nombre de lignes
            - columns: nombre de colonnes
            - column_names: liste des noms de colonnes
            - column_types: types SQLite des colonnes
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # Obtenir les informations sur les colonnes
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        column_names = [col[1] for col in columns]
        column_types = {col[1]: col[2] for col in columns}
        
        # Compter le nombre de lignes
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        
        info = {
            'name': table_name,
            'rows': row_count,
            'columns': len(column_names),
            'column_names': column_names,
            'column_types': column_types
        }
        
        if self.logger:
            self.logger.info(
                f"Table '{table_name}': {row_count} lignes, "
                f"{len(column_names)} colonnes"
            )
        
        return info
    
    def get_all_tables_info(self) -> List[Dict]:
        """
        Obtenir les informations de toutes les tables de la base.
        
        Returns:
            Liste de dictionnaires avec les informations de chaque table
        """
        table_names = self.get_table_names()
        tables_info = []
        
        for table_name in table_names:
            try:
                info = self.get_table_info(table_name)
                tables_info.append(info)
            except Exception as e:
                if self.logger:
                    self.logger.warning(
                        f"Impossible de lire la table '{table_name}': {str(e)}"
                    )
                # Continuer avec les autres tables
                continue
        
        return tables_info
    
    def read_table(self, table_name: str) -> pd.DataFrame:
        """
        Lire toutes les données d'une table dans un DataFrame.
        
        Args:
            table_name: Nom de la table à lire
            
        Returns:
            DataFrame pandas avec les données de la table
            
        Raises:
            Exception: Si la table ne peut pas être lue
        """
        conn = self.connect()
        
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            
            if self.logger:
                self.logger.info(
                    f"Table '{table_name}' lue: {len(df)} lignes, "
                    f"{len(df.columns)} colonnes"
                )
            
            return df
        except Exception as e:
            if self.logger:
                self.logger.error(
                    f"Erreur lors de la lecture de la table '{table_name}': {str(e)}"
                )
            raise Exception(f"Impossible de lire la table '{table_name}': {str(e)}")
    
    def __enter__(self):
        """Support du context manager."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support du context manager."""
        self.close()
