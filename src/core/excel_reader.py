"""
Lecture et analyse des fichiers Excel
"""
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging

from ..core.type_detector import infer_column_types, get_type_stats, convert_datetime_columns
from ..utils.name_cleaner import clean_table_name, clean_and_ensure_unique


class ExcelReader:
    """
    Classe pour lire et analyser des fichiers Excel.
    """
    
    def __init__(self, file_path: Path, logger: Optional[logging.Logger] = None):
        """
        Initialiser le lecteur Excel.
        
        Args:
            file_path: Chemin vers le fichier Excel
            logger: Logger optionnel
        """
        self.file_path = Path(file_path)
        self.logger = logger
        self._validate_file()
        
    def _validate_file(self) -> None:
        """
        Valider que le fichier existe et est lisible.
        
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            ValueError: Si le fichier n'est pas un Excel valide
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"Le fichier {self.file_path} n'existe pas")
        
        if self.file_path.suffix.lower() not in ['.xlsx', '.xls', '.xlsm']:
            raise ValueError(
                f"Format de fichier non supporté: {self.file_path.suffix}. "
                "Formats acceptés: .xlsx, .xls, .xlsm"
            )
    
    def get_sheet_names(self) -> List[str]:
        """
        Obtenir la liste des noms de feuilles dans le fichier Excel.
        
        Returns:
            Liste des noms de feuilles
            
        Raises:
            Exception: Si le fichier ne peut pas être lu
        """
        try:
            excel_file = pd.ExcelFile(self.file_path)
            sheet_names = excel_file.sheet_names
            
            if self.logger:
                self.logger.info(
                    f"Fichier analysé: {len(sheet_names)} feuille(s) détectée(s)"
                )
            
            return sheet_names
        except Exception as e:
            if self.logger:
                self.logger.error(f"Erreur lors de la lecture du fichier: {str(e)}")
            raise Exception(f"Impossible de lire le fichier Excel: {str(e)}")
    
    def read_sheet(
        self,
        sheet_name: str,
        nrows: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Lire une feuille Excel spécifique.
        
        Args:
            sheet_name: Nom de la feuille à lire
            nrows: Nombre de lignes à lire (None = toutes)
            
        Returns:
            DataFrame pandas avec les données de la feuille
            
        Raises:
            Exception: Si la feuille ne peut pas être lue
        """
        try:
            df = pd.read_excel(
                self.file_path,
                sheet_name=sheet_name,
                nrows=nrows
            )
            
            # Nettoyer les noms de colonnes
            df.columns = clean_and_ensure_unique(df.columns.tolist())
            
            if self.logger:
                self.logger.info(
                    f"Feuille '{sheet_name}' lue: {len(df)} lignes, "
                    f"{len(df.columns)} colonnes"
                )
            
            return df
        except Exception as e:
            if self.logger:
                self.logger.error(
                    f"Erreur lors de la lecture de la feuille '{sheet_name}': {str(e)}"
                )
            raise Exception(f"Impossible de lire la feuille '{sheet_name}': {str(e)}")
    
    def get_sheet_info(self, sheet_name: str) -> Dict:
        """
        Obtenir les informations détaillées sur une feuille.
        
        Args:
            sheet_name: Nom de la feuille
            
        Returns:
            Dictionnaire avec les informations de la feuille:
            - name: nom d'origine
            - table_name: nom nettoyé pour SQLite
            - rows: nombre de lignes
            - columns: nombre de colonnes
            - column_names: liste des noms de colonnes
            - column_types: types SQLite détectés
            - preview_df: DataFrame avec les premières lignes
        """
        # Lire toute la feuille pour le comptage complet
        df_full = self.read_sheet(sheet_name)
        
        # Lire seulement les premières lignes pour l'aperçu
        df_preview = df_full.head(10)
        
        # Détecter automatiquement les types de colonnes
        column_types = infer_column_types(df_full)
        
        info = {
            'name': sheet_name,
            'table_name': clean_table_name(sheet_name),
            'rows': len(df_full),
            'columns': len(df_full.columns),
            'column_names': df_full.columns.tolist(),
            'column_types': column_types,
            'preview_df': df_preview,
            'type_stats': get_type_stats(df_full)
        }
        
        return info
    
    def get_all_sheets_info(self) -> List[Dict]:
        """
        Obtenir les informations de toutes les feuilles du fichier.
        
        Returns:
            Liste de dictionnaires avec les informations de chaque feuille
        """
        sheet_names = self.get_sheet_names()
        sheets_info = []
        
        for sheet_name in sheet_names:
            try:
                info = self.get_sheet_info(sheet_name)
                sheets_info.append(info)
            except Exception as e:
                if self.logger:
                    self.logger.warning(
                        f"Impossible de lire la feuille '{sheet_name}': {str(e)}"
                    )
                # Continuer avec les autres feuilles
                continue
        
        return sheets_info
