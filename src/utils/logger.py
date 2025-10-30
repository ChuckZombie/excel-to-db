"""
Configuration du système de logging pour l'application
"""
import logging
from pathlib import Path
from typing import Optional


def setup_logger(
    log_file: Optional[Path] = None,
    level: int = logging.INFO
) -> logging.Logger:
    """
    Configurer le système de logging de l'application.
    
    Crée un logger qui écrit à la fois dans un fichier et dans la console.
    
    Args:
           log_file: Chemin vers le fichier de log (par défaut: excel_to_db.log)
        level: Niveau de logging (par défaut: INFO)
        
    Returns:
        Logger configuré et prêt à l'emploi
    """
    if log_file is None:
           log_file = Path("excel_to_db.log")
    
    # Créer le logger principal
    logger = logging.getLogger("excel_to_sqlite")
    logger.setLevel(level)
    
    # Éviter la duplication des handlers si le logger existe déjà
    if logger.handlers:
        return logger
    
    # Format des messages de log
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler pour l'écriture dans le fichier
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler pour la console (optionnel, pour le debug)
    # Commenté pour éviter la duplication avec rich
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.WARNING)
    # console_handler.setFormatter(formatter)
    # logger.addHandler(console_handler)
    
    return logger


def log_conversion_start(logger: logging.Logger, file_path: Path) -> None:
    """
    Enregistrer le démarrage d'une conversion dans les logs.
    
    Args:
        logger: Logger configuré
        file_path: Chemin vers le fichier Excel à convertir
    """
    logger.info("=" * 60)
    logger.info("Démarrage de la conversion")
    logger.info(f"Fichier source: {file_path}")


def log_conversion_success(
    logger: logging.Logger,
    table_name: str,
    rows_inserted: int,
    duration: float
) -> None:
    """
    Enregistrer le succès d'une conversion de feuille dans les logs.
    
    Args:
        logger: Logger configuré
        table_name: Nom de la table créée
        rows_inserted: Nombre de lignes insérées
        duration: Durée de l'opération en secondes
    """
    logger.info(
        f"SUCCESS - Table '{table_name}': {rows_inserted} lignes insérées "
        f"en {duration:.2f}s"
    )


def log_conversion_summary(
    logger: logging.Logger,
    db_path: Path,
    sheets_converted: int,
    total_rows: int,
    total_duration: float
) -> None:
    """
    Enregistrer le résumé final de la conversion dans les logs.
    
    Args:
        logger: Logger configuré
        db_path: Chemin vers la base de données créée
        sheets_converted: Nombre de feuilles converties
        total_rows: Nombre total de lignes insérées
        total_duration: Durée totale en secondes
    """
    logger.info("=" * 60)
    logger.info("Conversion terminée avec succès")
    logger.info(f"Base de données: {db_path}")
    logger.info(f"Feuilles converties: {sheets_converted}")
    logger.info(f"Lignes totales insérées: {total_rows}")
    logger.info(f"Durée totale: {total_duration:.2f}s")
    logger.info("=" * 60)


def log_error(logger: logging.Logger, error: Exception, context: str = "") -> None:
    """
    Enregistrer une erreur dans les logs.
    
    Args:
        logger: Logger configuré
        error: Exception levée
        context: Contexte dans lequel l'erreur s'est produite
    """
    if context:
        logger.error(f"ERREUR [{context}]: {str(error)}")
    else:
        logger.error(f"ERREUR: {str(error)}")
    logger.exception(error)
