# Client -Controllers
from Models import Client as ClientModels
from Views import Functions as FuncViews
from Views import Client as ClientViews
from Controllers import Functions as FuncControllers
from consts import (
    USER_CLIENT, COLOR_SECT_CLIENT, MENU_CLIENT, LEN_MENU_CLIENT, TAUX_TRANSFERT
    , MENU_GESTION_REPERTOIRE, MENU_GESTION_CONTACT, LIMIT_NB_CONTACTS_CLIENT
    , BOOL_NOT_BLOCKED, BOOL_BLOCKED, MENU_CONTACT_FLITRE, FILE_SD_CALLING, FILE_SD_COUPURE
    , NB_NUMBER_AFTER_COMMA, IS_NOT_ALREADY_READ, IS_ALREADY_READ
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
        gestion_repertoire,
        historique_appels,
    ]
    
    while True:
        choix = menu_gestionnaire_interactif()
        
        if choix == LEN_MENU_CLIENT-1:
            return True
        elif choix == LEN_MENU_CLIENT-2:
            return False
        
        func_use_case[choix](choix)


def voir_credit(choix_main_menu):
    header_client(choix_main_menu)
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


def gestion_repertoire(choix_main_menu):
    repertoire = ClientModels.recuperer_contacts(Client["numero"])
    while True:
        header_client(choix_main_menu, 1)
        ClientViews.afficher_repertoire(repertoire)
        choix_menu = take_choix_menu(MENU_GESTION_REPERTOIRE.keys())
        if choix_menu == 'S':
            choix_contact = take_choix_contact(len(repertoire), sms="Entrer l'indice du contact", opt_exit='R', name_opt="retour")
            if choix_contact != 'R':
                indice_contact = int(choix_contact) - 1
                gestion_contact(choix_main_menu, repertoire, indice_contact)
            else:
                FuncViews.processing(go="back")
        elif choix_menu == 'RE':
            rechercher_contact(choix_main_menu, repertoire)
        elif choix_menu == 'A':
            ajouter_contact(repertoire)
        elif choix_menu == 'C':
            composer_numero(choix_main_menu, repertoire)
        elif choix_menu == 'R':
            break
    FuncViews.processing(go="back")

def take_choix_contact(max_choice, sms, opt_exit, name_opt):
    ff_sms = f"{sms} [{opt_exit} pour {name_opt}]"
    choix = FuncViews.take_choice(ff_sms, default="1")
    already_error = False
    while not check_choix(choix.upper(), max_choice, opt_exit):
        FuncViews.processing(mode="error")
        choix = FuncViews.take_choice(ff_sms, default="1", mode_affichage="error", already_error=already_error)
        if not already_error:
            already_error = True
    FuncViews.processing()
    return choix.upper()

def gestion_contact(choix_main_menu, repertoire, indice_contact):
    contact = repertoire[indice_contact]
    while True:
        header_client(choix_main_menu)
        ClientViews.afficher_menu_contact(contact)
        choix_menu = take_choix_menu(MENU_GESTION_CONTACT.keys())
        if choix_menu == 'A':
            appeler_num_contact(repertoire, indice_contact, choix_main_menu)
        elif choix_menu == 'RN':
            renommer_contact(repertoire, indice_contact)
        elif choix_menu == 'AD':
            ajouter_numero(repertoire, indice_contact)
        elif choix_menu == 'B':
            flag_bloquer_debloquer_contact(repertoire, indice_contact, action='B')
        elif choix_menu == 'D':
            flag_bloquer_debloquer_contact(repertoire, indice_contact, action='D')
        elif choix_menu == 'S':
            if supprimer_contact(repertoire, indice_contact):
                break
        elif choix_menu == 'R':
            break
    FuncViews.processing(go="back")

def flag_bloquer_debloquer_contact(repertoire, indice_contact, action='B'):
    
    action_flag = {
        'B' : {"flag": BOOL_BLOCKED, "sms_fr": "bloquer", "sms_eng": "lock"},
        'D' : {"flag": BOOL_NOT_BLOCKED, "sms_fr": "débloquer", "sms_eng": "unlock"}
    }
    
    flag, sms_fr, sms_eng = action_flag[action].values()
    
    contact = repertoire[indice_contact]

    if flag != contact["flag"]:
        contact["flag"] = flag
        date = FuncControllers.get_date()
        ClientModels.update_repertoire(Client["numero"], repertoire)
        FuncViews.succes_message(f"Le contact a été {sms_fr} avec succes")
        ClientModels.update_registre(
            Client["numero"],
            f"{sms_eng}_contact",
            date,
            f"Contact '{contact["nom_contact"]}' {sms_fr}"
        )
    else:
        FuncViews.error_message_simple(f"Le contact est déjà {sms_fr}")
    FuncViews.continuer()

def take_choix_menu(choices, with_first_default=True):
    default = list(choices)[0] if with_first_default else None
    choix_menu = FuncViews.take_choice(default=default)
    already_error = False
    while choix_menu.upper() not in choices:
        FuncViews.processing(mode="error")
        choix_menu = FuncViews.take_choice(default=default, mode_affichage="error", already_error=already_error)
        if not already_error:
            already_error = True
    FuncViews.processing()
    return choix_menu.upper()

def check_choix(choix, max_choice, opt_exit=""):
    if opt_exit:
        return choix == opt_exit or FuncControllers.check_choix_in_marge(choix, max_choice)
    else:
        return FuncControllers.check_choix_in_marge(choix, max_choice)

def transfert_credit(choix_main_menu):
    header_client(choix_main_menu)
    
    numero = FuncControllers.take_numero()
    debt_credit = FuncControllers.take_credit()
    if check_numero_and_opeateur(numero):
        credit_client = ClientModels.recuperer_credit(Client["numero"])
        take_code_pin()
        new_solde_client = credit_client-debt_credit
        if new_solde_client>=0:
            credit_avec_taux = debt_credit * (1 - TAUX_TRANSFERT)
            if FuncControllers.confirmer(f"Envoie {debt_credit} | {credit_avec_taux} F CFA au '{FuncViews.formated_num(numero)}'. Confirmer?"):
                ClientModels.update_credit_client(Client["numero"], new_solde_client, add=False)
                ClientModels.update_credit_client(numero, credit_avec_taux)
                FuncViews.succes_message(f"{credit_avec_taux} crédits envoyé au {numero}")
                FuncViews.succes_message(f"Nouveau solde {new_solde_client}F")
                date = FuncControllers.get_date()
                ClientModels.update_registre(
                    Client['numero'],
                    "transfert_credit",
                    date,
                    f"{credit_avec_taux} crédits transférés au {numero}"
                )
                ClientModels.update_registre(
                    numero,
                    "receive_credit",
                    date,
                    f"{credit_avec_taux} crédits reçu du {Client['numero']}"
                )
        else:
            FuncViews.error_message("Solde insuffisant")
            FuncViews.error_message_simple("Veuillez d'abord recharger chez un fournisseur.")
    else:
        FuncViews.error_message("Numéro invalide")
        FuncViews.error_message_simple("Ce numéro est soit d'un opérateur différent, soit est le votre ou soit n'a pas encore été attribué")
    FuncViews.continuer()


def historique_appels(choix_main_menu):
    header_client(choix_main_menu)
    historique = ClientModels.collect_historique(Client["numero"])
    ClientViews.afficher_historique(historique)
    choix_lecture = take_choix_contact(len(historique), "Entrer la position pour lire", "Q", "pour quitter")
    if choix_lecture != 'Q':
        indice_audio = int(choix_lecture) - 1
        audio = historique[indice_audio]
        fic_audio = audio["fic_voc"]
        FuncViews.afficher_en_couleur("Appuyer sur [Entrer] pour sortir du mode lecture.", end="")
        ClientModels.lire_vocal(fic_audio)
        FuncViews.warning_message("Arrêté/Interrompu")
        if audio["vue"] == IS_NOT_ALREADY_READ:
            audio["vue"] = IS_ALREADY_READ
            ClientModels.update_historique_for_ecoute(Client["numero"], historique)
        FuncViews.processing(go="back")
        historique_appels(choix_main_menu)
        return
    FuncViews.processing(go="back")

def check_numero_and_opeateur(numero):
    return Client["numero"] != numero and Client["operateur"] == FuncControllers.operateur_of_numero_client(numero)

def convert_menu_in_str(menu, sep=' | '):
    return sep.join([f"({choix}){option}" for choix, option in menu.items()])

def ajouter_contact(repertoire):
    nom_contact = FuncControllers.take_name("Entrer le nom du contact")
    premier_numero = FuncControllers.take_numero()
    ff_premier_numero = FuncViews.formated_num(premier_numero)
    date = FuncControllers.get_date()
    indice = indice_contact_exist(nom_contact, repertoire)
    if indice != -1:
        FuncViews.warning_message(f"Le contact '{nom_contact}' existe déjà. Que voulez vous faire?")
        FuncViews.afficher_en_couleur("(A)ajouter le numéro | (N)annuler.", "yellow")
        ajouter = FuncControllers.confirmer("Entrer un choix", pos_choice='a', neg_choice='n', default='n')
        if ajouter:
            operation_ajout_numero_contact(premier_numero, repertoire, indice, ff_premier_numero, date)
        else:
            FuncViews.warning_message("Opération annuler!")
    else:
        contact = dict(nom_contact=nom_contact, flag=BOOL_NOT_BLOCKED, liste_nums=[premier_numero])
        ClientModels.ajouter_contact(Client["numero"], contact)
        repertoire.append(contact)
        FuncViews.succes_message(f"Contact '{nom_contact}' '{ff_premier_numero}' ajouté avec succès")
        ClientModels.update_registre(
            Client["numero"],
            "add_contact",
            date,
            f"Ajout du contact: '{nom_contact}' '{premier_numero}'"
        )

    FuncViews.continuer()


def indice_contact_exist(nom_contact, repertoire):
    N = len(repertoire)
    for indice in range(N):
        if nom_contact == repertoire[indice]["nom_contact"]:
            return indice
    return -1

def check_add_num_in_liste_nums(numero, liste_nums):
    return len(liste_nums) < LIMIT_NB_CONTACTS_CLIENT and numero not in liste_nums

def check_numero_for_contact(numero):
    return Client["numero"] != numero and numero in ClientModels.recuperer_numeros()

def operation_ajout_numero_contact(numero_to_add, repertoire, indice_contact, ff_numero, date):
    contact = repertoire[indice_contact]
    if check_add_num_in_liste_nums(numero_to_add, contact["liste_nums"]):
        contact["liste_nums"].append(numero_to_add)
        ClientModels.update_repertoire(Client["numero"], repertoire)
        FuncViews.succes_message(f"Numéro: '{ff_numero}' ajouter au contact '{contact["nom_contact"]}' avec succes")
        ClientModels.update_registre(
            Client["numero"],
            "add_num_contact",
            date,
            f"Ajout du numéro '{numero_to_add}' au contact '{contact["nom_contact"]}'"
        )
    else:
        FuncViews.error_message("Impossible d'ajouter")
        FuncViews.error_message_simple(f"Cet contact '{contact["nom_contact"]}' a soit atteint le nombre limite de numéro ou soit le numéro est déjà présent")

def ajouter_numero(repertoire, indice_contact):
    numero = FuncControllers.take_numero()
    ff_numero = FuncViews.formated_num(numero)
    date = FuncControllers.get_date()
    operation_ajout_numero_contact(numero, repertoire, indice_contact, ff_numero, date)
    FuncViews.continuer()


def renommer_contact(repertoire, indice_contact):
    nouveau_nom = FuncControllers.take_name("Entrer le nouveau nom")
    contact = repertoire[indice_contact]
    if indice_contact_exist(nouveau_nom, repertoire) == -1:
        ancien_nom = contact["nom_contact"]
        contact["nom_contact"] = nouveau_nom
        date = FuncControllers.get_date()
        ClientModels.update_repertoire(Client["numero"], repertoire)
        FuncViews.succes_message(f"Contact renommé avec succè. Nouveau nom: '{contact["nom_contact"]}'")
        ClientModels.update_registre(
            Client["numero"],
            "rename_contact",
            date,
            f"Nom du contact '{ancien_nom}' devenu '{nouveau_nom}'"
        )
    else:
        FuncViews.error_message("Nom invalide")
        FuncViews.error_message_simple(f"Le nom '{nouveau_nom}' appartient déjà à un de vos contacts!")
    FuncViews.continuer()

def rechercher_contact(choix_main_menu, repertoire):
    mot_cle = FuncViews.take_value("Rechercher [QUIT pour quitter]...")
    FuncViews.processing()
    if mot_cle != "QUIT":
        while True:
            filtre_repertoire = collect_names_by_word_key(repertoire, mot_cle)
            header_client(choix_main_menu, 1)
            ClientViews.dispaly_rule_sous_titre(f" RECHERCHER | filtre par mot clé '{mot_cle}'")
            FuncViews.lines_spaces()
            ClientViews.afficher_repertoire_filtre(filtre_repertoire)
            choix_menu = take_choix_menu(MENU_CONTACT_FLITRE.keys())
            if choix_menu == 'S':
                choix_cf = take_choix_contact(len(filtre_repertoire), sms="Entrer l'indice du contact", opt_exit='R', name_opt="retour")
                nom_contact = filtre_repertoire[int(choix_cf) - 1]["nom_contact"]
                indice_contact = indice_contact_exist(nom_contact, repertoire)
                if choix_cf != 'R':
                    gestion_contact(choix_main_menu, repertoire, indice_contact)
                else:
                    FuncViews.processing(go="back")
            elif choix_menu == 'RE':
                rechercher_contact(choix_main_menu, repertoire)
                return
            elif choix_menu == 'R':
                break
    FuncViews.processing(go="back")


def collect_names_by_word_key(repertoire, mot_cle):
    filtre_repertoire = []
    mot_cle = mot_cle.lower()
    for contact in repertoire:
        if mot_cle in contact["nom_contact"].lower():
            filtre_repertoire.append(contact)
    return filtre_repertoire


def supprimer_contact(repertoire, indice_contact):
    if FuncControllers.confirmer("Confirmer la suppression su contact?"):
        contact = repertoire.pop(indice_contact)
        ClientModels.update_repertoire(Client["numero"], repertoire)
        FuncViews.succes_message(f"Contact '{contact["nom_contact"]}' supprimé avec succès")
        ClientModels.update_registre(
            Client["numero"],
            "del_contact",
            FuncControllers.get_date(),
            f"Suppression du contact '{contact["nom_contact"]}'"
        )
        return True
    
    FuncViews.warning_message("Opération annuler")
    FuncViews.processing(go="back")
    return False

def appeler_num_contact(repertoire, indice_contact, choix_main_menu):
    contact = repertoire[indice_contact]
    ClientViews.afficher_tab_num_contact(contact["liste_nums"], contact["flag"])
    choix_contact = take_choix_contact(len(contact["liste_nums"]), "Sélectionner un des numéros", "Q", "quitter")
    if choix_contact != 'Q':
        numero_selectionne = contact["liste_nums"][int(choix_contact) - 1]
        flag = contact["flag"] == BOOL_BLOCKED
        appeler(choix_main_menu, repertoire, numero_selectionne, flag, contact["nom_contact"])
    else:
        FuncViews.warning_message("Action annuler!")
        FuncViews.continuer()

def appeler(choix_main_menu, repertoire, numero_appel, give_flag=False, nom_contact=None):
    if give_flag:
        appeler_num_unlock(choix_main_menu, numero_appel, nom_contact)
    else:
        flag, nom_contact = check_num_is_not_unlock_name_contact(repertoire, numero_appel)
        if flag:
            appeler_num_unlock(choix_main_menu, numero_appel, nom_contact)
        else:
            FuncViews.error_message_simple("Contact bloqué! appel indisponible")
    FuncViews.continuer()

def appeler_num_unlock(choix_main_menu, numero_appel, nom_contact=None):
    solde = ClientModels.recuperer_credit(Client["numero"])
    if solde > 0:
        if numero_appel != Client["numero"]:
            operateur_destinaire = check_num_return_op(numero_appel)
            if operateur_destinaire:
                header_client(choix_main_menu, 1)
                appel_pass(operateur_destinaire, numero_appel, solde, nom_contact)
            else:
                FuncViews.error_message_simple("Impossible de joindre ce numéro!")
        else:
            FuncViews.error_message_simple("Impossible de joindre ce numéro!")
    else:
        FuncViews.error_message_simple("Solde de crédit insuffisant. Veuillez recharger pour effectuer un appel")

def appel_pass(operateur_destine, numero_destine, solde, nom_contact=None):
    type_tarif = "ordinaire" if (Client["operateur"] == operateur_destine) else "different"
    tarif = ClientModels.select_tarif_op(Client["operateur"], type_tarif)
    duree_max = solde / tarif
    nom_fichier = FuncControllers.generer_nom_unique(Client["numero"], numero_destine)
    nom_complet_fichier = f"{nom_fichier}.wav"
    page_appel(nom_complet_fichier, duree_max, numero_destine, tarif, solde, nom_contact)


def page_appel(nom_fichier, max_time, numero, tarif, solde, nom_contact=None):
    ClientViews.dispaly_rule_sous_titre(" APPEL TELEPHONIQUE ")
    FuncViews.lines_spaces()
    ClientViews.contact_appel(numero, nom_contact)
    FuncViews.lines_spaces()
    ClientViews.message_appel()

    reponse = ClientModels.lire_audio_avec_arret(FILE_SD_CALLING)
    
    if reponse == "" or reponse.upper() == 'D':
        date = FuncControllers.get_date()
        FuncViews.warning_message("Enregistrement en cours...")
        FuncViews.warning_message("Appuyez sur [Entrée] pour arrêter")
        durree_appel = ClientModels.enregistrer_vocal_wav(nom_fichier, max_time)
        ClientModels.lire_audio_fin(FILE_SD_COUPURE)
        FuncViews.succes_message("Enregistrement terminé")
        
        cout_appel = round(tarif * durree_appel, NB_NUMBER_AFTER_COMMA)
        if cout_appel > solde:
            cout_appel = solde
        
        nouveau_solde = round(solde - cout_appel, NB_NUMBER_AFTER_COMMA)
        
        FuncViews.succes_message(f"Vocal envoyé au {FuncViews.formated_num(numero)}")
        FuncViews.succes_message(f"Durée: {durree_appel}s | tarif: {tarif}F/s | coût: {cout_appel}F")
        FuncViews.succes_message(f"Nouveau solde: {nouveau_solde}F")
        
        ClientModels.update_credit_client(Client["numero"], nouveau_solde, False)
        
        ClientModels.update_historique(
            nom_fichier,
            Client["numero"],
            numero,
            date,
            durree_appel,
            cout_appel
        )
        
        ClientModels.update_registre(
            Client["numero"],
            "in_call",
            date,
            f"Envoie du vocal '{nom_fichier}' au '{numero}'.Durée: {durree_appel}s.Coût d'appel: {cout_appel} crédits"
        )
        
        ClientModels.update_registre(
            numero,
            "out_call",
            date,
            f"Reception du vocal '{nom_fichier}' du '{Client['numero']}'. Durée: {durree_appel}"
        )
    else:
        FuncViews.warning_message("Action annuler!")


def composer_numero(choix_main_menu, repertoire):
    numero_appel = FuncControllers.take_numero()
    appeler(choix_main_menu, repertoire, numero_appel)

def check_num_return_op(numero):
    if numero in ClientModels.recuperer_numeros():
        return ClientModels.recuperer_op_for_num(numero)
    return None

def check_num_is_not_unlock_name_contact(repertoire, numero_search):
    for contact in repertoire:
        if numero_search in contact["liste_nums"]:
            return contact["flag"], contact["nom_contact"]
    return True, None

