MAIN_TITLE = " opérateur téléphonique "
PATH_DB_OPERATEURS = r"./DB/Operateurs/"
FILE_GESTIONNAIRES = r"./DB/Gestionnaires.txt"
PATH_DB_CLIENTS = r"./DB/Clients/"
FILE_CAISSE = "transactions.txt"
FILE_REGISTRE = "registre.txt"
FILE_INFO = "infos.txt"
FILE_CONTACTS = "contacts.txt"
DIR_INDEX = "Index"
NUM_GENERES = 100
BOOL_DISPO = "1"
BOOL_NOT_DISPO = "0"
STYLE_DISPO = "bold bright_green"
STYLE_NOT_DISPO = "bold bright_red"

DEFAULT_LINES_SPACES = 1

USER_GESTIONNAIRE = "Gestionnaire"
USER_CLIENT = "Client"
COLOR_USER_GESTION = "yellow"
COLOR_SECT_CLIENT = "red"

MAX_CHAR_DEFAULT = 15
MIN_CHAR_DEFAULT = 3
PROCESSING_COUPURE = 0.36
TIME_LECTURE_UNIQUE = 6

CODE_PIN_DEFAULT = "1234"
LENGTH_CODE_PIN = 4
MAX_INDEX = 99
MIN_INDEX = 10
CHAR_INDEX = 2

SPACES_TAB = 4
TAB = " "*SPACES_TAB

STYLE_DEFAULT_INDEX = "bright_cyan"
# STYLE_DEFAULT_INPUT = "cyan"


BG_COLOR_HEXA = "on #282C34"
BG_COLOR_SYS = ""


# Clés dictionnaires
KEY_EXIST = "exist"
KEY_NOT_EXIST = "not_exist"
KEY_LENGTH_DEFAULT = "length_default"
KEY_LENGTH_INDEX = "length_index"
KEY_NONE = "none"
KEY_NOT_FOUND = "N/A"
KEY_INT_POS = "int_positif"
KEY_LENGTH_NUMB = "length_numero"
KEY_NOT_EXIST_NUMB = "not_exist_for_num"
KEY_LENGTH_CODE_PIN = "length_code_pin"
KEY_INCORRECT_CODE_PIN = "incorrect_code_pin"


# DICTIONNAIRE
ERROR_MESSAGES = {
    KEY_EXIST : "existe déjà",
    KEY_NOT_EXIST : "n'existe pas",
    KEY_LENGTH_DEFAULT : f"Saisir caractères valides SVP (A-Za-z0-9)[{MIN_CHAR_DEFAULT}, {MAX_CHAR_DEFAULT}]",
    KEY_LENGTH_INDEX : f"Veuillez entrer un entier compris entre [{MIN_INDEX}, {MAX_INDEX}]",
    KEY_INT_POS : "Veuillez saisir un entier positif",
    KEY_LENGTH_NUMB : "Veuillez saisir un numéro valide",
    KEY_NOT_EXIST_NUMB : "n'est pas disponible",
    KEY_LENGTH_CODE_PIN : f"Le code PIN doit comporter {LENGTH_CODE_PIN} chiffres!",
    KEY_INCORRECT_CODE_PIN : "Mauvais code pin",
    KEY_NONE : "",
    KEY_NOT_FOUND : 'N/A',
}



MENU_GESTIONNAIRE = [
    "Créer un opérateur",
    "Renommer un opérateur",
    "Lister les opérateurs et leur index",
    "Lister les numéros d’un opérateur",
    "Ajouter un nouvel index pour un opérateur existant",
    "Supprimer un index d’un opérateur",
    "Vendre un numéro",
    "Vendre du crédit à un client",
    "État de la caisse",
    "Se déconnecter",
    "Quitter"
]

MENU_CLIENT = [
    "Consulter son crédit",
    "Effectuer un appel",
    "Voir l’historique des appels (vocaux)",
    "Écouter un vocal",
    "Supprimer un contact",
    "Renommer un contact ",
    "Ajouter un autre numéro à un contact existant",
    "Afficher le répertoire ",
    "Recherche un contact du répertoire par un mot clé ",
    "Bloquer / débloquer un contact",
    "Transférer du crédit",
    "Se déconnecter",
    "Quitter",
]

KEY_TITLE = "tilte"
KEY_OPTIONS = "options"
KEY_TITLE_STYLE = ""
KEY_ALTERN_COLORS = ""
KEY_BORDER_PANEL_STYLE = ""
KEY_INDEX_EXIST = ""


STRUCT_MENU_GESTIONNAIRE = {
    KEY_TITLE : " opérateur téléphonique ",
    KEY_OPTIONS : MENU_GESTIONNAIRE,
    KEY_TITLE_STYLE : "bold white",
    KEY_ALTERN_COLORS : ("bright_yellow", "bright_green"),
    KEY_BORDER_PANEL_STYLE : "bright_blue",
    KEY_INDEX_EXIST : STYLE_DEFAULT_INDEX,
}
