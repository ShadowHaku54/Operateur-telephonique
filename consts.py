MAIN_TITLE = " opérateur téléphonique "
PATH_DB_OPERATEURS = r"./DB/Operateurs/"
FILE_GESTIONNAIRES = r"./DB/Gestionnaires.txt"
PATH_DB_CLIENTS = r"./DB/Clients/"
PATH_DB_VOCAUX = r"./DB/Sounds/Vocaux/"
PATH_DB_SOUNDS = r"./DB/Sounds/"
FILE_SD_COUPURE = r"./DB/Sounds/coupure_appel.wav"
FILE_SD_CALLING = r"./DB/Sounds/calling.wav"
FILE_CAISSE = "transactions.txt"
FILE_REGISTRE = "registre.txt"
FILE_INFO = "infos.txt"
FILE_CONTACTS = "contacts.txt"
FILE_HISTORIQUE = "historique.txt"
DIR_INDEX = "Index"
NUM_GENERES = 100
BOOL_DISPO = "1"
BOOL_NOT_DISPO = "0"
BOOL_BLOCKED = "1"
BOOL_NOT_BLOCKED = "0"
IS_ALREADY_READ = "1"
IS_NOT_ALREADY_READ = "0"
APPEL_ENTRANT = "in"
APPEL_SORTANT = "out"
STYLE_DISPO = "bold bright_green"
STYLE_NOT_DISPO = "bold bright_red"
CREDIT_MINIMUN = 100
DEFAULT_LINES_SPACES = 1
LIMIT_NB_INDEX = 3
LIMIT_NB_CONTACTS_CLIENT = 3
NB_NUMBER_AFTER_COMMA = 2

USER_GESTIONNAIRE = "Gestionnaire"
USER_CLIENT = "Client"
COLOR_USER_GESTION = "yellow"
COLOR_SECT_CLIENT = "purple"

MAX_CHAR_DEFAULT = 15
MIN_CHAR_DEFAULT = 3
PROCESSING_COUPURE = 0.36
TIME_LECTURE_UNIQUE = 6

CODE_PIN_DEFAULT = "1234"
LENGTH_CODE_PIN = 4
MAX_INDEX = 99
MIN_INDEX = 10
CHAR_INDEX = 2
TAUX_TRANSFERT = 10/100

SPACES_TAB = 4
TAB = " "*SPACES_TAB

STYLE_DEFAULT_INDEX = "bright_cyan"


BG_COLOR_HEXA = "on #282C34"
BG_COLOR_SYS = ""

WARNING_STYLE = "bold #fe7b00 on black"

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
KEY_RESPECT_CREDIT = "incorrect_credit"

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
    KEY_RESPECT_CREDIT: f"Nombre de crédit invalide (* >= {CREDIT_MINIMUN})",
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

LEN_MENU_GESTIONNAIRE = len(MENU_GESTIONNAIRE)

MENU_CLIENT = [
    "Consulter son crédit",
    "Transférer du crédit",
    "Gestion des contacts et appels",
    "Gestion de l'historique des vocaux",
    "Se déconnecter",
    "Quitter",
]

LEN_MENU_CLIENT = len(MENU_CLIENT)

MEMUN_GESTION_HISTORIQUE = {
    'C' : "choisir",
    'Q' : "quitter",
}

MENU_GESTION_VOCAUX = {
    'E': "écouter",
    'S': "supprimer",
    'R': "retour",
    'Q': "quitter"
}

MENU_GESTION_REPERTOIRE = {
    'S': "Sélectionner un contact",
    'RE': "Rechercher un contact",
    'A': "Ajouter un contact",
    'C': "Composer un numéro (appel)",
    'R': "Retour"
}

MENU_GESTION_CONTACT = {
    'A': "Appeler",
    'RN': "Renommer",
    'AD': "Ajouter numéro",
    'B': "Bloquer",
    'D': "Débloquer",
    'S': "Supprimer le contact",
    'R': "Retour",
}

MENU_CONTACT_FLITRE = {
    'S' : "Sélectionner",
    'RE' : "Effectuer une autre recherche",
    'R' : "Retour"
}


KEY_TITLE = "tilte"
KEY_OPTIONS = "options"
KEY_TITLE_STYLE = ""
KEY_ALTERN_COLORS = ""
KEY_BORDER_PANEL_STYLE = ""
KEY_INDEX_EXIST = ""

