from datetime import datetime
from consts import ERROR_MESSAGES, KEY_NOT_FOUND


def est_un_entierPos(value):
    return value.isdigit()


def get_date():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def get_error_message(key):
    if key in ERROR_MESSAGES:
        return ERROR_MESSAGES[key]
    return ERROR_MESSAGES[KEY_NOT_FOUND]

