# Operateur - Models
import os
from consts import (
    PATH_DB_OPERATEURS, FILE_INFO, BOOL_DISPO, DIR_INDEX, CHAR_INDEX, PATH_DB_CLIENTS,
    FILE_GESTIONNAIRES, FILE_REGISTRE
)

def add_new_operateur(operateur):
    path_file = os.path.join(PATH_DB_OPERATEURS, operateur["nom_operateur"])
    
    os.makedirs(path_file)
    
    file_info = os.path.join(path_file, FILE_INFO)
    
    with open(file_info, "w", encoding='utf-8') as f:
        f.write(f"nom opérateur : {operateur["nom_operateur"]}\n")
        f.write(f"date de création : {operateur["date_creation"]}\n")
        f.write(f"tarif ordinaire : {operateur["tarif_ordinaire"]}\n")
        f.write(f"tarif différent : {operateur["tarif_different"]}\n")
    
    file_registre = os.path.join(path_file, FILE_REGISTRE)
    with open(file_registre, "w", encoding='utf-8') as f:
        f.write(f"creation | {operateur["date_creation"]} | création de l'opérateur '{operateur["nom_operateur"]}'\n")

    path_index = os.path.join(path_file, DIR_INDEX)
    os.makedirs(path_index)


def update_registre(nom_operateur, type_update, date, commentaire, value=""):
    file_registre = os.path.join(PATH_DB_OPERATEURS, nom_operateur, FILE_REGISTRE)
    with open(file_registre, "a", encoding='utf-8') as f:
        if value:
            f.write(f"{type_update} | {date} | {value} | {commentaire}\n")
        else:
            f.write(f"{type_update} | {date} | {commentaire}\n")


def recupere_les_index_for_all():
    liste_operateur = os.listdir(PATH_DB_OPERATEURS)
    liste_index = []
    
    for nom_operateur in liste_operateur:
        liste_index.extend(recupere_les_index_for_op(nom_operateur))
    
    return liste_index

def recupere_les_index_for_op(nom_operateur):
    path_index = os.path.join(PATH_DB_OPERATEURS, nom_operateur, DIR_INDEX)
    
    les_index_txt = os.listdir(path_index)
    
    return [index[:CHAR_INDEX] for index in les_index_txt]


def add_new_index(index, nom_operateur):
    path_dir = os.path.join(PATH_DB_OPERATEURS, nom_operateur)
    file_index = os.path.join(path_dir, DIR_INDEX, f"{index["index"]}.txt")
    with open(file_index, "w", encoding='utf-8') as f:
        for numero in index["liste_nums"]:
            f.write(f"{numero} : {BOOL_DISPO}\n")

def maj_index(index, nom_operateur):
    file_index = os.path.join(PATH_DB_OPERATEURS, nom_operateur, DIR_INDEX, f"{index["index"]}.txt")
    with open(file_index, "w", encoding='utf-8') as f:
        for numero, etat in index["liste_nums"]:
            f.write(f"{numero} : {etat}\n")

def del_index(nom_operateur, index):
    file_index = os.path.join(PATH_DB_OPERATEURS, nom_operateur, DIR_INDEX, f"{index}.txt")
    os.remove(file_index)

def readlines_file(path_file):
    with open(path_file, 'r', encoding="utf-8") as f:
        lignes = f.readlines()
        return lignes

def write_file(path_file, lignes):
    with open(path_file, 'w', encoding="utf-8") as f:
        for ligne in lignes:
            f.write(ligne)

def rename_operate(ancien_nom, nouveau_nom):
    path_dir = rename_path(PATH_DB_OPERATEURS, ancien_nom, nouveau_nom)
    
    file_info = os.path.join(path_dir, FILE_INFO)
    
    lines_op = readlines_file(file_info)
    
    lines_op[0] = f"nom opérateur : {nouveau_nom}\n"
    
    write_file(file_info, lines_op)

def rename_path(start_path, last_end_path, new_end_path):
    path_ancien = os.path.join(start_path, last_end_path)

    path_nouveau = os.path.join(start_path, new_end_path)
    
    os.rename(path_ancien, path_nouveau)
    
    return path_nouveau


def collect_nums_index(nom_operateur, index):
    path_index = os.path.join(PATH_DB_OPERATEURS, nom_operateur, DIR_INDEX, f"{index}.txt")
    liste_nums = []
    with open(path_index, "r", encoding="utf-8") as f:
        for ligne in f:
            numero, etat = ligne.split(' : ')
            liste_nums.append([numero.strip(), etat.strip()])
    return liste_nums


def recuperer_liste_operateur():
    return os.listdir(PATH_DB_OPERATEURS)

def save_new_client(new_client):
    path_file = os.path.join(PATH_DB_CLIENTS, f"{new_client["numero"]}.txt")
    with open(path_file, 'w', encoding="utf-8") as f:
        f.write(f"nom : {new_client["nom"]}\n")
        f.write(f"numéro : {new_client["numero"]}\n")
        f.write(f"opérateur : {new_client["nom_operateur"]}\n")
        f.write(f"code pin : {new_client["code_pin"]}\n")
        f.write("crédit : 0\n")
        f.write("Liste des contacts :\n")
        f.write("liste des appels :\n")

def recupere_gestionnaires():
    path_file = FILE_GESTIONNAIRES
    with open(path_file, 'r', encoding="utf-8")as f:
        contenu = f.read()
    return contenu.splitlines()

def ajouter_credit_client(numero, credit):
    path_file = os.path.join(PATH_DB_CLIENTS, f"{numero}.txt")
    with open(path_file, 'r', encoding="utf-8")as f:
        lines = f.readlines()
    N = len(lines)
    for i in range(N):
        if lines[i].startswith("crédit :"):
            ancien_credit = int(lines[i].split(':')[1])
            nouveau_credit = ancien_credit + credit
            lines[i] = f"crédit : {nouveau_credit}\n"
            break
    
    with open(path_file, 'w', encoding="utf-8") as f:
        for i in range(N):
            f.write(lines[i])

def donnees_caisse(nom_operateur):
    path_file = os.path.join(PATH_DB_OPERATEURS, nom_operateur, FILE_REGISTRE)
    caisse = {}
    with open(path_file, 'r', encoding="utf-8") as f:
        for line in f:
            if line.startswith('sell_credit'):
                date, value = line.split(' | ')[1:3]
                date_jma = date.split(' ')[0]
                if date_jma not in caisse:
                    caisse[date_jma] = {'sell_credit': int(value), 'sell_num': 0}
                else:
                    caisse[date_jma]["sell_credit"]+=int(value)
            elif line.startswith('sell_num'):
                date = line.split(' | ')[1]
                date_jma = date.split(' ')[0]
                if date_jma not in caisse:
                    caisse[date_jma] = {'sell_credit': 0, 'sell_num': 1}
                else:
                    caisse[date_jma]["sell_num"]+=1
    return caisse