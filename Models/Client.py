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
    return recuperer_element_in_file(numero, "code pin : ")