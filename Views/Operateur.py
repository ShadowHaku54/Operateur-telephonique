# Operateur - Views

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.padding import Padding
from rich.text import Text
from rich.box import ASCII

from consts import BOOL_DISPO, STYLE_DEFAULT_INDEX
from consts import BG_COLOR_HEXA, STYLE_DISPO, STYLE_NOT_DISPO
from Views.Functions import max_col_rows_terminal




console = Console()

def afficher_operateurs(struct_op):
    title = Text("Liste des opérateurs", style="bold red")
    table = Table(title=title, show_lines=True, style="red", title_justify="center")

    table.add_column("Opérateur", style="bold cyan")
    table.add_column("Index", style="bold magenta")

    for operateur, index_list in struct_op.items():
        table.add_row(operateur, ", ".join(index_list))
    panel = Panel(
        table,
        expand=False,
        border_style="cyan"
    )
    padded_panel = Padding(panel, (1, 0))
    console.print(padded_panel, style=BG_COLOR_HEXA, justify="center")


def tableau_numeros(liste_nums, show_lines_box=True):
    available_columns = max_col_rows_terminal(col_width=22, limite_marge_col=0, limite_marge_row=8)[0]
    
    formatted_data = [
        liste_nums[i : i + available_columns]
        for i in range(0, len(liste_nums), available_columns)
    ]

    altern_colors_lines = (BG_COLOR_HEXA, "on black")
    altern = 0

    table = Table(title="Liste des numéros disponibles",expand=True, show_lines=show_lines_box, box=ASCII)

    for _ in range(available_columns):
        table.add_column("Numéros 📞", justify="center")

    i = 0
    for row in formatted_data:
        row_numbers = []
        for numero, etat in row:
            i += 1
            style_cell = STYLE_DISPO if etat == BOOL_DISPO else STYLE_NOT_DISPO
            numero_format = f"{numero[:2]} {numero[2:5]} {numero[5:7]} {numero[7:]}"
            format_cell = Text()
            format_cell.append('({:03}) '.format(i), STYLE_DEFAULT_INDEX)
            format_cell.append(numero_format, style_cell)
            row_numbers.append(format_cell)
        table.add_row(*row_numbers, style=altern_colors_lines[altern])
        altern = 1 - altern


    panel = Panel(
        table,
        title_align="left",
        border_style="cyan",
    )

    padded_panel = Padding(panel, (1, 0))

    console.print(padded_panel, justify="center", style=BG_COLOR_HEXA)


def etat_caisse(caisse_ops, title="Etat de la caisse", subtitle=""):
    table = Table(title=title, title_style="bold yellow", show_lines=True, style="bright_yellow")
    table.add_column("Opérateur", justify="left", style="blue", no_wrap=True)
    table.add_column("Crédit Vendu", justify="right", style="green")
    table.add_column("Numéros Vendus", justify="right", style="magenta")

    for operateur, details in caisse_ops.items():
        table.add_row(
            operateur,
            str(details["sell_credit"]),
            str(details["sell_num"])
        )
    
    pannel = Panel(
        table,
        subtitle=f"[bright_cyan]{subtitle}[/]",
        expand=False,
        border_style="cyan"
    )
    
    marge = Padding(
        pannel,
        (2, 0),
    )
    console.print(marge, style=BG_COLOR_HEXA, justify="center")