# Operateur - Views

from shutil import get_terminal_size
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.padding import Padding
from rich.text import Text
from rich.box import ASCII

from consts import BOOl_DISPONIPLE, STYLE_DEFAULT_INDEX
from consts import BG_COLOR_SYS, BG_COLOR_HEXA

from os import system



console = Console()

def max_col_rows_terminal(terminal_size=get_terminal_size(), col_width=0, limite_marge_col=0, limite_marge_row=0):
    terminal_width = terminal_size.columns
    terminal_height = terminal_size.lines

    available_columns = max(1, (terminal_width - limite_marge_col) // col_width)
    rows_per_page = max(1, terminal_height - limite_marge_row)

    return available_columns, rows_per_page

def tableau_deroulant_inteactif(liste_nums, show_lines_box=True):
    system(f"color {BG_COLOR_SYS}")
    terminal_size = get_terminal_size()
    available_columns, rows_per_page = max_col_rows_terminal(terminal_size, col_width=22, limite_marge_col=10, limite_marge_row=8)
    if show_lines_box:
        rows_per_page //= 2

    liste_nums.sort()
    len_liste_num = len(liste_nums)
    formatted_data = [
        liste_nums[i : i + available_columns]
        for i in range(0, len_liste_num, available_columns)
    ]
    
    len_formdata = len(formatted_data)
    
    total_pages = (len_formdata + rows_per_page - 1) // rows_per_page
    start_row = 0
    
    altern_colors_lines = ("on #535A6A", "on black")
    altern = 0
    
    while True:
        table = Table(title="Liste des numéros disponibles",expand=True, show_lines=show_lines_box, box=ASCII, style=BG_COLOR_HEXA)

        for _ in range(available_columns):
            table.add_column("Numéros 📞", justify="center")

        i = start_row * available_columns
        for row in formatted_data[start_row : start_row + rows_per_page]:
            row_numbers = []
            for numero, etat in row:
                i += 1
                style_cell = "bold green" if etat == BOOl_DISPONIPLE else "bold bright_red"
                numero_format = f"{numero[:2]} {numero[2:5]} {numero[5:7]} {numero[7:]}"
                format_cell = Text()
                format_cell.append('({:03}) '.format(i), STYLE_DEFAULT_INDEX)
                format_cell.append(numero_format, style_cell)
                row_numbers.append(format_cell)
            table.add_row(*row_numbers, style=altern_colors_lines[altern])
            altern = 1 - altern

        current_page = (start_row // rows_per_page) + 1

        panel = Panel(
            table,
            title=f"Page {current_page}/{total_pages}",
            title_align="left",
            border_style="cyan",
            style=BG_COLOR_HEXA
        )

        padded_panel = Padding(panel, (0, 4, 0, 4), style=BG_COLOR_HEXA)

        console.print(padded_panel)

        user_input = console.input(
            "[cyan](S)uivant , (P)récedent, (I)nfos, (C)hoisir, (Q)uitter: [/cyan]"
        ).strip().lower()

        if user_input == "s" and start_row + rows_per_page < len(formatted_data):
            start_row += rows_per_page
        elif user_input == "p" and start_row - rows_per_page >= 0:
            start_row -= rows_per_page
        elif user_input == "q":
            break
        else:
            console.print("[bold red]Option invalide. Réessayer.[/]")

