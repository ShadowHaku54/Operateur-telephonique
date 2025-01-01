from consts import NUM_GENERES, MAX_CHAR_OP, MIN_CHAR_OP, MIN_INDEX, MAX_INDEX
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
    

def take_nom_operateur(exist_mode="none"):
    
    existence_check = {
        "exist" : (lambda nom: OpModels.check_operate_exist(nom), "existe déjà"),
        "not_exist" : (lambda nom: not OpModels.check_operate_exist(nom), "n'existe pas"),
        "none" : (lambda nom: False, "")
    }
    
    message = "Saisir le nom de l'opérateur"
    
    nom_operateur = OpViews.take_value(message)
    
    no_respect = not check_op(nom_operateur)
    existence = existence_check[exist_mode][0](nom_operateur)
    existence_message = existence_check[exist_mode][1]
    
    while no_respect or existence:
        
        if existence:
            adv = f"l'opérateur '{nom_operateur}' {existence_message}"
        else:
            adv = f"nombre de caractères compris entre [{MIN_CHAR_OP}-{MAX_CHAR_OP}]"
        
        FuncViews.processing(type="error")
        nom_operateur = OpViews.take_value(
            message,
            mode="error",
            advertissement = adv
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
    while not FuncControllers.est_un_entierPos(entier):
        FuncViews.processing(type="error")
        entier = OpViews.take_value(
            sms, mode="error", advertissement = "un entier positif SVP !"
        )
    FuncViews.processing()
    return entier

def take_index(sms):        
    index = OpViews.take_value(sms)
    
    no_respect = not check_index(index)
    existance = OpModels.check_index_exist(index) 

    while no_respect or existance :
        if (existance) :
            adv = "Cet index existe déjà pour un opérateur"
        else:
            adv = f"entier compris entre [{MIN_INDEX}-{MAX_INDEX}]"
            
        FuncViews.processing(type="error")
        index = OpViews.take_value(
            sms, mode="error", advertissement = adv
        )
        no_respect = not check_index(index)
        existance = OpModels.check_index_exist(index)
        
    FuncViews.processing()
    
    return index

def check_index(index):
    return FuncControllers.est_un_entierPos(index) and  MIN_INDEX <= int(index) <= MAX_INDEX


def create_new_op():
    operateur = {}
    operateur["nom_operateur"] = take_nom_operateur(exist_mode="exist")
    FuncViews.lines_spaces(2)
    operateur["tarif_ordinaire"] = take_entier_positif("Entrer le tarif ordinaire")
    FuncViews.lines_spaces(2)
    operateur["tarif_different"] = take_entier_positif("Entrer le tarif pour les autres opérateurs")
    FuncViews.lines_spaces(2)
    
    operateur["date_creation"] = FuncControllers.get_date()
    
    operateur["first_index"] = create_new_index("le premier ")
    
    return operateur

def create_new_index(sms="l'"):
    first_index = {}
    first_index["index"] = take_index(f"Entrer {sms}index")
    first_index["numeros"] = generate_nums_for_index(first_index["index"])
    first_index["date_creation"] = FuncControllers.get_date()
    return first_index

def add_new_op():
    operateur = create_new_op()
    OpModels.add_new_operateur(operateur)
    FuncViews.succes_message("Operateur créer avec succes")
    

def rename_operate():
    ancien_nom = take_nom_operateur("not_exist")
    nouveau_nom = take_nom_operateur("exist")
    OpModels.rename_operate(ancien_nom, nouveau_nom, FuncControllers.get_date())