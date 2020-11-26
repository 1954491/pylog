#!/usr/bin/env python3

"""
crée des log avec l'information donné

Par Xavier Gagnon
"""
import pprint
import getpass
import datetime
import pyinputplus as pyin
import colorama
from colorama import Fore

colorama.init()

INITIALE = "[XG]"
MESSAGE_INVALIDE = Fore.YELLOW + INITIALE + Fore.RED + f" Lettre, chiffre, tiret," \
                                                       " espace et apostrophe seulement dans le nom svp" + Fore.RESET


def main() -> None:
    """Fonction principale"""
    print(Fore.YELLOW, INITIALE, Fore.RESET,
          "Svp, veuillez entrer votre message et facultativement son type et votre nom...")

    try:
        print()
        promp = (Fore.BLUE + "Message: " + Fore.RESET)
        message = pyin.inputStr(prompt=promp, limit=5)
        print()
        promp = (Fore.BLUE + "Type[" + Fore.YELLOW + "1" + Fore.BLUE + "]:\n" + Fore.RESET)
        typemessage = pyin.inputMenu(['notification', 'avertissement', 'erreur'],
                                     prompt=promp,
                                     numbered=True,
                                     default='notification')
        print()
        promp = (Fore.BLUE + "Utilisateur [" + Fore.YELLOW + getpass.getuser() + Fore.BLUE + "]: " + Fore.RESET)
        utilisateur = pyin.inputStr(prompt=promp, default=getpass.getuser(), blockRegexes=[("[^\\s',\\w\\-]",
                                                                                            MESSAGE_INVALIDE),
                                                                                           ("\\t",
                                                                                            MESSAGE_INVALIDE)])
        print()
        date = datetime.datetime.today()
        log = {'dateheure': str(date),
               'logtype': typemessage,
               'message': message,
               'utilisateur': utilisateur}
        pprint.pprint(log)
    except pyin.RetryLimitException as ex:
        print(Fore.YELLOW, INITIALE, Fore.RED, ex.__class__.__name__,
              Fore.YELLOW, ": la limite du nombre d'essais est atteinte")
        exit(1)


if __name__ == '__main__':
    main()
