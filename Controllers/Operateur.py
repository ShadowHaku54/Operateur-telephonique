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


def take_nom_operateur(exist_mode=KEY_NONE):
    
    existence_check = {
        KEY_EXIST : lambda nom: OpModels.check_operate_exist(nom),
        KEY_NOT_EXIST : lambda nom: not OpModels.check_operate_exist(nom),
        KEY_NONE : lambda nom: False,
    }
    
    message = "Saisir le nom de l'opérateur"
    
    nom_operateur = OpViews.take_value(message)
    
    no_respect = not check_op(nom_operateur)
    existence = existence_check[exist_mode](nom_operateur)
    
    existence_message = FuncControllers.get_error_message(exist_mode)
    no_respect_message = FuncControllers.get_error_message(KEY_LENGTH_OP)
    
    while no_respect or existence:
        FuncViews.processing(type="error")
        
        adv = f"l'opérateur '{nom_operateur}' {existence_message}" if existence else no_respect_message
        nom_operateur = OpViews.take_value(
            message, mode="error", advertissement = adv
        )
        
        no_respect = not check_op(nom_operateur)
        existence = existence_check[exist_mode][0](nom_operateur)
    
    FuncViews.processing()
    
    return nom_operateur.capitalize()

def check_op(nom_operateur):
    N = len(nom_operateur)
    return N >= MIN_CHAR_OP and N <= MAX_CHAR_OP

def take_entier_positif(sms):
    entier = OpViews.take_value(sms)
    no_respect = not FuncControllers.est_un_entierPos(entier)
    no_respect_message = FuncControllers.get_error_message(KEY_INT_POS)
    
    while no_respect:
        FuncViews.processing(type="error")
        
        entier = OpViews.take_value(
            sms, mode="error", advertissement = no_respect_message
        )
        
        no_respect = not FuncControllers.est_un_entierPos(entier)
    FuncViews.processing()
    return entier

def take_index(sms):
    index = OpViews.take_value(sms)
    
    no_respect = not check_index(index)
    existence = OpModels.check_index_exist(index)
    
    existence_message = FuncControllers.get_error_message(KEY_EXIST)
    no_respect_message = FuncControllers.get_error_message(KEY_LENGTH_INDEX)

    while no_respect or existence :
        FuncViews.processing(type="error")
        
        adv = f"L'index '{index}' {existence_message} pour un opérateur" if existence else no_respect_message
        index = OpViews.take_value(
            sms, mode="error", advertissement = adv
        )
        
        no_respect = not check_index(index)
        existence = OpModels.check_index_exist(index)
        
    FuncViews.processing()
    
    return index

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
    first_index["index"] = take_index(sms)
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
    
