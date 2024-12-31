from consts import PATH_DB_OPERATEUR, NUM_GENERES, BOOl_DISPONIPLE, BOOL_INDISPONIBLE
import os

def add_new_operateur(operateur : dict):
    
    path_file = os.path.join(PATH_DB_OPERATEUR, operateur["nom_operateur"])
    
    if os.path.exists(path_file):
        return 1
    
    os.makedirs(path_file)
    
    file_info = f"{os.path.join(path_file, operateur["nom_operateur"])}.txt"
    
    with open(file_info, "w", encoding='utf-8') as f:
        f.write(f"nom : {operateur["nom_operateur"]}\n")
        f.write(f"date de création : {operateur["date_creation"]}\n")
        f.write(f"tarif ordinaire : {operateur["tarif_ordinaire"]}\n")
        f.write(f"tarif différent : {operateur["tarif_different"]}\n")

    path_index = os.path.join(path_file, "Index")
    os.makedirs(path_index)
    add_new_index(operateur["first_index"], operateur["nom_operateur"])
    return 0


def add_new_index(index : dict, nom_operateur : str):
    path_operateur = os.path.join(PATH_DB_OPERATEUR, nom_operateur)
    
    if not os.path.exists(path_operateur):
        return 1
    
    file_index = f"{os.path.join(PATH_DB_OPERATEUR, nom_operateur, "Index", index["index"])}.txt"
    
    if os.path.exists(file_index):
        return -1
    
    with open(file_index, "w", encoding='utf-8') as f:
        f.write(f"index : {index["index"]}\n")
        f.write("numéro vendus : 0\n")
        f.write(f"numéro disponibles : {NUM_GENERES}\n")
        f.write("liste des numéros : \n")
        
        for numero in index["numeros"]:
            f.write(f"- {numero} : {BOOl_DISPONIPLE}\n")
    return 0
