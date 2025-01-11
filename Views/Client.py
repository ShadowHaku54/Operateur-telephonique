from rich.console import Console
from rich.rule import Rule
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
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