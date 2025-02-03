import random
from consts import (
    NUM_GENERES, MIN_INDEX, MAX_INDEX, BOOL_DISPO, BOOL_NOT_DISPO,
    CODE_PIN_DEFAULT, LENGTH_CODE_PIN, KEY_EXIST, KEY_LENGTH_DEFAULT, KEY_NOT_EXIST, KEY_LENGTH_INDEX,
    KEY_INT_POS, USER_GESTIONNAIRE, COLOR_USER_GESTION, MENU_GESTIONNAIRE, TIME_LECTURE_UNIQUE,
    LEN_MENU_GESTIONNAIRE, LIMIT_NB_INDEX
)
from Controllers import Functions as FuncControllers
from Views import Functions as FuncViews, Operateur as OpViews
from Models import Operateur as OpModels

def menu_gestionnaire_interactif():
    FuncViews.afficher_tritre_principal_styler()
    FuncViews.afficher_titre_section_styler(USER_GESTIONNAIRE, COLOR_USER_GESTION)
    FuncViews.lines_spaces(2)
    FuncViews.afficher_menu("Menu principal : Gestion des Opérateurs", MENU_GESTIONNAIRE)
    choix = FuncViews.take_choice(default="1")
    already_error = False
    max_choice = len(MENU_GESTIONNAIRE)
    while not FuncControllers.check_choix_in_marge(choix, maxi=max_choice):
        FuncViews.processing(mode="error")
        choix = FuncViews.take_choice(mode_affichage="error", default="1", already_error=already_error)
        if not already_error:
            already_error = True
    FuncViews.processing()
    return int(choix) - 1


def header_gestionnaire(choix, spaces=2):
    FuncViews.afficher_tritre_principal_styler()
    FuncViews.afficher_titre_section_styler(USER_GESTIONNAIRE, COLOR_USER_GESTION)
    FuncViews.afficher_titre_operation_styler(MENU_GESTIONNAIRE[choix])
    FuncViews.lines_spaces(spaces)

def use_case_gestionnaire():
    func = [
        create_new_op,
        rename_operate,
        lister_operateurs_et_index,
        afficher_numeros_operateur,
        add_new_index,
        supprimer_index,
        vendre_numero,
        vendre_credit,
        etat_caisse,
    ]
    
    while True:
        choix = menu_gestionnaire_interactif()
        if choix == LEN_MENU_GESTIONNAIRE-1:
            return True
        elif choix == LEN_MENU_GESTIONNAIRE-2:
            return False
    
        func[choix](choix)


def generate_nums_for_index(index):
    
    numeros = set()
    
    motifs_possibles = [
        lambda: f"{random.randint(100, 999)}{random.randint(1000, 9999)}",
        lambda: f"{random.randint(100, 999)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(10, 99)}",
        lambda: f"{random.randint(10, 99)}{random.randint(0, 9)}{random.randint(10, 99)}{random.randint(0, 9)}{random.randint(0, 9)}"
    ]
    
    while len(numeros) < NUM_GENERES:
        motif = random.choice(motifs_possibles)()
        numero = index+motif
        numeros.add(numero)
    
    return sorted(numeros)


def take_nom_operateur(exist_mode, sms="Saisir le nom de l'opérateur"):
    adv_exist_message = "l'opérateur '{valeur}' {existence_message}"
    return FuncControllers.take_any(sms, FuncControllers.check_respect_name, KEY_LENGTH_DEFAULT, check_operate_exist, adv_exist_message, exist_mode).capitalize()


def check_index_exist(index, nom_operateur=None):
    if nom_operateur is None:
        return index in OpModels.recupere_les_index_for_all()
    else:
        return index in OpModels.recupere_les_index_for_op(nom_operateur)

def take_index(exist_mode, sms, nom_operateur=None):
    end_adv = "un opérateur" if nom_operateur is None else f"l'opérateur '{nom_operateur}'"
    adv_message = "L'index '{valeur}' {existence_message} pour " + end_adv
    
    func_check_exist = lambda index : check_index_exist(index, nom_operateur)
    
    return FuncControllers.take_any(sms, check_respect_index, KEY_LENGTH_INDEX, func_check_exist, adv_message, exist_mode)

def take_entier_positif(sms):
    return FuncControllers.take_any(sms, FuncControllers.est_un_entier_pos, KEY_INT_POS)



def check_respect_index(index):
    return FuncControllers.est_un_entier_pos(index) and  MIN_INDEX <= int(index) <= MAX_INDEX

def check_operate_exist(name_op : str):
    return name_op.capitalize() in OpModels.recuperer_liste_operateur()


def create_new_op(choix):
    header_gestionnaire(choix)
    operateur = {}
    operateur["nom_operateur"] = take_nom_operateur(KEY_EXIST)
    operateur["tarif_ordinaire"] = take_entier_positif("Entrer le tarif ordinaire")
    operateur["tarif_different"] = take_entier_positif("Entrer le tarif pour les autres opérateurs")
    
    operateur["date_creation"] = FuncControllers.get_date()
    
    index = create_new_index("Entrer le premier index")
    
    OpModels.add_new_operateur(operateur)
    
    OpModels.add_new_index(index, operateur["nom_operateur"])
    
    FuncViews.succes_message(f"Operateur '{operateur['nom_operateur']}' créer avec succes")
    
    OpModels.update_registre(
        operateur["nom_operateur"],
        "ajout_index",
        operateur["date_creation"],
        f"Ajout d'un nouvel index '{index["index"]}' avec {NUM_GENERES} numéros"
    )
    
    FuncViews.continuer()


def create_new_index(sms="Entrer l'index"):
    first_index = {}
    first_index["index"] = take_index(KEY_EXIST, sms)
    first_index["liste_nums"] = generate_nums_for_index(first_index["index"])
    return first_index

def add_new_index(choix):
    header_gestionnaire(choix)
    
    nom_operateur = choisir_operateur()
    if len(OpModels.recupere_les_index_for_op(nom_operateur)) < LIMIT_NB_INDEX:
        new_index = create_new_index("Entrer le nouveau index")
        OpModels.add_new_index(new_index, nom_operateur)
        
        FuncViews.succes_message("Nouvelle index ajouté avec succès")
        
        OpModels.update_registre(
            nom_operateur,
            "ajout_index",
            FuncControllers.get_date(),
            f"Ajout d'un nouvel index '{new_index["index"]}' avec {NUM_GENERES} numéros"
        )
    else:
        FuncViews.error_message_simple(f"L'opérateur '{nom_operateur}' a déjà atteint le nombre limite d'index ({LIMIT_NB_INDEX}) !")
    FuncViews.continuer()

def rename_operate(choix):
    header_gestionnaire(choix)
    ancien_nom = choisir_operateur()
    nouveau_nom = take_nom_operateur(KEY_EXIST, "Saisir le nouveau nom")
    OpModels.rename_operate(ancien_nom, nouveau_nom)
    
    FuncViews.succes_message(f"Rennomé '{ancien_nom}' => '{nouveau_nom}'. Opération terminé")
    
    OpModels.update_registre(
        nouveau_nom,
        "rename_op",
        FuncControllers.get_date(),
        f"opérateur '{ancien_nom}' renommé en '{nouveau_nom}'"
    )
    
    FuncViews.continuer()

def vendre_numero(choix):
    header_gestionnaire(choix)
    nom_operateur = choisir_operateur()
    header_gestionnaire(choix)
    nom_index = choisir_index(nom_operateur)
    header_gestionnaire(choix)
    
    liste_nums = OpModels.collect_nums_index(nom_operateur, nom_index)
    header_gestionnaire(choix, 0)
    OpViews.tableau_numeros(liste_nums)
    
    choix_num = choisir_numero(liste_nums)
    numero = liste_nums[choix_num][0]
    FuncViews.succes_message(f"Vous avez choisi le numéro {FuncViews.formated_num(numero)}")
    
    if not FuncControllers.confirmer():
        return
    
    username = FuncControllers.take_name("Entrer un nom d'utilisateur")
    code_pin = take_code_pin_client("Entrer le code pin")
    
    if not FuncControllers.confirmer(f"Enregistrer le client '{username}' avec le numéro {FuncViews.formated_num(numero)} ?"):
        return
    
    client = dict(username=username, numero=numero,nom_operateur=nom_operateur, code_pin=code_pin)
    date = FuncControllers.get_date()
    OpModels.save_new_client(client, date)
    
    liste_nums[choix_num][1] = BOOL_NOT_DISPO
    index = dict(index=nom_index, liste_nums=liste_nums)
    
    OpModels.maj_index(index, nom_operateur)
    
    FuncViews.succes_message("Nouveau client ajouté avec succès")
    
    OpModels.update_registre(
        nom_operateur,
        "sell_num",
        date,
        f"numéro {numero} vendu au client '{username}'"
    )
    
    FuncViews.continuer()

def choisir_operateur(is_one_element=True, end_txt="index"):
    liste_operateurs = OpModels.recuperer_liste_operateur()
    len_op = len(liste_operateurs)

    if is_one_element and len_op == 1:
        op = liste_operateurs[0]
        FuncViews.afficher_en_couleur(f"Le seul opérateur disponible est [{op}]", style="bold blue on black")
        FuncViews.afficher_en_couleur(f"Vous serez diriger vers la liste de ses {end_txt}", style="bright_green")
        FuncViews.processing(TIME_LECTURE_UNIQUE)
        return op

    FuncViews.afficher_menu("Les opérateurs disponible", liste_operateurs)
    choix = FuncViews.take_choice(default="1")

    already_error = False
    while not FuncControllers.check_choix_in_marge(choix, maxi=len_op):
        FuncViews.processing(mode="error")
        choix = FuncViews.take_choice(mode_affichage="error", default="1", already_error=already_error)
        if not already_error:
            already_error = True

    FuncViews.processing()
    return liste_operateurs[int(choix) - 1]

def choisir_index(nom_operateur, is_one_element=True):
    liste_index = OpModels.recupere_les_index_for_op(nom_operateur)
    len_ind = len(liste_index)
    if is_one_element and len_ind == 1:
        ind = liste_index[0]
        FuncViews.afficher_en_couleur(f"Le seul index disponible est [{ind}]", style="bold blue on black")
        FuncViews.afficher_en_couleur("Vous serez diriger vers la liste de ses numéros", style="bright_green")
        FuncViews.processing(TIME_LECTURE_UNIQUE)
        return ind
    
    FuncViews.afficher_menu(f"Les index disponibles pour [{nom_operateur}]", liste_index,)
    choix = FuncViews.take_choice(default="1")
    already_error = False
    while not FuncControllers.check_choix_in_marge(choix, maxi=len_ind):
        FuncViews.processing(mode="error")
        choix = FuncViews.take_choice(mode_affichage="error", default="1", already_error=already_error)
        if not already_error:
            already_error = True
    
    FuncViews.processing()
    return liste_index[int(choix) - 1]

def choisir_numero(liste_nums):
    choix = FuncViews.take_choice("Votre choix", default="000")
    already_error = False
    
    while (not check_choix_numero(choix, liste_nums)):
        FuncViews.processing(mode="error")
        choix = FuncViews.take_choice(mode_affichage="error", already_error=already_error, default="000")
        if not already_error:
            already_error = True
    FuncViews.processing()
    return int(choix)-1

def check_choix_numero(choix, liste_nums):
    max_choice = len(liste_nums)
    if not FuncControllers.check_choix_in_marge(choix, max_choice):
        return False
    numero = liste_nums[int(choix)-1]
    return numero[1] == BOOL_DISPO


def check_code_pin(code_saisie):
    return FuncControllers.est_un_entier_pos(code_saisie) and len(code_saisie) == LENGTH_CODE_PIN

def take_code_pin_client(sms):
    code_pin = FuncViews.take_password(sms, default=CODE_PIN_DEFAULT)
    already_error = False
    while not check_code_pin(code_pin):
        FuncViews.processing(mode="error")
        adv = "Saisir un code pin correct"
        code_pin = FuncViews.take_password(sms, mode_affichage="error", default=CODE_PIN_DEFAULT, adv_sms=adv, already_error=already_error)
        if not already_error:
            already_error = True
    FuncViews.processing()
    return code_pin

def lister_operateurs_et_index(choix):
    header_gestionnaire(choix, 0)
    liste_op = OpModels.recuperer_liste_operateur()
    struct_op = {}
    for nom_operateur in liste_op:
        struct_op[nom_operateur] = OpModels.recupere_les_index_for_op(nom_operateur)
    OpViews.afficher_operateurs(struct_op)
    FuncViews.continuer()

def supprimer_index(choix):
    header_gestionnaire(choix)
    nom_operateur = choisir_operateur()
    index = take_index(KEY_NOT_EXIST, "Entrer l'index à supprimer", nom_operateur)
    if check_index_can_be_del(nom_operateur, index):
        OpModels.del_index(nom_operateur, index)
        FuncViews.succes_message(f"Index '{index}' supprimer avec succès")
        OpModels.update_registre(
            nom_operateur,
            "del_index",
            FuncControllers.get_date(),
            f"L'index '{index}' supprimé"
        )
    else:
        FuncViews.error_message_simple(f"Index '{index}' ne peut être supprimé")
    FuncViews.continuer()

def check_index_can_be_del(nom_operateur, index):
    liste_nums = OpModels.collect_nums_index(nom_operateur, index)
    for num in liste_nums:
        if num[1] == BOOL_NOT_DISPO:
            return False
    return True

def vendre_credit(choix):
    header_gestionnaire(choix)
    numero = FuncControllers.take_numero()
    credit = FuncControllers.take_credit()
    nom_operateur = FuncControllers.operateur_of_numero_client(numero)
    if nom_operateur:
        FuncViews.warning_message(f"Envoyé {credit} F CFA au {numero}")
        if not FuncControllers.confirmer():
            return
        
        date = FuncControllers.get_date()
        OpModels.ajouter_credit_client(numero, credit, date)
        
        OpModels.update_registre(
            nom_operateur,
            "sell_credit",
            date,
            f"Le client '{numero}' a pris {credit} crédits",
            value=credit
        )
        FuncViews.succes_message(f"{credit} crédits envoyé au client {numero}")
    else:
        FuncViews.error_message("Le numéro saisie n'est pas attribué")
    FuncViews.continuer()

def numeros_operateur(nom_operateur):
    liste_index = OpModels.recupere_les_index_for_op(nom_operateur)
    liste_nums = []
    for index in liste_index:
        liste_nums.extend(OpModels.collect_nums_index(nom_operateur, index))
    return liste_nums

def afficher_numeros_operateur(choix):
    header_gestionnaire(choix)
    nom_operateur = choisir_operateur(end_txt="numéros")
    header_gestionnaire(choix, 0)
    liste_nums = numeros_operateur(nom_operateur)
    OpViews.tableau_numeros(liste_nums)
    FuncViews.continuer()


def etat_caisse(choix):
    liste_op = OpModels.recuperer_liste_operateur()
    caisse_ops = {}
    for op in liste_op:
        caisse_ops[op] = OpModels.donnees_caisse(op)
    filtre_caisse_choix(caisse_ops, choix)

def filtre_caisse_choix(caisses_ops, choix, filtre = 'J'):
    ff_date = text_date = ""
    while filtre != 'Q':
        header_gestionnaire(choix, 0)
        caisses_op_filtrer = {}
        ff_date, text_date = get_ff_text_date(filtre)

        filtre_etat_caisse(caisses_ops, caisses_op_filtrer, ff_date)
        OpViews.etat_caisse(caisses_op_filtrer, subtitle=f"{text_date} {ff_date} / par opérateurs")
        filtre = take_choix_filtre()

def get_ff_text_date(filtre):
    today_date = FuncControllers.get_date("short")
    ff_date = text_date = ""
    if filtre == 'J':
        ff_date, text_date = today_date, "Journée"
    elif filtre == 'M':
        ff_date, text_date = today_date[3:], "Mois"
    elif filtre == 'A':
        ff_date, text_date = today_date[6:], "Année"
    return ff_date, text_date

def take_choix_filtre(sms="Filtres: (J)our, (M)ois, (A)nnée | (Q)uitter "):
    choices = ['J', 'M', 'A', 'Q']
    choix = FuncViews.take_choice(sms)
    already_error = False
    while choix.upper() not in choices:
        FuncViews.processing(mode="error")
        choix = FuncViews.take_choice(sms, mode_affichage="error", already_error=already_error)
        if not already_error:
            already_error = True
    if choix == 'Q':
        FuncViews.processing(2, go="back")
    else:
        FuncViews.processing()
    
    return choix.upper()

def filtre_etat_caisse(caisses_ops, caisses_op_filtrer, ff_date):
    for op, dates in caisses_ops.items():
        caisses_op_filtrer[op] = {'sell_credit': 0, 'sell_num': 0}
        for date, donnees in dates.items():
            if date.endswith(ff_date):
                caisses_op_filtrer[op]['sell_credit']+=donnees['sell_credit']
                caisses_op_filtrer[op]['sell_num']+=donnees['sell_num']
