# Client - Models
import os
from consts import PATH_DB_CLIENTS

def recuperer_numeros():
    path_file = PATH_DB_CLIENTS
    liste_nums = []
    for dir_client in os.listdir(path_file):
        numero = dir_client.split('.')[0]
        liste_nums.append(numero)
    return liste_nums

def update_credit_client(numero, credit, add=True):
    path_file = os.path.join(PATH_DB_CLIENTS, f"{numero}.txt")
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
    path_file = os.path.join(PATH_DB_CLIENTS, f"{numero}.txt")
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