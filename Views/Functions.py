from shutil import get_terminal_size
import time
import sys
import pyfiglet

from rich.console import Console
from rich.rule import Rule
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
console = Console()

from consts import TAB, MAIN_TITLE, STYLE_DEFAULT_INDEX, DEFAULT_LINES_SPACES, PROCESSING_COUPURE, BG_COLOR_HEXA, WARNING_STYLE


def effacer_ecran():
    print("\033c", end="")


def lines_spaces(nb_lignes=DEFAULT_LINES_SPACES):
    for _ in range(nb_lignes):
        print("")

def max_col_rows_terminal(terminal_size=get_terminal_size(), col_width=1, limite_marge_col=0, limite_marge_row=0):
    terminal_width = terminal_size.columns
    terminal_height = terminal_size.lines

    available_columns = max(1, (terminal_width - limite_marge_col) // col_width)
    rows_per_page = max(1, terminal_height - limite_marge_row)

    return available_columns, rows_per_page


def processing(duree=1, remplissage=0.3, mode="succes", go="go"):
    largeur_barre = int(remplissage * max_col_rows_terminal()[0])
    message, coupure, range_go = processing_sous_func(mode, go, largeur_barre)
    for i in range_go:
        pourcentage = int((i / largeur_barre) * 100)
        barre = "#" * i + " " * (largeur_barre - i)
        if i%5 == 0:
            time.sleep(coupure)
        sys.stdout.write(f"\rProcessing [{barre}] {pourcentage}/100 {message}")
        sys.stdout.flush()
        time.sleep(duree / largeur_barre)
    effacer_ligne()

def processing_sous_func(mode, go, largeur_barre):
    message = coupure = range_go = None
    
    if mode == "error":
        message = "\033[31mError traitement\033[0m🛑"
        coupure = PROCESSING_COUPURE
    elif mode == "succes":
        message = "\033[32mSucces traitement\033[0m🟢"
        coupure = 0

    if go=="go":
        range_go = range(0, largeur_barre+1)
    elif go=="back":
        range_go = range(largeur_barre+1, 0, -1)

    return message, coupure, range_go

def remonter_ligne(nb_lignes):
    effacer_ligne()
    for _ in range(nb_lignes):
        sys.stdout.write("\033[A")
        effacer_ligne()

def effacer_ligne():
    sys.stdout.write("\033[2K")
    sys.stdout.write("\r")
    sys.stdout.flush()

def continuer(sms="Appuyer sur [Enter] pour retourner"):
    console.input(f"\n[blue on black]{sms}...[/]")
    processing(go="back")

def take_value(message, mode_affichage="simple", advertissement = "", already_error=False):
    def saisie_simple(message):
        return lire(message)

    def saisie_error(message):
        nblines_to_clear = 2 + DEFAULT_LINES_SPACES + already_error
        remonter_ligne(nblines_to_clear)
        error_message(advertissement)
        return lire(message)

    actions = {
        "simple": saisie_simple,
        "error": saisie_error,
    }

    action = actions[mode_affichage]
    return action(message)

def take_choice(message="Votre choix", mode_affichage="simple", already_error=False, default=None, choices=None):
    def saisie_simple(message):
        return ask_choice(message, default=default, choices=choices)

    def saisie_error(message):
        nblines_to_clear = 1 + DEFAULT_LINES_SPACES + already_error
        remonter_ligne(nblines_to_clear)
        error_message_simple("Veuillez entrer un choix parmi les options disponibles ❗")
        return ask_choice(message, default=default, choices=choices)

    actions = {
        "simple": saisie_simple,
        "error": saisie_error,
    }

    action = actions[mode_affichage]
    return action(message)

def take_password(message="Entrez le mot de passe", mode_affichage="simple", already_error=False, default=None, adv_sms=""):
    def saisie_simple(message):
        return ask_password(message, default=default)

    def saisie_error(message):
        nblines_to_clear = 1 + DEFAULT_LINES_SPACES + already_error
        remonter_ligne(nblines_to_clear)
        error_message_simple(adv_sms)
        return ask_password(message, default=default)

    actions = {
        "simple": saisie_simple,
        "error": saisie_error,
    }

    action = actions[mode_affichage]
    return action(message)


def succes_message(message):
    afficher_en_couleur(message, style="bold bright_white on green")

def error_message(message):
    afficher_en_couleur(">>> ERROR <<<", style="bold red on black", end="")
    afficher_en_couleur(f" {message.upper()} ", style="yellow on black", end="")
    afficher_en_couleur(">>> ERROR <<<", style="bold red on black")


def warning_message(message, end="\n"):
    afficher_en_couleur(message, WARNING_STYLE, end=end)

def error_message_simple(message):
    afficher_en_couleur(message, style="red on black")

def afficher_tritre_principal_styler():
    effacer_ecran()
    titre_principal = Text(MAIN_TITLE.upper(), style="bold on red")
    console.print(Rule(titre_principal, style="cyan on black", characters="═"))

def afficher_titre_section_styler(name_section, color):
    sous_titre = Text(f"Section {name_section} ", style=f"bold #ffffff on {color}")
    console.print(Rule(sous_titre, style=f"{color} on black", characters=">", align="left"))

def afficher_titre_operation_styler(name_operation):
    titre_operation = Text(name_operation.upper(), style="bold magenta on bright_white")
    console.print(Rule(titre_operation, style="magenta on black", align="right"))

def afficher_menu(
    title, options, title_style=f"bold white",
    altern_colors=("bright_yellow", "bright_green"),
    border_panel_style="bright_blue", index_style="bright_cyan"
):

    Taille = len(options)
    decalage = len(str(Taille))
    table = Table(show_header=False, show_edge=False, padding=(0, 3))

    len_altcol = len(altern_colors)
    
    for index, option in enumerate(options, start=1):
        color = altern_colors[index % len_altcol]
        index_ff = "{:>0{}}".format(index, decalage)
        table.add_row(f"[{index_style}]{index_ff}[/] [{color}]➤[/]", f"[{color}]{option}[/{color}]")
        

    panel = Panel(
        table,
        title=f"[{title_style}]{title}[/{title_style}]",
        border_style=border_panel_style,
        padding=(1, 2),
        style=BG_COLOR_HEXA,
    )

    console.print(panel, justify="center")
    lines_spaces()


def afficher_en_couleur(message, style="green", end='\n'):
    console.print(f"[{style}]{message}[/]", end=end)

def ask_choice(message, style_sms="bold yellow", default=None, choices=None):
    afficher_en_couleur(message, style_sms, end="")
    if choices is not None:
        afficher_en_couleur(f" [{'/'.join(choices)}]", style="green", end="")
    if default is not None:
        afficher_en_couleur(f" ({default})", STYLE_DEFAULT_INDEX, end="")
    saisie = input(": ").strip()
    lines_spaces()
    return default if default and saisie=="" else saisie

def lire(message, style_sms="bold bright_magenta"):
    afficher_en_couleur(f"{message}\n> {TAB}", style_sms, end="")
    user_input = input().strip()
    lines_spaces()
    return user_input


def formated_num(numero):
    return f"{numero[:2]} {numero[2:5]} {numero[5:7]} {numero[7:]}"

def reforme_num(numero):
    return numero.replace(' ', '', count=3)

def ask_password(sms, default=None):
    message_style = Text(sms, "bold bright_yellow")
    mdp = Prompt.ask(
        message_style,
        password=True,
        default=default,
    )
    lines_spaces()
    return mdp

def take_login_and_password(sms1="Entrer le login/numéro", sms2="Entrer le mot de passe/code pin ", mode_affichage="simple", already_error=False, adv="login ou mot de passe incorrect"):
    def saisie_simple(sms1, sms2):
        value = take_value(sms1)
        password = take_password(sms2)
        return value, password

    def saisie_error(sms1, sms2):
        nblines_to_clear = 3 + DEFAULT_LINES_SPACES*2 + already_error
        remonter_ligne(nblines_to_clear)
        error_message(adv)
        return saisie_simple(sms1, sms2)

    actions = {
        "simple": saisie_simple,
        "error": saisie_error,
    }

    action = actions[mode_affichage]
    return action(sms1, sms2)

def take_numero(sms1="Entrer le nom d'opérateur", sms2="Entrer le numéro", mode_affichage="simple", already_error=False, adv="Numéro non acrédité"):
    def saisie_simple(sms1, sms2):
        value = take_value(sms1)
        password = take_password(sms2)
        return value, password

    def saisie_error(sms1, sms2):
        nblines_to_clear = 3 + DEFAULT_LINES_SPACES*2 + already_error
        remonter_ligne(nblines_to_clear)
        error_message(adv)
        return saisie_simple(sms1, sms2)

    actions = {
        "simple": saisie_simple,
        "error": saisie_error,
    }

    action = actions[mode_affichage]
    return action(sms1, sms2)

def display_aurevoir():

    message_ascii = pyfiglet.figlet_format("Au Revoir!")
    lines = message_ascii.split("\n")
    console.print("\n")
    for line in lines:
        console.print(f"[bold magenta]{line}[/bold magenta]", justify='center', style="on black")
        time.sleep(0.2)

    console.print("\n💫 [bold cyan]À bientôt ![/bold cyan] 💫", justify="center")
    time.sleep(2)
    effacer_ecran()