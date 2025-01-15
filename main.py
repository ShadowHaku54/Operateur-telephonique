from Controllers.Functions import log_in, aurevoir
from Controllers.Operateur import use_case_gestionnaire
from Controllers.Client import use_case_client, define_client

def main():
    quitter = False
    while not quitter:
        user = log_in()
        if user["is_client"]:
            define_client(user["login"])
            quitter = use_case_client()
        else:
            quitter = use_case_gestionnaire()
    aurevoir()

if __name__ == "__main__":
    main()
