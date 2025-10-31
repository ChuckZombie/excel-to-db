"""
Affichage spécifique pour la conversion Excel vers SQLite
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


def show_conversion_summary(
    db_path: str,
    sheets_converted: int,
    total_rows: int,
    duration: float,
    db_size: str,
    log_file: str
) -> None:
    """Afficher le résumé final de la conversion."""
    rows_per_second = int(total_rows / duration) if duration > 0 else 0
    
    console.print()
    
    grid = Table.grid(padding=(0, 2), expand=True)
    grid.add_column(style="bold cyan", justify="right")
    grid.add_column(style="white")
    
    grid.add_row("Feuilles converties:", f"{sheets_converted}")
    grid.add_row("Lignes insérées:", f"{total_rows:,}")
    grid.add_row("Base de données:", f"{db_path}")
    grid.add_row("Taille:", f"{db_size}")
    grid.add_row("Durée:", f"{duration:.2f}s")
    grid.add_row("Performance:", f"{rows_per_second:,} lignes/s")
    grid.add_row("Fichier de log:", f"{log_file}")
    
    console.print(Panel(
        grid,
        title="[bold] Conversion terminée avec succès[/bold]",
        title_align="left",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 2)
    ))
    
    console.print()
