"""
Affichage des données avec Rich - Version améliorée
Fonctions d'affichage communes aux deux modes (convert et reverse)
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from typing import Dict, Optional

# Console avec thème personnalisé
console = Console()


def clear_screen():
    """Effacer l'écran pour une navigation fluide entre les écrans."""
    console.clear()


def show_error(message: str, error: Optional[Exception] = None) -> None:
    """
    Afficher un message d'erreur (version améliorée).
    
    Args:
        message: Message d'erreur principal
        error: Exception optionnelle pour plus de détails
    """
    error_content = Text()
    error_content.append("❌ ", style="bold red")
    error_content.append(message, style="bold red")
    
    if error:
        error_content.append("\n\n", style="")
        error_content.append("Détails techniques:\n", style="yellow")
        error_content.append(str(error), style="dim")
    
    panel = Panel(
        error_content,
        title="[bold red]ERREUR[/bold red]",
        border_style="red",
        box=box.HEAVY,
        padding=(1, 2)
    )
    
    console.print()
    console.print(panel)
    console.print()


def show_warning(message: str) -> None:
    """
    Afficher un avertissement (version améliorée).
    
    Args:
        message: Message d'avertissement
    """
    warning_panel = Panel(
        Text.from_markup(f"⚠️  {message}"),
        border_style="yellow",
        box=box.ROUNDED,
        padding=(0, 1)
    )
    console.print(warning_panel)


def show_info(message: str) -> None:
    """
    Afficher un message d'information (version améliorée).
    
    Args:
        message: Message d'information
    """
    info_text = Text()
    info_text.append("ℹ️  ", style="bold blue")
    info_text.append(message, style="blue")
    console.print(info_text)


def show_success(message: str) -> None:
    """
    Afficher un message de succès (version améliorée).
    
    Args:
        message: Message de succès
    """
    success_text = Text()
    success_text.append("✓ ", style="bold green")
    success_text.append(message, style="green")
    console.print(success_text)


def show_database_stats(stats: Dict) -> None:
    """
    Afficher les statistiques d'une base de données (version améliorée).
    
    Args:
        stats: Dictionnaire contenant les statistiques de la base de données
    """
    console.print()
    
    # En-tête avec le chemin de la base de données dans un Panel
    console.print(Panel(
        f"📁 {stats['path']}",
        title="[bold]Statistiques[/bold]",
        title_align="left",
        border_style="dim",
        box=box.ROUNDED
    ))
    
    # Créer une table pour afficher les statistiques par table
    table = Table(
        show_header=True,
        header_style="bold white on blue",
        border_style="bright_blue",
        row_styles=["", "dim"],
        box=box.ROUNDED,
        expand=True,
        show_footer=True
    )
    
    table.add_column("Table", style="cyan")
    table.add_column("Lignes", justify="right", style="yellow")
    table.add_column("Colonnes", justify="right", style="blue")
    table.add_column("Taille estimée", justify="right", style="magenta")
    
    total_rows = 0
    for table_info in stats['tables']:
        # Estimer la taille approximative par table
        estimated_size = (table_info['rows'] * table_info['columns'] * 100) / (1024 * 1024)
        size_str = f"{estimated_size:.2f} MB" if estimated_size > 0.01 else "< 0.01 MB"
        
        table.add_row(
            table_info['name'],
            f"{table_info['rows']:,}",
            str(table_info['columns']),
            size_str
        )
        total_rows += table_info['rows']
    
    # Ajouter une ligne de pied de page avec les totaux
    table.columns[0].footer = Text("TOTAL", style="bold white")
    table.columns[1].footer = Text(f"{total_rows:,}", style="bold yellow")
    table.columns[2].footer = Text(f"{stats['tables_count']} tables", style="bold blue")
    table.columns[3].footer = Text(stats['size_formatted'], style="bold magenta")
    
    console.print(table)
