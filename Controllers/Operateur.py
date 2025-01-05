import random
from consts import NUM_GENERES, MAX_CHAR_OP, MIN_CHAR_OP, MIN_INDEX, MAX_INDEX, BOOl_DISPONIPLE
from consts import KEY_EXIST, KEY_LENGTH_OP, KEY_NONE, KEY_NOT_EXIST, KEY_LENGTH_INDEX, KEY_INT_POS, KEY_LENGTH_NUMB
from consts import COLOR_SECT_GESTION, MENUS_GESTIONNAIRE, PROMPT_END_CHOICE
from Controllers import Functions as FuncControllers
from Views import Functions as FuncViews, Operateur as OpViews
from Models import Operateur as OpModels

def generate_nums_for_index(index : str):
        
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
    
    return numeros


def take_any(sms, func_check_no_respect, no_respect_key, func_check_exist=None, adv_exist_message="", exist_mode=KEY_NONE):
    
    existence_check = {
        KEY_EXIST : lambda nom: func_check_exist(nom),
        KEY_NOT_EXIST : lambda nom: not func_check_exist(nom),
        KEY_NONE : lambda nom: False,
    }
    
    
    valeur = FuncViews.take_value(sms)
    
    no_respect = not func_check_no_respect(valeur)
    existence = existence_check[exist_mode](valeur)
    
    existence_message = FuncControllers.get_error_message(exist_mode)
    no_respect_message = FuncControllers.get_error_message(no_respect_key)
    
    already_error = False
    while no_respect or existence:
        FuncViews.processing(type="error")
        
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

def take_nom_operateur(exist_mode, sms="Saisir le nom de l'opérateur"):
    adv_exist_message = "l'opérateur '{valeur}' {existence_message}"
    return take_any(sms, check_respect_operateur, KEY_LENGTH_OP, check_operate_exist, adv_exist_message, exist_mode).capitalize()


def check_index_exist(index, nom_operateur=None):
    if nom_operateur is None:
        return index in OpModels.recupere_les_index_for_all()
    else:
        return index in OpModels.recupere_les_index_for_op(nom_operateur)

def take_index(exist_mode, sms, nom_operateur=None):
    end_adv = "un opérateur" if nom_operateur is None else f"l'opérateur '{nom_operateur}'"
    adv_message = "L'index '{valeur}' {existence_message} pour " + end_adv
    
    func_check_exist = lambda index : check_index_exist(index, nom_operateur)
    
    return take_any(sms, check_respect_index, KEY_LENGTH_INDEX, func_check_exist, adv_message, exist_mode)

def take_numero(exist_mode, sms="Saisir le numéro"):
    adv_message = "Le numéro '{valeur}' {existence_message}"
    return take_any(sms, check_repect_numero, KEY_LENGTH_NUMB, check_numero_exist_et_non_vendu)

def take_entier_positif(sms):
    return take_any(sms, FuncControllers.est_un_entierPos, KEY_INT_POS)

def check_respect_operateur(nom_operateur):
    N = len(nom_operateur)
    return N >= MIN_CHAR_OP and N <= MAX_CHAR_OP

def check_respect_index(index):
    return FuncControllers.est_un_entierPos(index) and  MIN_INDEX <= int(index) <= MAX_INDEX

def check_operate_exist(name_op : str):
    return name_op.capitalize() in OpModels.recuperer_liste_operateur()


def create_new_op():
    operateur = {}
    operateur["nom_operateur"] = take_nom_operateur(KEY_EXIST)
    FuncViews.lines_spaces(2)
    operateur["tarif_ordinaire"] = take_entier_positif("Entrer le tarif ordinaire")
    FuncViews.lines_spaces(2)
    operateur["tarif_different"] = take_entier_positif("Entrer le tarif pour les autres opérateurs")
    FuncViews.lines_spaces(2)
    
    operateur["date_creation"] = FuncControllers.get_date()
    
    operateur["first_index"] = create_new_index("Entrer le premier index")
    
    return operateur

def create_new_index(sms="Entrer l'index"):
    first_index = {}
    first_index["index"] = take_index(KEY_EXIST, sms)
    first_index["numeros"] = generate_nums_for_index(first_index["index"])
    first_index["date_creation"] = FuncControllers.get_date()
    return first_index

def add_new_op():
    operateur = create_new_op()
    OpModels.add_new_operateur(operateur)
    FuncViews.succes_message("Operateur créer avec succes")

def rename_operate():
    ancien_nom = take_nom_operateur(KEY_NOT_EXIST)
    nouveau_nom = take_nom_operateur(KEY_EXIST)
    OpModels.rename_operate(ancien_nom, nouveau_nom, FuncControllers.get_date())

def menu_gestionnaire_interactif():
    choices = FuncViews.afficher_menu("Menu principal : Gestion des Opérateurs", MENUS_GESTIONNAIRE)
    choix = FuncViews.take_choice(default="1")
    already_error = False
    while choix not in choices:
        FuncViews.processing(type="error")
        choix = FuncViews.take_choice(mode_affichage="error", default="1", already_error=already_error)
        if not already_error:
            already_error = True
    FuncViews.processing()
    return int(choix)

def vendre_numero():
    FuncViews.effacer_ecran()
    nom_operateur = choisir_operateur()
    FuncViews.effacer_ecran()
    index = choisir_index(nom_operateur)
    FuncViews.effacer_ecran()
    Liste_nums = OpModels.collect_index(nom_operateur, index)["liste_nums"]
    OpViews.tableau_deroulant_inteactif(Liste_nums)

def choisir_operateur():
    liste_operateurs = OpModels.recuperer_liste_operateur()
    if FuncControllers.if_list_contain_one_element(liste_operateurs):
        op = liste_operateurs[0]
        FuncViews.afficher_en_couleur(f"Le seul opérateur disponible est [{op}]", style="bold blue on black")
        FuncViews.afficher_en_couleur("Vous serez diriger vers la liste de ses index", style="bright_green")
        FuncViews.processing(6)
        return op
    
    choices = FuncViews.afficher_menu("Liste des opérateurs disponible", liste_operateurs)
    choix = FuncViews.take_choice(default="1")
    already_error = False
    while choix not in choices:
        FuncViews.processing(type="error")
        choix = FuncViews.take_choice(mode_affichage="error", default="1", already_error=already_error)
        if not already_error:
            already_error = True

    FuncViews.processing()
    return liste_operateurs[int(choix) - 1]

def choisir_index(nom_operateur):
    liste_index = OpModels.recupere_les_index_for_op(nom_operateur)
    
    if FuncControllers.if_list_contain_one_element(liste_index):
        ind = liste_index[0]
        FuncViews.afficher_en_couleur(f"Le seul index disponible est [{ind}]", style="bold blue on black")
        FuncViews.afficher_en_couleur("Vous serez diriger vers la liste de ses index", style="bright_green")
        FuncViews.processing(6)
        return ind
    
    choices = FuncViews.afficher_menu(f"Liste des index disponibles pour [{nom_operateur}]", liste_index,)
    choix = FuncViews.take_choice(default="1")
    already_error = False
    while choix not in choices:
        FuncViews.processing(type="error")
        choix = FuncViews.take_choice(mode_affichage="error", default="1", already_error=already_error)
        if not already_error:
            already_error = True
    
    FuncViews.processing()
    return liste_index[int(choix) - 1]

def check_numero_exist_et_non_vendu(numero_search, nom_operateur, index):
    liste_nums = OpModels.collect_index(nom_operateur, index)["liste_nums"]
    for numero, etat in liste_nums:
        if numero == numero_search:
            return etat == BOOl_DISPONIPLE
    return False

def check_repect_numero(numero : str):
    return numero.isdigit() and len(numero) == 9