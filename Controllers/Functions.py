# Functions - Controllers
from re import match as rem
from datetime import datetime
from Views import Functions as FuncViews
from consts import ERROR_MESSAGES, KEY_NOT_FOUND, CREDIT_MINIMUN, KEY_RESPECT_CREDIT, KEY_EXIST, KEY_NONE, KEY_NOT_EXIST
from Models.Client import (
    recuperer_numeros as MC_recuperer_numeros, 
    recuperer_code_pin as MC_recuperer_code_pin, 
    recuperer_op_for_num as MC_recuperer_op_for_num
)
from Models.Operateur import recupere_gestionnaires as MO_recupere_gestionnaires

def est_chaine_valide(chaine, min_char=1, max_char=255):
    motif = rf"^[A-Za-z0-9]{{{min_char},{max_char}}}$"
    return bool(rem(motif, chaine.strip()))

def est_un_entier_pos(value):
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
    FuncViews.warning_message(sms, end="")
    pos_choice, neg_choice, default = [p.upper() if (p<"A" or p>"Z") else p for p in (pos_choice, neg_choice, default)]
    
    choices = [pos_choice, neg_choice]
    
    choices_disp = choices if display_choices else []
    choix = FuncViews.take_choice("", default=default, choices=choices_disp).upper()
    already_error = False
    
    
    while choix not in choices:
        FuncViews.processing(mode="error")
        FuncViews.warning_message(sms, end="")
        choix = FuncViews.take_choice("", mode_affichage="error", default=default, choices=choices_disp, already_error=already_error).upper()
        if not already_error:
            already_error = True

    FuncViews.processing()
    return choix in pos_choice

def check_choix_in_marge(choix, maxi, mini=1):
    return est_un_entier_pos(choix) and mini <= int(choix) <= maxi

def check_repect_numero(numero):
    numero = numero.replace(' ', '', count=3)
    return numero.isdigit() and len(numero) == 9

def check_log_in_client(numero, code_pin):
    numero = FuncViews.reforme_num(numero)
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

def operateur_of_numero_client(numero_search):
    if numero_search in MC_recuperer_numeros():
        return MC_recuperer_op_for_num(numero_search)
    return None

def respect_credit(credit):
    return est_un_entier_pos(credit) and int(credit)>=CREDIT_MINIMUN

def take_credit(sms = "Entrer le nombre de crédit à envoyer"):
    return int(take_any(sms, respect_credit, KEY_RESPECT_CREDIT))

def take_any(sms, func_check_no_respect, no_respect_key, func_check_exist=None, adv_exist_message="", exist_mode=KEY_NONE):
    
    existence_check = {
        KEY_EXIST : lambda nom: func_check_exist(nom),
        KEY_NOT_EXIST : lambda nom: not func_check_exist(nom),
        KEY_NONE : lambda nom: False,
    }
    
    
    valeur = FuncViews.take_value(sms)
    
    no_respect = not func_check_no_respect(valeur)
    existence = existence_check[exist_mode](valeur)
    
    existence_message = get_error_message(exist_mode)
    no_respect_message = get_error_message(no_respect_key)
    
    already_error = False
    while no_respect or existence:
        FuncViews.processing(mode="error")
        
        adv = adv_exist_message.format(valeur=valeur, existence_message=existence_message) if existence else no_respect_message
        valeur = FuncViews.take_value(
            sms, mode_affichage="error",
            advertissement = adv,
            already_error=already_error,
        )
        
        no_respect = not func_check_no_respect(valeur)
        existence = existence_check[exist_mode](valeur)
        
        if not already_error:
            already_error = True
    
    FuncViews.processing()
    
    return valeur

def take_numero(sms = "Entrer le numéro"):
    numero = FuncViews.take_value(sms)
    numero = FuncViews.reforme_num(numero)
    already_error = False
    while not check_repect_numero(numero):
        FuncViews.processing(mode="error")
        numero = FuncViews.take_value(sms, "error", "Numéro incorrect", already_error)
        numero = FuncViews.reforme_num(numero)
        
        if not already_error:
            already_error = True
    FuncViews.processing()
    return numero


def aurevoir():
    FuncViews.display_aurevoir()
    
