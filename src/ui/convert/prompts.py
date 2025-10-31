"""
Invites interactives avec Rich et Questionary
"""
import questionary
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box
from prompt_toolkit.completion import PathCompleter as PTPathCompleter
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.key_binding import KeyBindings
import os

from ...core.db_manager import ConflictAction


console = Console()


class ExcelFileValidator(Validator):
    """Validateur pour vérifier que le fichier Excel existe."""
    
    def validate(self, document):
        text = document.text.strip()
        if not text:
            return
        
        path = Path(text)
        if not path.is_absolute():
            path = Path.cwd() / path
        
        if not path.exists():
            raise ValidationError(message=f"Le chemin n'existe pas")
        
        if path.is_dir():
            raise ValidationError(message=f"C'est un dossier, pas un fichier")
        
        if path.suffix.lower() not in ['.xlsx', '.xls', '.xlsm']:
            raise ValidationError(message=f"Ce n'est pas un fichier Excel (.xlsx, .xls, .xlsm)")


def prompt_excel_file() -> Optional[Path]:
    """
    Demander à l'utilisateur de sélectionner un fichier Excel avec auto-complétion.
    Utilise une vraie auto-complétion de fichiers depuis le répertoire courant.
    
    Returns:
        Chemin du fichier sélectionné ou None si annulé
    """
    console.print(Panel(
        "[bold cyan]Sélection du fichier Excel[/bold cyan]\n\n"
        "[dim]💡 Tab pour compléter\n"
        "📁 Tab sur un dossier pour le sélectionner\n"
        f"✅ Entrée pour valider[/dim]",
        border_style="cyan",
        box=box.ROUNDED
    ))
    
    # Créer le completer avec filtrage pour Excel
    def excel_file_filter(path):
        """Filtre pour ne montrer que les fichiers Excel et les dossiers."""
        p = Path(path)
        if p.is_dir():
            return True
        return p.suffix.lower() in ['.xlsx', '.xls', '.xlsm']
    
    completer = PTPathCompleter(
        only_directories=False,
        expanduser=True,
        file_filter=excel_file_filter
    )
    
    # Key bindings pour ajouter automatiquement \ après un dossier
    kb = KeyBindings()
    
    @kb.add('tab')
    def _(event):
        r"""Tab : compléter et ajouter \ si c'est un dossier."""
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
            "🔍 Chemin du fichier Excel : ",
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
        
        # Vérifier l'extension
        if path.suffix.lower() not in ['.xlsx', '.xls', '.xlsm']:
            console.print(f"[yellow]⚠️  Le fichier ne semble pas être un fichier Excel[/yellow]")
            if not confirm_action("Voulez-vous continuer quand même ?", default=False):
                return None
        
        console.print(f"[green]✓ Fichier : {path}[/green]")
        return path
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Opération annulée[/yellow]")
        return None
    except EOFError:
        console.print("\n[yellow]⚠️  Opération annulée[/yellow]")
        return None


def prompt_database_name(default_name: str) -> Optional[str]:
    """
    Demander le nom souhaité pour la base de données avec Rich.
    
    Args:
        default_name: Nom proposé par défaut
        
    Returns:
        Nom de la base de données ou None si annulé
    """
    try:
        db_name = Prompt.ask(
            "\n[bold]💾 Nom de la base de données[/bold] ",
            default=default_name,
            console=console
        )
        
        if not db_name:
            console.print("[yellow]⚠️  Opération annulée[/yellow]")
            return None
        
        # Ajouter automatiquement l'extension .db si nécessaire
        if not db_name.endswith('.db'):
            db_name += '.db'
        
        console.print(f"[green]✓ Base de données: {db_name}[/green]")
        return db_name
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Opération annulée[/yellow]")
        return None


def prompt_select_sheets(sheets_info: List[dict]) -> Optional[List[str]]:
    """
    Demander à l'utilisateur de sélectionner les feuilles à convertir.
    
    Args:
        sheets_info: Liste des informations sur les feuilles
        
    Returns:
        Liste des noms de feuilles sélectionnées ou None si annulé
    """
    if not sheets_info:
        return None
    
    # Préparer les choix pour questionary avec checked
    choices = [
        questionary.Choice(
            title=f"{info['name']} ({info['rows']:,} lignes × {info['columns']} colonnes)",
            value=info['name'],
            checked=True  # Présélectionné par défaut
        )
        for info in sheets_info
    ]
    
    # Utiliser questionary pour la sélection multiple
    selected = questionary.checkbox(
        "📑 Sélectionnez les feuilles à convertir :",
        choices=choices
    ).ask()
    
    if selected is None:
        return None
    
    if not selected:
        console.print("[yellow]⚠️  Aucune feuille sélectionnée[/yellow]")
        return None
    
    console.print(f"[green]✓ {len(selected)} feuille(s) sélectionnée(s)[/green]")
    return selected


def prompt_conflict_action(table_name: str, existing_rows: int) -> Optional[ConflictAction]:
    """
    Demander l'action à effectuer en cas de conflit de table existante.
    
    Args:
        table_name: Nom de la table en conflit
        existing_rows: Nombre de lignes dans la table existante
        
    Returns:
        Action choisie ou None si annulé
    """
    console.print()
    console.print(Panel(
        f"[bold yellow]⚠️  Conflit détecté[/bold yellow]\n\n"
        f"La table [cyan]'{table_name}'[/cyan] existe déjà avec "
        f"[yellow]{existing_rows:,}[/yellow] lignes.\n\n"
        f"[dim]Que souhaitez-vous faire ?[/dim]",
        border_style="yellow",
        box=box.HEAVY
    ))
    
    # Utiliser questionary.select pour une navigation au clavier
    action = questionary.select(
        "Choisissez une action :",
        choices=[
            questionary.Choice("🔴 Écraser - Supprimer et recréer la table", value="overwrite"),
            questionary.Choice("➕ Ajouter - Ajouter les données à la table existante", value="append"),
            questionary.Choice("⊘ Ignorer - Passer à la feuille suivante", value="skip"),
            questionary.Choice("✗ Annuler - Arrêter l'opération complète", value="cancel")
        ],
        default="append"
    ).ask()
    
    if action is None:
        return "cancel"
    
    # Messages de confirmation
    messages = {
        "overwrite": "[red]⚠️  La table sera écrasée[/red]",
        "append": "[green]✓ Les données seront ajoutées[/green]",
        "skip": "[yellow]⊘ Feuille ignorée[/yellow]",
        "cancel": "[dim]✗ Opération annulée[/dim]"
    }
    
    console.print(messages[action])
    return action


def prompt_new_database_name(original_name: str) -> Optional[str]:
    """
    Demander un nouveau nom pour la base de données avec Rich.
    
    Args:
        original_name: Nom d'origine de la base
        
    Returns:
        Nouveau nom ou None si annulé
    """
    # Suggérer un nom avec un suffixe
    base_name = original_name.replace('.db', '')
    suggestion = f"{base_name}_new.db"
    
    console.print(Panel(
        "[bold cyan]Nouveau nom de base de données[/bold cyan]\n\n"
        f"[dim]Le fichier original: {original_name}[/dim]",
        border_style="cyan",
        box=box.ROUNDED
    ))
    
    try:
        new_name = Prompt.ask(
            "\n[bold]💾 Nouveau nom[/bold]",
            default=suggestion,
            console=console
        )
        
        if not new_name:
            console.print("[yellow]⚠️  Opération annulée[/yellow]")
            return None
        
        if not new_name.endswith('.db'):
            new_name += '.db'
        
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


def prompt_database_exists_action() -> Optional[str]:
    """
    Demander l'action à effectuer si la base de données existe déjà.
    
    Returns:
        Action choisie ('use', 'overwrite', 'rename') ou None si annulé
    """
    console.print()
    console.print(Panel(
        "[bold yellow]⚠️ Base de données existante[/bold yellow]\n\n"
        "[dim]La base de données existe déjà. Que souhaitez-vous faire ?[/dim]",
        border_style="yellow",
        box=box.HEAVY
    ))
    
    # Utiliser questionary.select pour une navigation au clavier
    action = questionary.select(
        "Choisissez une action :",
        choices=[
            questionary.Choice("🔄 Utiliser - Utiliser la base existante (gérer les conflits table par table)", value="use"),
            questionary.Choice("🗑️ Écraser - Supprimer complètement et recréer la base", value="overwrite"),
            questionary.Choice("📝 Renommer - Créer une nouvelle base avec un autre nom", value="rename"),
            questionary.Choice("✗ Annuler - Arrêter l'opération", value="cancel")
        ]
    ).ask()
    
    if action is None:
        return "cancel"
    
    messages = {
        "use": "[green]✓ Utilisation de la base existante[/green]",
        "overwrite": "[red]⚠️  La base sera écrasée[/red]",
        "rename": "[cyan]✓ Création d'une nouvelle base[/cyan]",
        "cancel": "[dim]✗ Opération annulée[/dim]"
    }
    
    console.print(messages[action])
    return action


def prompt_chunk_size(default: int = 10000) -> int:
    """
    Demander la taille des lots (chunks) pour l'insertion avec Rich.
    
    Args:
        default: Valeur par défaut proposée
        
    Returns:
        Taille des lots choisie
    """
    console.print(Panel(
        "[bold cyan]Configuration avancée[/bold cyan]\n\n"
        "[dim]Taille des chunks pour l'insertion par batch[/dim]\n"
        "[dim]Valeurs recommandées: 1000-50000[/dim]",
        border_style="cyan",
        box=box.ROUNDED
    ))
    
    try:
        size = IntPrompt.ask(
            "\n[bold]📦 Taille des chunks[/bold]",
            default=default,
            console=console
        )
        
        if size <= 0:
            console.print("[yellow]⚠️  Valeur invalide, utilisation de la valeur par défaut[/yellow]")
            return default
        
        console.print(f"[green]✓ Taille des chunks: {size:,}[/green]")
        return size
        
    except (KeyboardInterrupt, ValueError):
        console.print("\n[yellow]⚠️  Utilisation de la valeur par défaut[/yellow]")
        return default
