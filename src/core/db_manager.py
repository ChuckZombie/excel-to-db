"""
Gestion de la base de données SQLite
"""
import sqlite3
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Literal, Tuple
import logging
import time

from ..core.type_detector import convert_datetime_columns


ConflictAction = Literal['overwrite', 'append', 'skip', 'cancel']


class DatabaseManager:
    """
    Classe pour gérer les opérations sur la base de données SQLite.
    """
    
    def __init__(self, db_path: Path, logger: Optional[logging.Logger] = None):
        """
        Initialiser le gestionnaire de base de données.
        
        Args:
            db_path: Chemin vers le fichier de base de données SQLite
            logger: Logger optionnel
        """
        self.db_path = Path(db_path)
        self.logger = logger
        self.conn: Optional[sqlite3.Connection] = None
    
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
    
    def table_exists(self, table_name: str) -> bool:
        """
        Vérifier si une table existe dans la base de données.
        
        Args:
            table_name: Nom de la table
            
        Returns:
            True si la table existe, False sinon
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        
        exists = cursor.fetchone() is not None
        return exists
    
    def get_all_tables(self) -> List[str]:
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
        return tables
    
    def get_table_info(self, table_name: str) -> List[Dict]:
        """
        Obtenir les informations sur les colonnes d'une table.
        
        Args:
            table_name: Nom de la table
            
        Returns:
            Liste de dictionnaires avec les infos des colonnes
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute(f"PRAGMA table_info({table_name})")
        
        columns = []
        for row in cursor.fetchall():
            columns.append({
                'cid': row[0],
                'name': row[1],
                'type': row[2],
                'notnull': bool(row[3]),
                'default': row[4],
                'pk': bool(row[5])
            })
        
        return columns
    
    def get_row_count(self, table_name: str) -> int:
        """
        Obtenir le nombre de lignes dans une table.
        
        Args:
            table_name: Nom de la table
            
        Returns:
            Nombre de lignes
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        
        return count
    
    def drop_table(self, table_name: str) -> None:
        """
        Supprimer une table de la base de données.
        
        Args:
            table_name: Nom de la table à supprimer
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()
        
        if self.logger:
            self.logger.info(f"Table '{table_name}' supprimée")
    
    def insert_dataframe(
        self,
        df: pd.DataFrame,
        table_name: str,
        if_exists: Literal['fail', 'replace', 'append'] = 'fail',
        chunk_size: int = 10000
    ) -> int:
        """
        Insérer un DataFrame pandas dans une table SQLite.
        
        Args:
            df: DataFrame à insérer
            table_name: Nom de la table de destination
            if_exists: Action si la table existe ('fail', 'replace', 'append')
            chunk_size: Taille des chunks pour l'insertion
            
        Returns:
            Nombre de lignes insérées
            
        Raises:
            ValueError: Si if_exists='fail' et la table existe
        """
        conn = self.connect()
        
        # Convertir les colonnes datetime en string
        df_to_insert = convert_datetime_columns(df)
        
        start_time = time.time()
        
        try:
            # Insérer les données
            df_to_insert.to_sql(
                name=table_name,
                con=conn,
                if_exists=if_exists,
                index=False,
                method='multi',
                chunksize=chunk_size
            )
            
            conn.commit()
            
            duration = time.time() - start_time
            rows_inserted = len(df)
            
            if self.logger:
                self.logger.info(
                    f"Table '{table_name}': {rows_inserted} lignes insérées "
                    f"en {duration:.2f}s"
                )
            
            return rows_inserted
            
        except Exception as e:
            conn.rollback()
            if self.logger:
                self.logger.error(
                    f"Erreur lors de l'insertion dans '{table_name}': {str(e)}"
                )
            raise Exception(f"Impossible d'insérer les données: {str(e)}")
    
    def handle_table_conflict(
        self,
        table_name: str,
        action: ConflictAction
    ) -> Literal['replace', 'append', 'skip']:
        """
        Gérer le conflit lorsqu'une table existe déjà.
        
        Args:
            table_name: Nom de la table en conflit
            action: Action à effectuer ('overwrite', 'append', 'skip', 'cancel')
            
        Returns:
            Action correspondante pour pandas to_sql ('replace', 'append', 'skip')
            
        Raises:
            ValueError: Si action='cancel'
        """
        if action == 'overwrite':
            if self.logger:
                self.logger.info(f"Écrasement de la table '{table_name}'")
            return 'replace'
        
        elif action == 'append':
            if self.logger:
                self.logger.info(f"Ajout de données à la table '{table_name}'")
            return 'append'
        
        elif action == 'skip':
            if self.logger:
                self.logger.info(f"Table '{table_name}' ignorée")
            return 'skip'
        
        elif action == 'cancel':
            if self.logger:
                self.logger.info("Opération annulée par l'utilisateur")
            raise ValueError("Opération annulée")
        
        else:
            raise ValueError(f"Action inconnue: {action}")
    
    def get_database_size(self) -> Tuple[int, str]:
        """
        Obtenir la taille de la base de données.
        
        Returns:
            Tuple (taille_en_octets, taille_formatée)
        """
        if not self.db_path.exists():
            return 0, "0 B"
        
        size_bytes = self.db_path.stat().st_size
        
        # Formater la taille
        if size_bytes < 1024:
            size_str = f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            size_str = f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
        
        return size_bytes, size_str
    
    def get_database_stats(self) -> Dict:
        """
        Obtenir des statistiques sur la base de données.
        
        Returns:
            Dictionnaire avec les statistiques
        """
        tables = self.get_all_tables()
        total_rows = 0
        
        table_stats = []
        for table in tables:
            row_count = self.get_row_count(table)
            total_rows += row_count
            
            columns = self.get_table_info(table)
            
            table_stats.append({
                'name': table,
                'rows': row_count,
                'columns': len(columns)
            })
        
        size_bytes, size_str = self.get_database_size()
        
        stats = {
            'path': str(self.db_path),
            'size_bytes': size_bytes,
            'size_formatted': size_str,
            'tables_count': len(tables),
            'total_rows': total_rows,
            'tables': table_stats
        }
        
        return stats
    
    def __enter__(self):
        """Support du context manager."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support du context manager."""
        self.close()
