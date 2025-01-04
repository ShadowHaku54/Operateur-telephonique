# Operateur - Models
import os
from consts import PATH_DB_OPERATEUR, NUM_GENERES, BOOl_DISPONIPLE, DIR_INDEX, CHAR_INDEX

def add_new_operateur(operateur):
    path_file = os.path.join(PATH_DB_OPERATEUR, operateur["nom_operateur"])
    
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


def recupere_les_index_for_all():
    liste_operateur = os.listdir(PATH_DB_OPERATEUR)
    liste_index = []
    
    for nom_operateur in liste_operateur:
        liste_index.extend(recupere_les_index_for_op(nom_operateur))
    
    return liste_index

def recupere_les_index_for_op(nom_operateur):
    path_index = os.path.join(PATH_DB_OPERATEUR, nom_operateur, DIR_INDEX)
    
    les_index_txt = os.listdir(path_index)
    
    return [index[:CHAR_INDEX] for index in les_index_txt]



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


def collect_index(nom_operateur, index):
    path_index = os.path.join(PATH_DB_OPERATEUR, nom_operateur, DIR_INDEX, f"{index}.txt")
    index_struct = {}
    liste_nums = []
    with open(path_index, "r", encoding="utf-8") as f:
        for ligne in f:
            if ligne.startswith("- "):
                numero, etat = ligne[2:].split(':')
                liste_nums.append([numero.strip(), etat.strip()])
            elif ligne.startswith("index : "):
                index_struct["index"] = last_part_str(ligne)
            elif ligne.startswith("date de création : "):
                index_struct["date_creation"] = last_part_str(ligne)
            elif ligne.startswith("numéro vendus : "):
                index_struct["num_sell"] = last_part_str(ligne)
            elif ligne.startswith("numéro disponibles : "):
                index_struct["num_dispo"] = last_part_str(ligne)
        index_struct["liste_nums"] = liste_nums
    return index_struct

def last_part_str(chaine, sep=":"):
    return chaine.split(sep, 1)[1].strip()

def recuperer_liste_operateur():
    return os.listdir(PATH_DB_OPERATEUR)



