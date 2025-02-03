import os
import threading
import time
import numpy as np
import sounddevice as sd
import soundfile as sf

from consts import (
    PATH_DB_CLIENTS, FILE_CONTACTS, FILE_HISTORIQUE, FILE_INFO, 
    FILE_REGISTRE, PATH_DB_OPERATEURS, PATH_DB_VOCAUX,
    IS_NOT_ALREADY_READ,  APPEL_ENTRANT, APPEL_SORTANT,
    NB_NUMBER_AFTER_COMMA
    )

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
    repertoire = []
    with open(path_file, 'r', encoding="utf-8") as f:
        for line in f:
            ff_ligne = sup_char_retour_line(line)
            nom_contact, flag, liste_nums = ff_ligne.split(' | ')
            repertoire.append(dict(nom_contact=nom_contact, flag=flag, liste_nums=liste_nums.split(', ')))
    return repertoire


def sup_char_retour_line(chaine):
    if chaine[-1] == '\n':
        return chaine[:-1]
    return chaine

def ajouter_contact(numero_client, contact):
    path_file = os.path.join(PATH_DB_CLIENTS, numero_client, FILE_CONTACTS)
    with open(path_file, 'a', encoding="utf-8") as f:
        f.write(f"{contact["nom_contact"]} | {contact["flag"]} | {", ".join(contact["liste_nums"])}\n")

def update_repertoire(numero_client, repertoire):
    path_file = os.path.join(PATH_DB_CLIENTS, numero_client, FILE_CONTACTS)
    with open(path_file, 'w', encoding="utf-8") as f:
        for contact in repertoire:
            f.write(f"{contact["nom_contact"]} | {contact["flag"]} | {", ".join(contact["liste_nums"])}\n")
            

def select_tarif_op(nom_operateur, type_tf="ordinaire"):
    type_tarif = {
        "ordinaire": "tarif ordinaire : ",
        "different": "tarif différent : "
    }
    
    path_file = os.path.join(PATH_DB_OPERATEURS, nom_operateur, FILE_INFO)
    
    with open(path_file, 'r', encoding="utf-8") as f:
        for line in f:
            if line.startswith(type_tarif[type_tf]):
                return int(line.split(" : ")[1])


def enregistrer_vocal_wav(nom_fichier, duree):
    file_voc = os.path.join(PATH_DB_VOCAUX, nom_fichier)
    fs = 44100 
    buffer = []
    stop_event = threading.Event()

    def callback(indata, frames, time_info, status):
        if stop_event.is_set():
            raise sd.CallbackStop()
        buffer.extend(indata.copy())

    def attendre_arret_utilisateur():
        input()
        stop_event.set()

    start_time = time.time()

    with sd.InputStream(callback=callback, samplerate=fs, channels=1):
        arret_thread = threading.Thread(target=attendre_arret_utilisateur, daemon=True)
        arret_thread.start()
        stop_event.wait(duree)

    sf.write(file_voc, np.array(buffer), fs)
    end_time = time.time()
    duration = end_time - start_time
    
    return round(duration, NB_NUMBER_AFTER_COMMA)

def lire_audio_avec_arret(nom_fichier):
    stop_event = threading.Event()
    user_input = [None]

    def attendre_arret_utilisateur():
        user_input[0] = input()
        stop_event.set()

    data, samplerate = sf.read(nom_fichier)

    def lire_audio():
        with sd.OutputStream(samplerate=samplerate, channels=data.shape[1] if len(data.shape) > 1 else 1):
            sd.play(data, samplerate)
            while not stop_event.is_set() and sd.get_stream().active:
                sd.sleep(100)
            sd.stop()

    threading.Thread(target=attendre_arret_utilisateur, daemon=True).start()
    lire_audio()

    return user_input[0]


def lire_audio_fin(nom_fichier):
    data, samplerate = sf.read(nom_fichier)
    sd.play(data, samplerate)
    sd.wait()

def lire_vocal(fic_vocal):
    file_vocal = os.path.join(PATH_DB_VOCAUX, fic_vocal)
    lire_audio_avec_arret(file_vocal)

def update_historique(nom_fichier, numero_sortant, numero_entrant, date, durre, cout_appel):
    path_file_in = os.path.join(PATH_DB_CLIENTS, numero_entrant, FILE_HISTORIQUE)
    path_file_out = os.path.join(PATH_DB_CLIENTS, numero_sortant, FILE_HISTORIQUE)
    with open(path_file_in, 'a', encoding="utf-8") as file_in, open(path_file_out, 'a', encoding="utf8") as file_out:
        file_out.write(f"{APPEL_SORTANT} | {date} | {numero_entrant} | {durre} | {nom_fichier} | {cout_appel} | {IS_NOT_ALREADY_READ}\n")
        file_in.write(f"{APPEL_ENTRANT} | {date} | {numero_sortant} | {durre} | {nom_fichier} | -- | {IS_NOT_ALREADY_READ}\n")


def collect_historique(numero):
    path_file = os.path.join(PATH_DB_CLIENTS, numero, FILE_HISTORIQUE)
    historique = []
    with open(path_file, 'r', encoding="utf-8") as f:
        for line in f:
            line = sup_char_retour_line(line)
            type_appel, date_long, numero_appel, duree, fic_voc, cout, vue = line.split(' | ')
            date_day, date_heure = date_long.split()
            historique.append(dict(
                type_appel=type_appel,
                date_day=date_day,
                date_heure=date_heure,
                numero_appel=numero_appel,
                duree=duree,
                fic_voc=fic_voc,
                cout=cout,
                vue=vue
            ))
    return historique

def update_historique_for_ecoute(numero, historique):
    file_historique = os.path.join(PATH_DB_CLIENTS, numero, FILE_HISTORIQUE)
    with open(file_historique, 'w', encoding="utf-8") as f:
        for vocal in historique:
            type_appel, date_day, date_heure, numero_appel, duree, fic_voc, cout, vue = vocal.values()
            f.write(f"{type_appel} | {date_day} {date_heure} | {numero_appel} | {duree} | {fic_voc} | {cout} | {vue}\n")