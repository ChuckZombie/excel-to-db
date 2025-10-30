"""
Point d'entrée principal de l'application Excel to SQLite Converter
"""
import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
import time
import sys

from src.core.excel_reader import ExcelReader
from src.core.db_manager import DatabaseManager
from src.utils.logger import (
    setup_logger,
    log_conversion_start,
    log_conversion_success,
    log_conversion_summary,
    log_error
)
from src.ui.display import (
    show_conversion_summary,
    show_error,
    show_success,
    show_info,
    show_database_stats,
    clear_screen
)
from src.ui.prompts import (
    prompt_excel_file,
    prompt_database_name,
    prompt_select_sheets,
    prompt_conflict_action,
    prompt_database_exists_action,
    prompt_new_database_name,
)

# Constantes
DEFAULT_CHUNK_SIZE = 10000
DEFAULT_PREVIEW_ROWS = 10

app = typer.Typer(help="Excel to SQLite Converter - Convertir des fichiers Excel en base SQLite")
console = Console()


@app.command()
def convert(
    file_path: str = typer.Option(
        None,
        "--file",
        "-f",
        help="Chemin vers le fichier Excel à convertir"
    ),
    db_name: str = typer.Option(
        None,
        "--database",
        "-d",
        help="Nom de la base de données de destination"
    ),
    auto_yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Accepter automatiquement toutes les confirmations"
    )
):
    """
    Convertir un fichier Excel en base de données SQLite.
    
    Mode interactif avec guidage pas à pas.
    """
    # Nettoyer l'écran pour démarrer
    clear_screen()
    
    # Initialiser le logger
    logger = setup_logger()
    
    try:
        # ÉTAPE 1: Sélection du fichier Excel
        if file_path:
            excel_path = Path(file_path)
            if not excel_path.exists():
                show_error(f"Le fichier {file_path} n'existe pas")
                return
            show_info(f"Fichier sélectionné : {excel_path}")
        else:
            excel_path = prompt_excel_file()
            if not excel_path:
                show_info("Opération annulée par l'utilisateur")
                return
        
        log_conversion_start(logger, excel_path)
        
        # ÉTAPE 2: Analyse des feuilles
        console.print("\n[bold cyan]Analyse du fichier Excel[/bold cyan]\n")
        
        with console.status("[bold green]Analyse du fichier en cours..."):
            reader = ExcelReader(excel_path, logger)
            
            sheets_info = reader.get_all_sheets_info()
        
        if not sheets_info:
            show_error("Aucune feuille valide trouvée dans le fichier")
            return
        
        show_success(f"{len(sheets_info)} feuille(s) détectée(s)")
        console.print()

        # ÉTAPE 4: Choix du nom de base de données
        console.print("\n[bold cyan]Configuration de la base de données[/bold cyan]\n")
        
        if db_name:
            database_name = db_name if db_name.endswith('.db') else f"{db_name}.db"
            show_info(f"Base de données : {database_name}")
        else:
            # Suggérer un nom basé sur le nom du fichier Excel
            suggested_name = excel_path.stem + '.db'
            database_name = prompt_database_name(suggested_name)
            if not database_name:
                show_info("Opération annulée par l'utilisateur")
                return
        
        # Placer la base de données dans le même répertoire que le fichier Excel
        db_path = Path(database_name)
        if not db_path.is_absolute():
            db_path = excel_path.parent / db_path
        
        # Gérer le cas où la base existe déjà
        if db_path.exists():
            if auto_yes:
                db_action = 'use'
            else:
                db_action = prompt_database_exists_action()
            
            if db_action == 'cancel' or db_action is None:
                show_info("Opération annulée par l'utilisateur")
                return
            elif db_action == 'overwrite':
                db_path.unlink()
                show_success("Base de données existante supprimée")
            elif db_action == 'rename':
                new_name = prompt_new_database_name(database_name)
                if not new_name:
                    show_info("Opération annulée par l'utilisateur")
                    return
                # Placer dans le même répertoire que le fichier Excel
                db_path = Path(new_name)
                if not db_path.is_absolute():
                    db_path = excel_path.parent / db_path
        
        # ÉTAPE 5: Sélection des feuilles à convertir
        console.print("\n[bold cyan]Sélection des feuilles[/bold cyan]\n")
        
        if auto_yes:
            selected_sheets = [info['name'] for info in sheets_info]
        else:
            selected_sheets = prompt_select_sheets(sheets_info)
            if not selected_sheets:
                show_info("Opération annulée par l'utilisateur")
                return
        
        # Filtrer uniquement les feuilles sélectionnées
        sheets_to_convert = [
            info for info in sheets_info
            if info['name'] in selected_sheets
        ]
        
        show_success(f"{len(sheets_to_convert)} feuille(s) sélectionnée(s) pour la conversion")
        
        # ÉTAPE 6: Conversion
        console.print("\n[bold cyan]Conversion en cours...[/bold cyan]\n")
        
        db_manager = DatabaseManager(db_path, logger)
        
        total_rows_inserted = 0
        sheets_converted = 0
        conversion_start_time = time.time()
        
        # Progress bar pour chaque feuille
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            
            for sheet_info in sheets_to_convert:
                sheet_name = sheet_info['name']
                table_name = sheet_info['table_name']
                total_rows = sheet_info['rows']
                
                # Vérifier si la table existe déjà
                if db_manager.table_exists(table_name):
                    existing_rows = db_manager.get_row_count(table_name)
                    
                    if auto_yes:
                        conflict_action = 'append'
                    else:
                        conflict_action = prompt_conflict_action(table_name, existing_rows)
                    
                    if conflict_action == 'cancel' or conflict_action is None:
                        show_info("Conversion annulée par l'utilisateur")
                        db_manager.close()
                        return
                    
                    if conflict_action == 'skip':
                        show_info(f"Feuille '{sheet_name}' ignorée")
                        continue
                    
                    # Convertir l'action choisie en paramètre pour to_sql
                    if_exists = db_manager.handle_table_conflict(table_name, conflict_action)
                else:
                    if_exists = 'fail'
                
                # Créer une tâche pour la barre de progression
                task = progress.add_task(
                    f"[cyan]{sheet_name}[/cyan]",
                    total=total_rows
                )
                
                # Lire l'intégralité de la feuille
                df = reader.read_sheet(sheet_name)
                
                # Insérer dans la base de données
                sheet_start_time = time.time()
                
                try:
                    rows_inserted = db_manager.insert_dataframe(
                        df,
                        table_name,
                        if_exists=if_exists,
                        chunk_size=DEFAULT_CHUNK_SIZE
                    )
                    
                    sheet_duration = time.time() - sheet_start_time
                    
                    # Mettre à jour la barre de progression
                    progress.update(task, completed=total_rows)
                    
                    # Enregistrer le succès dans les logs
                    log_conversion_success(logger, table_name, rows_inserted, sheet_duration)
                    
                    total_rows_inserted += rows_inserted
                    sheets_converted += 1
                    
                except Exception as e:
                    log_error(logger, e, f"Conversion de '{sheet_name}'")
                    show_error(f"Erreur lors de la conversion de '{sheet_name}'", e)
                    # Continuer avec les autres feuilles restantes
                    continue
        
        # Fermer la connexion à la base de données
        db_manager.close()
        
        total_duration = time.time() - conversion_start_time
        
        # ÉTAPE 7: Résumé final
        console.print()
        
        # Obtenir la taille finale de la base de données
        size_bytes, size_str = DatabaseManager(db_path, logger).get_database_size()
        
        # Enregistrer le résumé dans les logs
        log_conversion_summary(
            logger,
            db_path,
            sheets_converted,
            total_rows_inserted,
            total_duration
        )
        
        # Afficher le résumé final à l'utilisateur
        show_conversion_summary(
            str(db_path),
            sheets_converted,
            total_rows_inserted,
            total_duration,
            size_str,
                "excel_to_db.log"
        )
        
    except KeyboardInterrupt:
        show_info("\n\nOpération interrompue par l'utilisateur")
        logger.info("Opération interrompue par l'utilisateur (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        log_error(logger, e, "Erreur fatale")
        show_error("Une erreur inattendue s'est produite", e)
        sys.exit(1)


@app.command()
def info(
    db_path: str = typer.Argument(..., help="Chemin vers la base de données SQLite")
):
    """
    Afficher les informations d'une base de données SQLite.
    """
    db_file = Path(db_path)
    
    if not db_file.exists():
        show_error(f"La base de données {db_path} n'existe pas")
        return
    
    logger = setup_logger()
    db_manager = DatabaseManager(db_file, logger)
    
    try:
        stats = db_manager.get_database_stats()
        show_database_stats(stats)
    except Exception as e:
        show_error("Erreur lors de la lecture de la base de données", e)
    finally:
        db_manager.close()


@app.command()
def version():
    """
    Afficher la version de l'application.
    """
    from src import __version__
    console.print(f"Excel to SQLite Converter v[bold cyan]{__version__}[/bold cyan]")


if __name__ == "__main__":
    app()
