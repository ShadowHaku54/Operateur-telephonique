# Functions - Views
import time
import sys
from os import system as osSystem
from tqdm import tqdm

from rich.console import Console
from rich.rule import Rule
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
console = Console()

from consts import TAB, MAIN_TITLE, STYLE_DEFAULT_INDEX


def effacer_ecran():
    osSystem("cls")


def lines_spaces(nb_lignes):
    for _ in range(nb_lignes):
        print("")


def processing(duree=2, largeur_barre=50, type="succes"):
    for i in range(largeur_barre + 1):
        pourcentage = int((i / largeur_barre) * 100)
        barre = "#" * i + " " * (largeur_barre - i)
        message = "\033[31mError traitement\033[0m🛑" if (type == "error") else "\033[32mSucces traitement\033[0m🟢"
        if type == "error" and i%10 == 0:
            time.sleep(0.5)
        sys.stdout.write(f"\rProcessing [{barre}] {pourcentage}/100 {message}")
        sys.stdout.flush()
        time.sleep(duree / largeur_barre)
    effacer_ligne()
    

def remonter_ligne(nb_lignes):
    effacer_ligne()
    for _ in range(nb_lignes):
        sys.stdout.write(f"\033[A")
        effacer_ligne()

def effacer_ligne():
    sys.stdout.write("\033[2K")
    sys.stdout.write("\r")
    sys.stdout.flush()


def take_value(message, mode_affichage="simple", advertissement = "", already_error=False):
    def saisie_simple(message):
        return lire(message)

    def saisie_error(message):
        nblines_to_clear = 2 + already_error
        remonter_ligne(nblines_to_clear)
        error_message(advertissement)
        return lire(message)

    actions = {
        "simple": saisie_simple,
        "error": saisie_error,
    }

    action = actions[mode_affichage]
    return action(message)

def take_choice(message, mode_affichage="simple", already_error=False, default=None):
    def saisie_simple(message):
        return ask_choice(message, default=default)

    def saisie_error(message):
        nblines_to_clear = 1 + already_error
        remonter_ligne(nblines_to_clear)
        afficher_en_couleur("Veuillez entrer un numéros parmis les options valides ❗", style="red")
        return ask_choice(message, default=default)

    actions = {
        "simple": saisie_simple,
        "error": saisie_error,
    }

    action = actions[mode_affichage]
    return action(message)


def succes_message(message):
    afficher_en_couleur(message, style="green")

def error_message(message):
    afficher_en_couleur(">>> ERROR <<<", style="bold red on black", end="")
    afficher_en_couleur(f" {message.upper()} ", style="yellow on black", end="")
    afficher_en_couleur(">>> ERROR <<<", style="bold red on black")


def afficher_tritre_principal_styler():
    titre_principal = Text(MAIN_TITLE.upper(), style="bold on red")
    console.print(Rule(titre_principal, style="cyan on black", characters="═"))

def afficher_titre_section_styler(name_section, color):
    sous_titre = Text(f"Section {name_section} ", style=f"bold on {color}")
    console.print(Rule(sous_titre, style=f"{color} on black", characters=">", align="left"))


def afficher_menu(
    title, options, title_style="bold white",
    altern_colors=("bright_yellow", "bright_green"),
    border_panel_style="bright_blue", index_style=STYLE_DEFAULT_INDEX
):

    table = Table(show_header=False, show_edge=False, padding=(0, 4))

    choices_str = set()
    len_altcol = len(altern_colors)
    
    for index, option in enumerate(options, start=1):
        color = altern_colors[index % len_altcol]
        
        table.add_row(f"[{index_style}][{index}][/{index_style}]", f"[{color}]{option}[/{color}]")
        
        choices_str.add(str(index))

    panel = Panel(
        table,
        title=f"[{title_style}]{title}[/{title_style}]",
        border_style=border_panel_style,
        padding=(1, 2),
    )

    console.print(panel, justify="center")

    return choices_str

def afficher_en_couleur(message, style="green", end='\n'):
    console.print(f"[{style}]{message}[/{style}]", end=end)

def ask_choice(message, style_sms="bold yellow", default=None):
    afficher_en_couleur(message, style_sms, end="")
    if default is not None:
        afficher_en_couleur(f" ({default})", STYLE_DEFAULT_INDEX, end="")
    saisie = input(": ")
    return default if saisie=="" else saisie

def lire(message, style_sms="bold"):
    afficher_en_couleur(message, style_sms, end="")
    return input(f"\n> {TAB}")
