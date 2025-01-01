
PATH_DB_OPERATEUR = r"./DB/Operateurs/"
DIR_INDEX = "Index"
NUM_GENERES = 100
BOOl_DISPONIPLE = 1
BOOL_INDISPONIBLE = 0

MAX_CHAR_OP = 15
MIN_CHAR_OP = 3

MAX_INDEX = 99
MIN_INDEX = 10
CHAR_INDEX = 2

SPACES_TAB = 4
TAB = " "*SPACES_TAB


ANSI_COULEURS = {
    "noir": "30",
    "rouge": "31",
    "vert": "32",
    "jaune": "33",
    "bleu": "34",
    "magenta": "35",
    "cyan": "36",
    "blanc": "37",
    "gris_clair": "90",
    "rouge_clair": "91",
    "vert_clair": "92",
    "jaune_clair": "93",
    "bleu_clair": "94",
    "magenta_clair": "95",
    "cyan_clair": "96",
    "blanc_clair": "97",
    "reset": "0"
}

ANSI_FONDS = {
    "noir": "40",
    "rouge": "41",
    "vert": "42",
    "jaune": "43",
    "bleu": "44",
    "magenta": "45",
    "cyan": "46",
    "blanc": "47",
    "gris_clair": "100",
    "rouge_clair": "101",
    "vert_clair": "102",
    "jaune_clair": "103",
    "bleu_clair": "104",
    "magenta_clair": "105",
    "cyan_clair": "106",
    "blanc_clair": "107"
}

ANSI_STYLE = {
    "gras": "1",
    "souligné": "4",
    "inversé": "7",
    "reset": "0"
}


# Clés dictionnaires
KEY_EXIST = "exist"
KEY_NOT_EXIST = "not_exist"
KEY_LENGTH_OP = "lenght_op"
KEY_LENGTH_INDEX = "lenght_index"
KEY_NONE = "none"
KEY_NOT_FOUND = "N/A"
KEY_INT_POS = "int_positif"



# DICTIONNAIRE
ERROR_MESSAGES = {
    KEY_EXIST : "existe déjà",
    KEY_NOT_EXIST : "n'existe pas",
    KEY_LENGTH_OP : f"nombre de caractères compris entre [{MIN_CHAR_OP}-{MAX_CHAR_OP}]",
    KEY_LENGTH_INDEX : f"entier compris entre [{MIN_INDEX}-{MAX_INDEX}]",
    KEY_INT_POS : "un entier positif SVP !",
    KEY_NONE : ""
}