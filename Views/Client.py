from rich.console import Console
from rich.rule import Rule
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.box import DOUBLE_EDGE, ROUNDED, ASCII, HORIZONTALS
from consts import BG_COLOR_HEXA, BOOL_BLOCKED, MENU_GESTION_CONTACT, MENU_GESTION_REPERTOIRE, MENU_CONTACT_FLITRE
from Views.Functions import formated_num
console = Console()


def barre_header(nom_operateur, fonctionnalites=""):
    style_rule = "red on bright_cyan"
    sep = '⟳'
    first_rule = Rule(style=style_rule, characters=sep)
    title = Text(f"\t{nom_operateur.upper()} OPERATORS\t", style=style_rule)
    mid_rule = Rule(title, style=style_rule)
    if fonctionnalites:
        fonc_style = Text(fonctionnalites, "bright_white on red")
        end_rule = Rule(fonc_style, style=style_rule, characters=sep, align="right")
    else:
        end_rule = Rule(style=style_rule, characters=sep)
    
    console.print(first_rule, mid_rule, end_rule)
    
def tableau_repertoire(repertoire):
    table = Table(title="Répertoire Téléphonique", title_style="bright_blue", show_lines=True, box=ROUNDED, padding=(0, 3), border_style="magenta")

    table.add_column("#", justify="center", style="cyan", no_wrap=True)
    table.add_column("Nom du Contact", justify="left", style="green")
    
    len_repertoire = len(repertoire)
    if len_repertoire > 0:
        nb_zero_before = len(str(len_repertoire))

        for i in range(len_repertoire):
            contact = repertoire[i]
            nom_contact = contact['nom_contact']
            if contact['flag'] == BOOL_BLOCKED:
                nom_contact = f"[red]{nom_contact}[/red]"

            ff_i = f"{i+1:>0{nb_zero_before}}"
            
            table.add_row(ff_i, nom_contact)
    else:
        table.add_row("N/O", "aucun contact disponible")
        
    return Panel(table, style="on black", expand=False)

def afficher_repertoire(repertoire, menu=None, title_menu="Menu/Gestion repertoire"):
    if not menu:
        menu = MENU_GESTION_REPERTOIRE
    table_rep = tableau_repertoire(repertoire)
    pan_menu = panel_menu(title_menu, menu)
    tab_main = Table(show_header=False, show_edge=False, padding=(1, 3), expand=True)
    tab_main.add_column("", vertical="bottom")
    tab_main.add_column("", vertical="bottom", justify="center")
    tab_main.add_row(pan_menu, table_rep)
    console.print(tab_main)

def afficher_repertoire_filtre(repertoire):
    afficher_repertoire(repertoire, MENU_CONTACT_FLITRE, "Menu/Gestion repertoire trié")

def dispaly_rule_sous_titre(sous_titre):
    console.print(Rule(sous_titre, style="bold yellow"))
    

def afficher_menu_contact(contact):
    style = "red" if contact["flag"] == BOOL_BLOCKED else "green"
    table_contact = Table(box=DOUBLE_EDGE, style="cyan")
    table_contact.add_column("Nom du contact", justify="center", vertical="middle")
    table_contact.add_column("Numéro(s)", justify="center")
    table_contact.add_row(
        contact["nom_contact"],
        "\n".join([formated_num(num) for num in contact["liste_nums"]]), 
        style=style
    )
    pannel_gauche = Panel(table_contact, style="on black", box=ASCII)

    table_menu = Table(title="Menu/Gestion contacts", show_header=False)
    for key, action in MENU_GESTION_CONTACT.items():
        table_menu.add_row(f"[bold]{key}[/]", action)

    panel_droit = panel_menu("Options/Menu contact", MENU_GESTION_CONTACT)

    console.print(Columns([panel_droit, pannel_gauche], padding=(2, 5), align="center"))


def panel_menu(title, options):
    title_style="bold white"
    altern_colors=("bright_yellow", "bright_green")
    border_panel_style="bright_blue"
    index_style="bright_cyan"
    
    table = Table(show_header=False, show_edge=False, padding=(0, 2))
    len_altcol = len(altern_colors)
    for index, (key, value) in enumerate(options.items(), start=1):
        color = altern_colors[index % len_altcol]
        table.add_row(
            f"[{index_style}]{key:<2}[/]  [{color}]➤[/]",
            f"[{color}]{value}[/]"
        )

    panel = Panel(
        table,
        title=f"[{title_style}]{title}[/{title_style}]",
        style=BG_COLOR_HEXA,
        border_style=border_panel_style,
        padding=(1, 2),
        expand=False,
    )

    return panel


def display_any_menu(titre, menu):
    console.print(panel_menu(titre, menu))
    

def afficher_tab_num_contact(liste_nums, flag=BOOL_BLOCKED):
    color = "red" if flag==BOOL_BLOCKED else "green"
    table = Table(show_header=False, show_edge=False, box=HORIZONTALS)
    N = len(liste_nums)
    for index in range(N):
        ff_number = f"[{color}]{formated_num(liste_nums[index])}[/]"
        table.add_row(f"([cyan]{index+1}[/]).", ff_number)

    console.print(table)


def contact_appel(numero, nom_contact=None):
    style = "green"
    if not nom_contact:
        nom_contact = "unknown"
    table_contact = Table(box=DOUBLE_EDGE, style="cyan")
    table_contact.add_column("Nom du contact", justify="center", vertical="middle")
    table_contact.add_column("Numéro", justify="center")
    table_contact.add_row(
        nom_contact,
        formated_num(numero),
        style=style
    )
    pannel = Panel(table_contact, style="on black", box=ASCII, padding=(2, 1))

    console.print(pannel, justify="center")
    
def message_appel():
    console.print("[yellow]Entrer sur D pour enregistrer un vocal ou Q pour quitter[/]", "[cyan](D)[/]", ': ', end="")