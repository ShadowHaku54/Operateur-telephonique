from consts import NUM_GENERES, MAX_CHAR_OP, MIN_CHAR_OP, MIN_INDEX, MAX_INDEX
from consts import KEY_EXIST, KEY_LENGTH_OP, KEY_NONE, KEY_NOT_EXIST, KEY_LENGTH_INDEX, KEY_INT_POS
import Controllers.Functions as FuncControllers
from Views import Functions as FuncViews
from Models import Operateur as OpModels
import random
from Views import Operateur as OpViews

def generate_nums_for_index(index : str):
        
    numeros = set()
    
    motifs_possibles = [
        lambda: f"{random.randint(1000, 9999)}{random.randint(100, 999)}",
        lambda: f"{random.randint(100, 999)}{random.randint(1000, 9999)}",
        lambda: f"{random.randint(100, 999)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(10, 99)}",
        lambda: f"{random.randint(10, 99)}{random.randint(0, 9)}{random.randint(10, 99)}{random.randint(0, 9)}{random.randint(0, 9)}"
    ]
    
    while len(numeros) <= NUM_GENERES:
        motif = random.choice(motifs_possibles)()
        numero = index+motif
        numeros.add(numero)
    
    return numeros


def take_any(sms, func_check_no_respect, func_check_exist=None, adv_exist_message="", exist_mode=KEY_NONE):
    
    existence_check = {
        KEY_EXIST : lambda nom: func_check_exist(nom),
        KEY_NOT_EXIST : lambda nom: not func_check_exist(nom),
        KEY_NONE : lambda nom: False,
    }
    
    
    valeur = OpViews.take_value(sms)
    
    no_respect = not func_check_no_respect(valeur)
    existence = existence_check[exist_mode](valeur)
    
    existence_message = FuncControllers.get_error_message(exist_mode)
    no_respect_message = FuncControllers.get_error_message(KEY_LENGTH_OP)
    
    while no_respect or existence:
        FuncViews.processing(type="error")
        
        adv = adv_exist_message.format(valeur=valeur, existence_message=existence_message) if existence else no_respect_message
        valeur = OpViews.take_value(
            sms, mode="error", advertissement = adv
        )
        
        no_respect = not func_check_no_respect(valeur)
        existence = existence_check[exist_mode](valeur)
    
    FuncViews.processing()
    
    return valeur

def take_nom_operateur(exist_mode, sms="Saisir le nom de l'opérateur"):
    adv_exist_message = "l'opérateur '{valeur}' {existence_message}"
    return take_any(sms, check_op, OpModels.check_operate_exist, adv_exist_message, exist_mode).capitalize()

def take_index(exist_mode, sms):
    adv_message = "L'index '{valeur}' {existence_message} pour un opérateur"
    return take_any(sms, check_index, OpModels.check_index_exist, adv_message, exist_mode)

def take_entier_positif(sms):
    return take_any(sms, FuncControllers.est_un_entierPos)

def check_op(nom_operateur):
    N = len(nom_operateur)
    return N >= MIN_CHAR_OP and N <= MAX_CHAR_OP


def check_index(index):
    return FuncControllers.est_un_entierPos(index) and  MIN_INDEX <= int(index) <= MAX_INDEX


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
    

