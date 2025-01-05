MAIN_TITLE = " opérateur téléphonique "
PATH_DB_OPERATEUR = r"./DB/Operateurs/"
DIR_INDEX = "Index"
NUM_GENERES = 100
BOOl_DISPONIPLE = "1"
BOOL_INDISPONIBLE = "0"

MAX_CHAR_OP = 15
MIN_CHAR_OP = 3

MAX_INDEX = 99
MIN_INDEX = 10
CHAR_INDEX = 2

SPACES_TAB = 4
TAB = " "*SPACES_TAB
PROMPT_END_DEFAULT = f"\n>{TAB}"
PROMPT_END_CHOICE = ": "

STYLE_DEFAULT_INDEX = "bright_cyan"
# STYLE_DEFAULT_INPUT = "cyan"


BG_COLOR_HEXA = "on #282C34"
BG_COLOR_SYS = ""

COLOR_SECT_CLIENT = "yellow"
COLOR_SECT_GESTION = "blue"

# Clés dictionnaires
KEY_EXIST = "exist"
KEY_NOT_EXIST = "not_exist"
KEY_LENGTH_OP = "lenght_op"
KEY_LENGTH_INDEX = "lenght_index"
KEY_NONE = "none"
KEY_NOT_FOUND = "N/A"
KEY_INT_POS = "int_positif"
KEY_LENGTH_NUMB = "lenght_numero"
KEY_NOT_EXIST_NUMB = "not_exist_for_num"



# DICTIONNAIRE
ERROR_MESSAGES = {
    KEY_EXIST : "existe déjà",
    KEY_NOT_EXIST : "n'existe pas",
    KEY_LENGTH_OP : f"nombre de caractères doit être compris entre [{MIN_CHAR_OP}-{MAX_CHAR_OP}]",
    KEY_LENGTH_INDEX : f"Veuillez entrer un entier compris entre [{MIN_INDEX}-{MAX_INDEX}]",
    KEY_INT_POS : "Veuillez saisir un entier positif",
    KEY_LENGTH_NUMB : "Veuillez saisir un numéro valide",
    KEY_NOT_EXIST_NUMB : "n'est pas disponible",
    KEY_NONE : ""
}



MENUS_GESTIONNAIRE = [
    "Créer un opérateur",
    "Renommer un opérateur",
    "Lister les opérateurs et leur index",
    "Lister les numéros d’un opérateur",
    "Ajouter un nouvel index pour un opérateur existant",
    "Supprimer un index d’un opérateur",
    "Vendre un numéro",
    "Vendre du crédit à un client",
    "État de la caisse"
]
KEY_TITLE = "tilte"
KEY_OPTIONS = "options"
KEY_TITLE_STYLE = ""
KEY_ALTERN_COLORS = ""
KEY_BORDER_PANEL_STYLE = ""
KEY_INDEX_EXIST = ""


STRUCT_MENU_GESTIONNAIRE = {
    KEY_TITLE : " opérateur téléphonique ",
    KEY_OPTIONS : MENUS_GESTIONNAIRE,
    KEY_TITLE_STYLE : "bold white",
    KEY_ALTERN_COLORS : ("bright_yellow", "bright_green"),
    KEY_BORDER_PANEL_STYLE : "bright_blue",
    KEY_INDEX_EXIST : STYLE_DEFAULT_INDEX,
}
