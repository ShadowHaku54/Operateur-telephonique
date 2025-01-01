from consts import PATH_DB_OPERATEUR, NUM_GENERES, BOOl_DISPONIPLE, BOOL_INDISPONIBLE, DIR_INDEX, CHAR_INDEX
import os

def add_new_operateur(operateur : dict):
    
    path_file = os.path.join(PATH_DB_OPERATEUR, operateur["nom_operateur"])
    
    if os.path.exists(path_file):
        return 1
    
    os.makedirs(path_file)
    
    file_info = f"{os.path.join(path_file, operateur["nom_operateur"])}.txt"
    
    with open(file_info, "w", encoding='utf-8') as f:
        f.write(f"nom opérateur : {operateur["nom_operateur"]}\n")
        f.write(f"date de création : {operateur["date_creation"]}\n")
        f.write(f"date de modification : {operateur["date_creation"]}\n")
        f.write(f"tarif ordinaire : {operateur["tarif_ordinaire"]}\n")
        f.write(f"tarif différent : {operateur["tarif_different"]}\n")

    path_index = os.path.join(path_file, DIR_INDEX)
    os.makedirs(path_index)
    add_new_index(operateur["first_index"], operateur["nom_operateur"])
    
    return 0

def check_operate_exist(name_op):
    path_file = os.path.join(PATH_DB_OPERATEUR, name_op)
    return os.path.exists(path_file)

def check_index_exist(index):
    return index in recupere_les_index()

def recupere_les_index():
    liste_operateur = os.listdir(PATH_DB_OPERATEUR)
    liste_index = []
    
    for nom_operateur in liste_operateur:
        
        path_index = os.path.join(PATH_DB_OPERATEUR, nom_operateur, DIR_INDEX)
        
        les_index_txt = os.listdir(path_index)
        
        liste_index.extend([index[:CHAR_INDEX] for index in les_index_txt])
        
    return liste_index

def add_new_index(index , nom_operateur):
    
    file_index = f"{os.path.join(PATH_DB_OPERATEUR, nom_operateur, DIR_INDEX, index["index"])}.txt"
    
    with open(file_index, "w", encoding='utf-8') as f:
        f.write(f"index : {index["index"]}\n")
        f.write(f"date de création : {index["date_creation"]}\n")
        f.write("numéro vendus : 0\n")
        f.write(f"numéro disponibles : {NUM_GENERES}\n")
        f.write("liste des numéros : \n")
        
        for numero in index["numeros"]:
            f.write(f"- {numero} : {BOOl_DISPONIPLE}\n")
            
    return 0

def readlines_file(path_file):
    with open(path_file, 'r', encoding="utf-8") as f:
        lignes = f.readlines()
        return lignes

def write_file(path_file, lignes):
    with open(path_file, 'w', encoding="utf-8") as f:
        for ligne in lignes:
            f.write(ligne)

def rename_operate(ancien_nom, nouveau_nom, date_modification):
    path_dir = rename_path(PATH_DB_OPERATEUR, ancien_nom, nouveau_nom)
    
    path_file = rename_path(path_dir, f"{ancien_nom}.txt", f"{nouveau_nom}.txt")
    
    lines_op = readlines_file(path_file)
    
    lines_op[0] = f"nom opérateur : {nouveau_nom}\n"
    lines_op[2] = f"date de modification : {date_modification}\n"
    
    write_file(path_file, lines_op)

def rename_path(start_path, last_end_path, new_end_path):
    path_ancien = os.path.join(start_path, last_end_path)

    path_nouveau = os.path.join(start_path, new_end_path)
    
    os.rename(path_ancien, path_nouveau)
    
    return path_nouveau