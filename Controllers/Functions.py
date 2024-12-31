from datetime import datetime


def est_un_entierPos(value):
    return value.isdigit()


def get_date():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


