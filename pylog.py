#!/usr/bin/env python3

"""
crée des log avec l'information donné

Par Xavier Gagnon
"""
import pprint
import argparse
import getpass
import datetime
import pyinputplus as pyin
import re
import colorama
from colorama import Fore

colorama.init()

INITIALE = "[XG]"
MESSAGE_INVALIDE = Fore.YELLOW + INITIALE + Fore.RED + f" Lettre, chiffre, tiret," \
                                                       " espace et apostrophe seulement dans le nom svp" + Fore.RESET
OPTION_TYPE_MESSAGE = ['notification', 'avertissement', 'erreur']
REGEX_TAB = "\\t"
REGEX_CHAR_INVALIDE = "[^\\s',\\w\\-]"


def main() -> None:
    """Fonction principale"""
    args = args_parse()

    try:
        typemessage = ajout_type(args.type)
        utilisateur = verifier_user(args.utilisateur)
        message = ' '.join(args.message)
        if len(args.message) == 0:
            print(Fore.YELLOW, INITIALE, Fore.RESET,
                  "Svp, veuillez entrer votre message et facultativement son type et votre nom...")
            print()
            promp = (Fore.BLUE + "Message: " + Fore.RESET)
            message = pyin.inputStr(prompt=promp, limit=5)
            print()
            promp = (Fore.BLUE + "Type[" + Fore.YELLOW + "1" + Fore.BLUE + "]:\n" + Fore.RESET)
            typemessage = pyin.inputMenu(OPTION_TYPE_MESSAGE,
                                         prompt=promp,
                                         numbered=True,
                                         blank=True)
            print()
            promp = (Fore.BLUE + "Utilisateur [" + Fore.YELLOW + getpass.getuser() + Fore.BLUE + "]: " + Fore.RESET)
            utilisateur = pyin.inputStr(prompt=promp, blank=True, blockRegexes=[(REGEX_CHAR_INVALIDE,
                                                                                 MESSAGE_INVALIDE),
                                                                                (REGEX_TAB,
                                                                                 MESSAGE_INVALIDE)])
        print_log(typemessage, message, utilisateur)
    except pyin.RetryLimitException as ex:
        print(Fore.YELLOW, INITIALE, Fore.RED, ex.__class__.__name__,
              Fore.YELLOW, ": la limite du nombre d'essais est atteinte")
        exit(1)
    except ValueError as ex:
        print(Fore.YELLOW, INITIALE, " ", Fore.RED, ex.__class__.__name__,
              Fore.YELLOW, ": Lettre, chiffre, tirets, espaces, et apostrophe seulement dans le nom svp", sep="")
        exit(1)


def ajout_type(arg) -> str:
    """Met le type en format long si nécéssaire"""
    typemessage = arg
    if len(typemessage) == 1:

        for typedifferent in OPTION_TYPE_MESSAGE:
            if typemessage == typedifferent[0]:
                typemessage = typedifferent
    return typemessage


def verifier_user(utilisateur) -> str:
    """Vérifier si le nom d'utilisateur est accepter"""
    if re.search(REGEX_CHAR_INVALIDE, utilisateur) is not None or re.search(REGEX_TAB, utilisateur) is not None:
        raise ValueError()
    return utilisateur


def print_log(typemessage, message, utilisateur) -> None:
    """Écrie le log sur la console"""
    print()
    if typemessage == "":
        typemessage = OPTION_TYPE_MESSAGE[0]

    if utilisateur == "":
        utilisateur = getpass.getuser()

    date = datetime.datetime.today()
    log = {'dateheure': str(date),
           'logtype': typemessage,
           'message': message,
           'utilisateur': utilisateur}
    pprint.pprint(log)


def args_parse() -> argparse.Namespace:
    """Fonction qui parse les arguments"""
    parser = argparse.ArgumentParser(description="Commande pour journaliser un message -- ©2020, par Xavier Gagnon",
                                     epilog="PS si aucun argument n'est fourni, il vous seront demandés.")
    parser.add_argument('-t',
                        metavar='{n,a,e}',
                        dest='type',
                        choices=['n', 'a', 'e'],
                        help='type de log',
                        default='notification',
                        type=str)
    parser.add_argument('--type',
                        metavar='{notification,avertissement,erreur}',
                        dest='type',
                        choices=['notification', 'avertissement', 'erreur'],
                        default='notification',
                        help='type de log',
                        type=str)
    parser.add_argument('-u', '--user',
                        metavar='USER',
                        help="Nom de l'utilisateur",
                        dest='utilisateur',
                        default=getpass.getuser(),
                        type=str)
    parser.add_argument('message',
                        metavar='message',
                        help='Message à journalier',
                        type=str,
                        nargs='*')
    return parser.parse_args()


if __name__ == '__main__':
    main()
