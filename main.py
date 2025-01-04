from Controllers import Operateur as OpControllers

# OpControllers.add_new_op()
OpControllers.menu_gestionnaire_interactif()
# OpControllers.use_case_getionnaire()

# OpControllers.rename_operate()

# from rich.console import Console
# from rich.panel import Panel
# from rich.table import Table
# from rich.prompt import Prompt

# def afficher_menu_minimaliste(titre, options):
#     """
#     Affiche un menu interactif minimaliste et stylisé.

#     :param titre: Titre du menu.
#     :param options: Liste des options à afficher.
#     :return: L'option choisie par l'utilisateur.
#     """
#     console = Console()

#     # Titre stylisé
#     console.print(Panel(f"[bold white]{titre}[/bold white]", border_style="bright_blue"))

#     # Menu : Tableau des options
#     table = Table.grid(expand=True)
#     table.add_column(justify="center", style="bold yellow")
#     table.add_column(justify="left", style="white")

#     for index, option in enumerate(options, start=1):
#         table.add_row(f"[{index}]", option)

#     console.print(Panel(table, border_style="bright_cyan"))

#     # Interaction utilisateur
#     choix = Prompt.ask(
#         "[bold yellow]Votre choix[/bold yellow]",
#         default="1",
#     )
#     return int(choix)

# # Exemple d'utilisation
# if __name__ == "__main__":
#     menu_options = [
#         "Ajouter un opérateur",
#         "Renommer un opérateur",
#         "Supprimer un opérateur",
#         "Voir les opérateurs",
#         "Quitter",
#     ]
#     choix = afficher_menu_minimaliste("Gestion des Opérateurs Télécom", menu_options)
#     print(f"Vous avez choisi : {menu_options[choix - 1]}")

