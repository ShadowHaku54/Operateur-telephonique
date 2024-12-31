from consts import TAB, ANSI_FONDS, ANSI_COULEURS, ANSI_STYLE
from tqdm import tqdm
import time
import sys
import os

def lire(sms):
    print(sms)
    return input(f">{TAB}")

def lines_spaces(nb_lignes):
    for _ in range(nb_lignes):
        print("")

def styliser_texte(texte, couleur="reset", style=None, fond=None):
    
    sequences = []
    if couleur in ANSI_COULEURS:
        sequences.append(ANSI_COULEURS[couleur])
    if style in ANSI_STYLE:
        sequences.append(ANSI_STYLE[style])
    if fond in ANSI_FONDS:
        sequences.append(ANSI_FONDS[fond])

    if not sequences:
        return texte

    ansi_seq = "\033[" + ";".join(sequences) + "m"
    reset_seq = "\033[0m"

    return f"{ansi_seq}{texte}{reset_seq}"


def effet_chargement_masque(duree=5):
    for _ in tqdm(range(100), desc="Chargement", ncols=50, bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} [{elapsed}]"):
        time.sleep(duree / 100)        
        
def processing(duree=2, largeur_barre=50, type="succes"):
    for i in range(largeur_barre + 1):
        pourcentage = int((i / largeur_barre) * 100)
        barre = "#" * i + " " * (largeur_barre - i)
        message = (f"{styliser_texte("Error traitement", "rouge")}🛑" if (type == "error") else f"{styliser_texte("Succes traitement", "vert")}🟢")
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
    
# import pyfiglet
# print(pyfiglet.figlet_format("Bonjour!"))

# from rich.console import Console
# from rich.prompt import Prompt

# console = Console()

# console.print("[bold cyan]Bienvenue dans l'application de gestion![/bold cyan]")
# nom_operateur = Prompt.ask("[green]Entrez le nom de l'opérateur[/green]", default="Opérateur X")
# console.print(f"Vous avez entré : [bold]{nom_operateur}[/bold]")

# from rich.logging import RichHandler
# import logging

# logging.basicConfig(level="INFO", handlers=[RichHandler()])
# logger = logging.getLogger("rich")

# logger.info("Information importante")
# logger.warning("Avertissement")
# logger.error("Erreur critique")

# from rich.tree import Tree

# tree = Tree("Racine")
# branche1 = tree.add("Branche 1")
# branche1.add("Feuille 1")
# branche1.add("Feuille 2")
# branche2 = tree.add("Branche 2")
# branche2.add("Feuille 3")

# from rich.console import Console
# console = Console()
# console.print(tree)

def succes_message(message):
    styliser_texte(message, "vert")

def error_message(message):
    styliser_texte(message, "rouge")