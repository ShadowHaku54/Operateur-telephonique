# Functions - Controllers
from datetime import datetime
from Views import Functions as FuncViews
from consts import ERROR_MESSAGES, KEY_NOT_FOUND


def est_un_entierPos(value):
    return value.isdigit()


def get_date():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def get_error_message(key):
    if key in ERROR_MESSAGES:
        return ERROR_MESSAGES[key]
    return ERROR_MESSAGES[KEY_NOT_FOUND]

def if_list_contain_one_element(L):
    return L == [L[0]]

def confirmer(
    sms, 
    choices = {"pos_choice": 'o', "neg_choice": 'n', "default": 'o'}, 
    display_choices=True, 
    sensitve_case=False
):
    pos_choice, neg_choice, default = [p.upper() if (sensitve_case and p<"A" or p>"Z") else p for p in choices.values()]
    choices = [pos_choice, neg_choice]
    
    choices_disp = choices if display_choices else []
    choix = FuncViews.take_choice(sms, default=default, choices=choices_disp)
    already_error = False
    
    if not sensitve_case:
        choix = choix.upper()
    
    while choix not in choices:
        FuncViews.processing(type="error")
        choix = FuncViews.take_choice(sms, mode_affichage="error", default=default, choices=choices_disp, already_error=already_error)
        if not already_error:
            already_error = True
        if not sensitve_case:
            choix = choix.upper()

    FuncViews.processing()
    return choix in pos_choice