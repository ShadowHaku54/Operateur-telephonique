# Client - Models
import os
from consts import PATH_DB_CLIENTS, FILE_CONTACTS, FILE_HISTORIQUE, FILE_INFO, FILE_REGISTRE

def recuperer_numeros():
    return os.listdir(PATH_DB_CLIENTS)


def update_credit_client(numero, credit, add=True):
    path_file = os.path.join(PATH_DB_CLIENTS, numero, FILE_INFO)
    with open(path_file, 'r', encoding="utf-8")as f:
        lines = f.readlines()

    N = len(lines)
    for i in range(N):
        if lines[i].startswith("crédit :"):
            if add:
                ancien_credit = float(lines[i].split(':')[1])
                nouveau_credit = ancien_credit + credit
                lines[i] = f"crédit : {nouveau_credit}\n"
            else:
                lines[i] = f"crédit : {credit}\n"
            break
    
    with open(path_file, 'w', encoding="utf-8") as f:
        for i in range(N):
            f.write(lines[i])


def recuperer_element_in_file(numero, element):
    path_file = os.path.join(PATH_DB_CLIENTS, numero, FILE_INFO)
    with open(path_file, 'r', encoding="utf-8") as f:
        line = f.readline()
        while line and not line.startswith(element):
            line = f.readline()

    return line.split(":")[1].strip()

def recuperer_op_for_num(numero):
    return recuperer_element_in_file(numero, "opérateur :")

def recuperer_code_pin(numero):
    return recuperer_element_in_file(numero, "code pin :")

def recuperer_credit(numero):
    return float(recuperer_element_in_file(numero, "crédit :"))

def update_registre(numero, type_update, date, commentaire):
    file_registre = os.path.join(PATH_DB_CLIENTS, numero, FILE_REGISTRE)
    with open(file_registre, "a", encoding='utf-8') as f:
        f.write(f"{type_update} | {date} | {commentaire}\n")
        

def recuperer_contacts(numero):
    path_file = os.path.join(PATH_DB_CLIENTS, numero, FILE_CONTACTS)
    contacts = {}
    with open(path_file, 'r', encoding="utf-8") as f:
        for line in f:
            ff_ligne = sup_char_retour_line(line)
            nom_contact, flag, liste_nums = ff_ligne.split(' | ')
            contacts[nom_contact] = {"flag": flag, "liste_nums": liste_nums.split(', ')}
    return contacts


def sup_char_retour_line(chaine):
    if chaine[-1] == '\n':
        return chaine[:-1]
    return chaine
