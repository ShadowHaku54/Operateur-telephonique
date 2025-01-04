# Functions - Controllers
from datetime import datetime
from Views.Functions import (
    afficher_titre_section_styler, 
    afficher_tritre_principal_styler,
    effacer_ecran,
    afficher_en_couleur
)
from consts import ERROR_MESSAGES, KEY_NOT_FOUND


def est_un_entierPos(value):
    return value.isdigit()


def get_date():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def get_error_message(key):
    if key in ERROR_MESSAGES:
        return ERROR_MESSAGES[key]
    return ERROR_MESSAGES[KEY_NOT_FOUND]

    