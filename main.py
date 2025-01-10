from Controllers import Operateur as OpControllers
from Controllers.Functions import log_in, menu_gestionnaire_interactif
from Controllers.Operateur import use_case_gestionnaire
from Controllers.Client import use_case_client
from consts import (
    MENU_GESTIONNAIRE, USER_GESTIONNAIRE, COLOR_USER_GESTION, 
    MENU_CLIENT, USER_CLIENT, COLOR_SECT_CLIENT
)

def main():
    len_menu_gest = len(MENU_GESTIONNAIRE)
    len_menu_client = len(MENU_CLIENT)
    while True:
        user = log_in()
        if user["is_client"]:
            while True:
                choix = menu_gestionnaire_interactif("Menu principal : ", MENU_CLIENT, USER_CLIENT, COLOR_SECT_CLIENT)
                if choix == len_menu_client-1:
                    return
                elif choix == len_menu_client-2:
                    break
                use_case_client(choix)
        else:
            while True:
                choix = menu_gestionnaire_interactif("Menu principal : Gestion des Opérateurs", MENU_GESTIONNAIRE, USER_GESTIONNAIRE, COLOR_USER_GESTION)
                if choix == len_menu_gest-1:
                    return
                elif choix == len_menu_gest-2:
                    break
                use_case_gestionnaire(choix)

if __name__ == "__main__":
    main()
