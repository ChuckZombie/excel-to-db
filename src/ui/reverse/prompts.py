"""
Invites interactives pour la conversion SQLite vers Excel
"""
import questionary
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import box
from prompt_toolkit.completion import PathCompleter as PTPathCompleter
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.key_binding import KeyBindings
import os


console = Console()


def prompt_database_file() -> Optional[Path]:
    """
    Demander à l'utilisateur de sélectionner un fichier SQLite avec auto-complétion.
    
    Returns:
        Chemin du fichier sélectionné ou None si annulé
    """
    console.print(Panel(
        "[bold cyan]Sélection de la base de données SQLite[/bold cyan]\n\n"
        "[dim]💡 Tab pour compléter\n"
        "📁 Tab sur un dossier pour le sélectionner\n"
        f"✅ Entrée pour valider[/dim]",
        border_style="cyan",
        box=box.ROUNDED
    ))
    
    # Créer le completer avec filtrage pour les fichiers de base de données
    def db_file_filter(path):
        """Filtre pour ne montrer que les fichiers de base de données et les dossiers."""
        p = Path(path)
        if p.is_dir():
            return True
        return p.suffix.lower() in ['.db', '.sqlite', '.sqlite3']
    
    completer = PTPathCompleter(
        only_directories=False,
        expanduser=True,
        file_filter=db_file_filter
    )
    
    # Key bindings pour ajouter automatiquement \ après un dossier
    kb = KeyBindings()
    
    @kb.add('tab')
    def _(event):
        """Tab : compléter et ajouter \\ si c'est un dossier."""
        buff = event.current_buffer
        
        # Si on a une complétion en cours, appliquer la première
        if buff.complete_state:
            completion = buff.complete_state.current_completion
            if completion:
                buff.apply_completion(completion)
                
                # Vérifier si le texte complet est un dossier
                text = buff.text
                path = Path(text) if Path(text).is_absolute() else Path.cwd() / text
                
                # Si c'est un dossier et ne se termine pas déjà par un séparateur
                if path.exists() and path.is_dir() and not text.endswith(os.sep):
                    buff.insert_text(os.sep)
                    # Relancer la complétion pour montrer le contenu du dossier
                    buff.start_completion(select_first=False)
            else:
                buff.complete_next()
        else:
            # Démarrer la complétion
            buff.start_completion(select_first=True)
    
    try:
        file_path = prompt(
            "🔍 Chemin de la base de données : ",
            completer=completer,
            complete_while_typing=False,
            key_bindings=kb,
        ).strip()
        
        if not file_path:
            console.print("[yellow]⚠️  Opération annulée[/yellow]")
            return None
        
        # Convertir en Path
        path = Path(file_path)
        if not path.is_absolute():
            path = Path.cwd() / path
        
        # Vérifier que le fichier existe
        if not path.exists():
            console.print(f"[red]✗ Le fichier n'existe pas[/red]")
            return None
        
        # Vérifier que c'est bien un fichier
        if not path.is_file():
            console.print(f"[red]✗ Ce n'est pas un fichier[/red]")
            return None
        
        console.print(f"[green]✓ Base de données : {path}[/green]")
        return path
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Opération annulée[/yellow]")
        return None
    except EOFError:
        console.print("\n[yellow]⚠️  Opération annulée[/yellow]")
        return None


def prompt_excel_name(default_name: str) -> Optional[str]:
    """
    Demander le nom souhaité pour le fichier Excel avec Rich.
    
    Args:
        default_name: Nom proposé par défaut
        
    Returns:
        Nom du fichier Excel ou None si annulé
    """
    try:
        excel_name = Prompt.ask(
            "\n[bold]📊 Nom du fichier Excel[/bold] ",
            default=default_name,
            console=console
        )
        
        if not excel_name:
            console.print("[yellow]⚠️  Opération annulée[/yellow]")
            return None
        
        # Ajouter automatiquement l'extension .xlsx si nécessaire
        if not excel_name.endswith('.xlsx'):
            excel_name += '.xlsx'
        
        console.print(f"[green]✓ Fichier Excel: {excel_name}[/green]")
        return excel_name
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Opération annulée[/yellow]")
        return None


def prompt_select_tables(tables_info: List[dict]) -> Optional[List[str]]:
    """
    Demander à l'utilisateur de sélectionner les tables à exporter.
    
    Args:
        tables_info: Liste des informations sur les tables
        
    Returns:
        Liste des noms de tables sélectionnées ou None si annulé
    """
    if not tables_info:
        return None
    
    # Préparer les choix pour questionary avec checked
    choices = [
        questionary.Choice(
            title=f"{info['name']} ({info['rows']:,} lignes × {info['columns']} colonnes)",
            value=info['name'],
            checked=True  # Présélectionné par défaut
        )
        for info in tables_info
    ]
    
    # Utiliser questionary pour la sélection multiple
    selected = questionary.checkbox(
        "📊 Sélectionnez les tables à exporter :",
        choices=choices
    ).ask()
    
    if selected is None:
        return None
    
    if not selected:
        console.print("[yellow]⚠️  Aucune table sélectionnée[/yellow]")
        return None
    
    console.print(f"[green]✓ {len(selected)} table(s) sélectionnée(s)[/green]")
    return selected


def prompt_excel_exists_action() -> Optional[str]:
    """
    Demander l'action à effectuer si le fichier Excel existe déjà.
    
    Returns:
        Action choisie ('overwrite', 'rename', 'cancel') ou None si annulé
    """
    console.print()
    console.print(Panel(
        "[bold yellow]⚠️ Fichier Excel existant[/bold yellow]\n\n"
        "[dim]Le fichier Excel existe déjà. Que souhaitez-vous faire ?[/dim]",
        border_style="yellow",
        box=box.HEAVY
    ))
    
    # Utiliser questionary.select pour une navigation au clavier
    action = questionary.select(
        "Choisissez une action :",
        choices=[
            questionary.Choice("🗑️ Écraser - Remplacer le fichier existant", value="overwrite"),
            questionary.Choice("📝 Renommer - Créer un nouveau fichier avec un autre nom", value="rename"),
            questionary.Choice("✗ Annuler - Arrêter l'opération", value="cancel")
        ]
    ).ask()
    
    if action is None:
        return "cancel"
    
    messages = {
        "overwrite": "[red]⚠️  Le fichier sera écrasé[/red]",
        "rename": "[cyan]✓ Création d'un nouveau fichier[/cyan]",
        "cancel": "[dim]✗ Opération annulée[/dim]"
    }
    
    console.print(messages[action])
    return action


def prompt_new_excel_name(original_name: str) -> Optional[str]:
    """
    Demander un nouveau nom pour le fichier Excel avec Rich.
    
    Args:
        original_name: Nom d'origine du fichier
        
    Returns:
        Nouveau nom ou None si annulé
    """
    # Suggérer un nom avec un suffixe
    base_name = original_name.replace('.xlsx', '')
    suggestion = f"{base_name}_new.xlsx"
    
    console.print(Panel(
        "[bold cyan]Nouveau nom de fichier Excel[/bold cyan]\n\n"
        f"[dim]Le fichier original: {original_name}[/dim]",
        border_style="cyan",
        box=box.ROUNDED
    ))
    
    try:
        new_name = Prompt.ask(
            "\n[bold]📊 Nouveau nom[/bold]",
            default=suggestion,
            console=console
        )
        
        if not new_name:
            console.print("[yellow]⚠️  Opération annulée[/yellow]")
            return None
        
        if not new_name.endswith('.xlsx'):
            new_name += '.xlsx'
        
        console.print(f"[green]✓ Nouveau nom: {new_name}[/green]")
        return new_name
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Opération annulée[/yellow]")
        return None


def confirm_action(message: str, default: bool = False) -> bool:
    """
    Demander une confirmation à l'utilisateur avec Rich.
    
    Args:
        message: Message de confirmation
        default: Valeur par défaut
        
    Returns:
        True si confirmé, False sinon
    """
    try:
        return Confirm.ask(
            f"[bold cyan]❓ {message}[/bold cyan]",
            default=default,
            console=console
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Opération annulée[/yellow]")
        return False
