"""
Affichage des données pour la conversion SQLite vers Excel
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box


console = Console()


def show_reverse_summary(
    excel_path: str,
    tables_exported: int,
    total_rows: int,
    duration: float,
    file_size: str,
    log_file: str
) -> None:
    """
    Afficher le résumé final de la conversion SQLite vers Excel.
    
    Args:
        excel_path: Chemin vers le fichier Excel créé
        tables_exported: Nombre de tables exportées
        total_rows: Nombre total de lignes exportées
        duration: Durée totale en secondes
        file_size: Taille du fichier Excel formatée
        log_file: Chemin vers le fichier de log
    """
    # Calculer les statistiques de performance
    rows_per_second = int(total_rows / duration) if duration > 0 else 0
    
    console.print()
    
    # Afficher les statistiques détaillées sous forme de grille
    grid = Table.grid(padding=(0, 2), expand=True)
    grid.add_column(style="bold cyan", justify="right")
    grid.add_column(style="white")
    
    grid.add_row("Tables exportées:", f"{tables_exported}")
    grid.add_row("Lignes exportées:", f"{total_rows:,}")
    grid.add_row("Fichier Excel:", f"{excel_path}")
    grid.add_row("Taille:", f"{file_size}")
    grid.add_row("Durée:", f"{duration:.2f}s")
    grid.add_row("Performance:", f"{rows_per_second:,} lignes/s")
    grid.add_row("Fichier de log:", f"{log_file}")
    
    console.print(Panel(
        grid,
        title="[bold]✓ Conversion terminée avec succès[/bold]",
        title_align="left",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 2)
    ))
    
    console.print()


def show_table_list(tables_info: list) -> None:
    """
    Afficher la liste des tables avec leurs informations.
    
    Args:
        tables_info: Liste des informations sur les tables
    """
    table = Table(
        show_header=True,
        header_style="bold white on blue",
        border_style="bright_blue",
        row_styles=["", "dim"],
        box=box.ROUNDED,
        expand=True
    )
    
    table.add_column("Table", style="cyan")
    table.add_column("Lignes", justify="right", style="yellow")
    table.add_column("Colonnes", justify="right", style="blue")
    
    for info in tables_info:
        table.add_row(
            info['name'],
            f"{info['rows']:,}",
            str(info['columns'])
        )
    
    console.print(table)
