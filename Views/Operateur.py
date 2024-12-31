from Views import Functions as FuncViews

    
def take_value(message, mode="simple", advertissement = ""):
    
    def saisie_simple(message):
        return FuncViews.lire(f"{message} :")

    def saisie_error(message):
        FuncViews.remonter_ligne(2)
        sms_error = FuncViews.styliser_texte("Erreur!", "rouge")
        sms_signalement = FuncViews.styliser_texte(advertissement, "jaune")
        return FuncViews.lire(f"{sms_error} {message} ({sms_signalement}) :")

    actions = {
        "simple": saisie_simple,
        "error": saisie_error,
    }

    action = actions.get(mode, saisie_simple)
    return action(message)