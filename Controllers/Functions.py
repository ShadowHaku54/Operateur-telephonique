# Functions - Controllers
from re import match as rem
from datetime import datetime
from Views import Functions as FuncViews
from consts import ERROR_MESSAGES, KEY_NOT_FOUND, BOOL_DISPO
from Models.Client import (
    recuperer_numeros as MC_recuperer_numeros, 
    recuperer_code_pin as MC_recuperer_code_pin, 
    recuperer_op_for_num as MC_recuperer_op_for_num
)
from Models.Operateur import recupere_gestionnaires as MO_recupere_gestionnaires

def est_chaine_valide(chaine, min_char=1, max_char=255):
    motif = rf"^[A-Za-z0-9]{{{min_char},{max_char}}}$"
    return bool(rem(motif, chaine.strip()))

def est_un_entierPos(value):
    return value.isdigit()

def get_date(short="all"):
    if short == "all":
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    elif short == "short":
        return datetime.now().strftime("%d/%m/%Y")


def get_error_message(key):
    if key in ERROR_MESSAGES:
        return ERROR_MESSAGES[key]
    return ERROR_MESSAGES[KEY_NOT_FOUND]

def if_list_contain_one_element(L):
    return L == [L[0]]

def confirmer(
    sms="Confirmer?",
    pos_choice = 'o',
    neg_choice = 'n',
    default = 'o',
    display_choices=True,
):
    pos_choice, neg_choice, default = [p.upper() if (p<"A" or p>"Z") else p for p in (pos_choice, neg_choice, default)]
    
    choices = [pos_choice, neg_choice]
    
    choices_disp = choices if display_choices else []
    choix = FuncViews.take_choice(sms, default=default, choices=choices_disp).upper()
    already_error = False
    
    
    while choix not in choices:
        FuncViews.processing(mode="error")
        choix = FuncViews.take_choice(sms, mode_affichage="error", default=default, choices=choices_disp, already_error=already_error).upper()
        if not already_error:
            already_error = True

    FuncViews.processing()
    return choix in pos_choice

def check_choix_in_marge(choix, maxi, mini=1):
    return est_un_entierPos(choix) and mini <= int(choix) <= maxi

def check_repect_numero(numero : str):
    numero = numero.replace(' ', '', count=3)
    return numero.isdigit() and len(numero) == 9

def check_log_in_client(numero, code_pin):
    numero = numero.replace(' ', '', count=3)
    liste_num = MC_recuperer_numeros()
    if numero in liste_num:
        return code_pin == MC_recuperer_code_pin(numero)
    return False

def check_log_in_gestionnaire(login, password):
    liste_gest = MO_recupere_gestionnaires()
    format_gest = f"{login},{password}"
    for gest in liste_gest:
        if format_gest == gest:
            return True
    return False

def log_in():
    FuncViews.afficher_tritre_principal_styler()
    FuncViews.afficher_titre_section_styler("Page de connexion", "purple")
    FuncViews.lines_spaces(2)
    login, code_pin = FuncViews.take_login_and_password()
    is_client = check_repect_numero(login)
    controle = condition_verifier(is_client)
    already_error = False
    while(not controle(login, code_pin)):
        FuncViews.processing(mode="error")
        login, code_pin = FuncViews.take_login_and_password(mode_affichage="error", already_error=already_error)
        is_client = check_repect_numero(login)
        
        controle = condition_verifier(is_client)
        if not already_error:
            already_error = True
    
    FuncViews.succes_message(" Connexion réussie ")
    FuncViews.processing()
    return dict(is_client=is_client, login=login)

def condition_verifier(is_client):
    if is_client:
        return check_log_in_client
    else:
        return check_log_in_gestionnaire

def menu_gestionnaire_interactif(title, menu, type_user, color_type_user):
    FuncViews.afficher_tritre_principal_styler()
    FuncViews.afficher_titre_section_styler(type_user, color_type_user)
    FuncViews.lines_spaces(2)
    FuncViews.afficher_menu(title, menu)
    choix = FuncViews.take_choice(default="1")
    already_error = False
    max_choice = len(menu)
    while not check_choix_in_marge(choix, maxi=max_choice):
        FuncViews.processing(mode="error")
        choix = FuncViews.take_choice(mode_affichage="error", default="1", already_error=already_error)
        if not already_error:
            already_error = True
    FuncViews.processing()
    return int(choix) - 1

def operateur_of_numero_client(numero_search):
    if numero_search in MC_recuperer_numeros():
        return MC_recuperer_op_for_num(numero_search)
    return None
