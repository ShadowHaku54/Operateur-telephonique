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
    

def take_nom_operateur():
    message = "Saisir le nom de l'opérateur"
    
    nom_operateur = OpViews.take_value(message)
    
    while check_op(nom_operateur):
        FuncViews.processing(type="error")
        nom_operateur = OpViews.take_value(
            message, 
            mode="error", 
            advertissement=f"nombre de caractères compris entre [{MIN_CHAR_OP}-{MAX_CHAR_OP}]"
        )
    FuncViews.processing()
    return nom_operateur.capitalize()

def check_op(nom_operateur):
    N = len(nom_operateur)
    return N < MIN_CHAR_OP or N > MAX_CHAR_OP

def take_entier_positif(sms):
    entier = OpViews.take_value(sms)
    while not FuncControllers.est_un_entierPos(entier):
        FuncViews.processing(type="error")
        entier = OpViews.take_value(
            sms, mode="error", advertissement="un entier positif SVP !"
        )
    FuncViews.processing()
    return entier

def take_index(sms):        
    index = OpViews.take_value(sms)
    
    while not check_index(index):
        FuncViews.processing(type="error")
        index = OpViews.take_value(
            sms, mode="error", advertissement=f"entier compris entre [{MIN_INDEX}-{MAX_INDEX}]"
        )
    FuncViews.processing()
    return index

def check_index(index):
    return FuncControllers.est_un_entierPos(index) and  MIN_INDEX <= int(index) <= MAX_INDEX


def create_new_op():
    operateur = {}
    operateur["nom_operateur"] = take_nom_operateur()
    FuncViews.lines_spaces(2)
    operateur["tarif_ordinaire"] = take_entier_positif("Entrer le tarif ordinaire")
    FuncViews.lines_spaces(2)
    operateur["tarif_different"] = take_entier_positif("Entrer le tarif pour les autres opérateurs")
    FuncViews.lines_spaces(2)
    
    operateur["date_creation"] = FuncControllers.get_date()
    
    first_index = {}
    first_index["index"] = take_index("Entrer le premier index")
    FuncViews.lines_spaces(2)
    first_index["numeros"] = generate_nums_for_index(first_index["index"])
    
    operateur["first_index"] = first_index
    return operateur

def add_new_op():
    operateur = create_new_op()
    while (OpModels.add_new_operateur(operateur) != 0):
        FuncViews.error_message("L'opérateur existe déjà")
        operateur = create_new_op()
    FuncViews.succes_message("Operateur créer avec succes")
    print("OK")
