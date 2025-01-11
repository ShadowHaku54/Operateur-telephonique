# Client -Controllers
from Models import Client as ClientModels
from Views import Functions as FuncViews
from Views import Client as ClientViews
from Controllers import Functions as FuncControllers
from consts import (
    USER_CLIENT, COLOR_SECT_CLIENT, MENU_CLIENT, LEN_MENU_CLIENT,
    KEY_LENGTH_NUMB, TAUX_TRANSFERT
)

Client = {
    "numero": "",
    "code_pin": "",
    "operateur": "",
}

def menu_gestionnaire_interactif():
    FuncViews.afficher_tritre_principal_styler()
    FuncViews.afficher_titre_section_styler(USER_CLIENT, COLOR_SECT_CLIENT)
    ClientViews.barre_header(Client["operateur"])
    FuncViews.lines_spaces(2)
    FuncViews.afficher_menu("Menu principal", MENU_CLIENT)
    choix = FuncViews.take_choice(default="1")
    already_error = False
    max_choice = len(MENU_CLIENT)
    while not FuncControllers.check_choix_in_marge(choix, maxi=max_choice):
        FuncViews.processing(mode="error")
        choix = FuncViews.take_choice(mode_affichage="error", default="1", already_error=already_error)
        if not already_error:
            already_error = True
    FuncViews.processing()
    return int(choix) - 1


def define_client(numero):
    Client["numero"] = FuncViews.reforme_num(numero)
    Client["code_pin"] = ClientModels.recuperer_code_pin(Client["numero"])
    Client["operateur"] = ClientModels.recuperer_op_for_num(Client["numero"])

def header_client(choix, spaces=2):
    FuncViews.afficher_tritre_principal_styler()
    FuncViews.afficher_titre_section_styler(USER_CLIENT, COLOR_SECT_CLIENT)
    ClientViews.barre_header(Client["operateur"], MENU_CLIENT[choix])
    FuncViews.lines_spaces(spaces)


def use_case_client():
    func_use_case = [
        voir_credit,
        transfert_credit,
    ]
    
    while True:
        choix = menu_gestionnaire_interactif()
        
        if choix == LEN_MENU_CLIENT-1:
            return True
        elif choix == LEN_MENU_CLIENT-2:
            return False
        
        func_use_case[choix](choix)


def voir_credit(choix):
    header_client(choix)
    take_code_pin()
    credit = ClientModels.recuperer_credit(Client["numero"])
    FuncViews.afficher_en_couleur(f"Vous avez [bold]{credit}[/] F CFA", "blue on bright_white")
    FuncViews.continuer()

def take_code_pin(sms="Entrer votre code pin"):
    code_pin = FuncViews.take_password(sms)
    already_error = False
    while not check_code_pin(code_pin):
        FuncViews.processing(mode="error")
        code_pin = FuncViews.take_password(sms, mode_affichage="error", adv_sms="code pin incorrect", already_error=already_error)
        if not already_error:
            already_error = True
    FuncViews.processing()

def check_code_pin(code_pin):
    return code_pin == Client["code_pin"]

def afficher_repertoire():
    pass


def transfert_credit(choix):
    header_client(choix)
    
    numero = take_numero()
    debt_credit = FuncControllers.take_credit()
    if check_numero(numero):
        credit_client = ClientModels.recuperer_credit(Client["numero"])
        take_code_pin()
        new_solde_client = credit_client-debt_credit
        if new_solde_client>=0:
            credit_avec_taux = debt_credit * (1 - TAUX_TRANSFERT)
            if FuncControllers.confirmer(f"Envoie {debt_credit} | {credit_avec_taux} F CFA au '{FuncViews.formated_num(numero)}'. Confirmer?"):
                ClientModels.update_credit_client(Client["numero"], new_solde_client, add=False)
                ClientModels.update_credit_client(numero, credit_avec_taux)
                FuncViews.succes_message(f"{debt_credit} crédits envoyé au {numero}")
                FuncViews.succes_message(f"Nouveau solde {new_solde_client}")
        else:
            FuncViews.error_message("Solde insuffisant")
            FuncViews.error_message_simple("Veuillez d'abord recharger chez un fournisseur.")
    else:
        FuncViews.error_message("Numéro invalide")
        FuncViews.error_message_simple("Ce numéro est soit d'un opérateur différent, soit est le votre ou soit n'a pas encore été attribué")
    FuncViews.continuer()

def take_numero(sms = "Entrer le numéro du client"):
    numero = FuncViews.take_value(sms)
    numero = FuncViews.reforme_num(numero)
    already_error = False
    while not FuncControllers.check_repect_numero(numero):
        FuncViews.processing(mode="error")
        numero = FuncViews.take_value(sms, "error", "Numéro incorrect", already_error)
        numero = FuncViews.reforme_num(numero)
        
        if not already_error:
            already_error = True
    FuncViews.processing()
    return numero

def check_numero(numero):
    return Client["numero"] != numero and Client["operateur"] == FuncControllers.operateur_of_numero_client(numero)

