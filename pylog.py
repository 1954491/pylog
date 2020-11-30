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
import csv
import os
import re
from tabulate import tabulate
import colorama
from colorama import Fore

colorama.init()

INITIALE = "[XG]"
MESSAGE_INVALIDE = Fore.YELLOW + INITIALE + Fore.RED + f" Lettre, chiffre, tiret," \
                                                       " espace et apostrophe seulement dans le nom svp" + Fore.RESET
OPTION_TYPE_MESSAGE = ['notification', 'avertissement', 'erreur']
REGEX_TAB = "\\t"
REGEX_CHAR_INVALIDE = "[^\\s'\\.,\\w\\-]"
USAGE = "usage: pylog.py [-h] [-l] [-t{n,a,e}] [--type {notification, avertissement, erreur}] [-u USER] [message [" \
        "message ...]] "


def main() -> None:
    """Fonction principale"""
    args = args_parse()

    if args.liste or args.browse:
        if len(args.message) > 0:
            affichererreur("ArgumentError")
        afficher_log(args)
    else:
        if len(args.message) == 0:
            affichererreur("ArgumentError")
        print(Fore.YELLOW, INITIALE, Fore.RESET,
              "Svp, veuillez entrer votre message et facultativement son type et votre nom...\n")
        main_log(args)


def affichererreur(nomerreur) -> None:
    """Affiche l'erreur"""
    print(USAGE)
    print(Fore.YELLOW, INITIALE, Fore.RED, nomerreur, Fore.YELLOW, ": Il faut spécifier un et un seul argument parmi: "
                                                                   "-l, message",
          Fore.RESET, sep="")
    exit(1)


def afficher_log(args) -> None:
    """Afficher les logs sauvgardée"""
    fichier = open("pylog.tsv", "r").readlines()
    doc = []
    for ligne in fichier:
        doc.append(ligne.split('\t'))
        print(doc)
    if args.browse:
        print(tabulate(doc, headers="firstrow", tablefmt="html"))
    else:
        print(tabulate(doc, headers="firstrow"))


def main_log(args) -> None:
    """Ecrit un log dans le fichier log"""
    try:
        ajout_log(args)
    except pyin.RetryLimitException as ex:
        print(Fore.YELLOW, INITIALE, Fore.RED, ex.__class__.__name__,
              Fore.YELLOW, ": la limite du nombre d'essais est atteinte")
        exit(1)
    except ValueError as ex:
        print(Fore.YELLOW, INITIALE, " ", Fore.RED, ex.__class__.__name__,
              Fore.YELLOW, ": Lettre, chiffre, tirets, espaces, et apostrophe seulement dans le nom svp", sep="")
        exit(1)


def ajout_log(args) -> None:
    """crée le log"""
    typemessage = ajout_type(args.type)
    utilisateur = verifier_user(args.utilisateur)
    message = ' '.join(args.message)
    if len(args.message) == 0:
        message = pyin.inputStr(prompt=Fore.BLUE + "Message: \n" + Fore.RESET, limit=5)
        promp = (Fore.BLUE + "Type[" + Fore.YELLOW + "1" + Fore.BLUE + "]:\n" + Fore.RESET)
        typemessage = pyin.inputMenu(OPTION_TYPE_MESSAGE, prompt=promp, numbered=True, blank=True)
        promp = (Fore.BLUE + "Utilisateur [" + Fore.YELLOW + getpass.getuser() + Fore.BLUE + "]: \n" + Fore.RESET)
        utilisateur = pyin.inputStr(prompt=promp, blank=True,
                                    blockRegexes=[(REGEX_CHAR_INVALIDE, MESSAGE_INVALIDE),
                                                  (REGEX_TAB, MESSAGE_INVALIDE)])
    print_log(typemessage, message, utilisateur)


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
    log = {'dateheure': str(date), 'logtype': typemessage, 'message': message, 'utilisateur': utilisateur}
    pprint.pprint(log)
    fichierexiste = False
    if os.path.exists("pylog.tsv"):
        fichierexiste = True
    try:
        enregister(log, fichierexiste)
    except Exception as ex:
        print(Fore.YELLOW, INITIALE, Fore.RED, ex.__class__.__name__, Fore.YELLOW, ": ", ex, Fore.RESET, sep="")


def enregister(log, fichierexiste) -> None:
    """enregistre le log dans le fichier"""
    with open('pylog.tsv', 'a', newline='') as tsvfichier:
        fieldnames = log.keys()
        writer = csv.DictWriter(tsvfichier, fieldnames=fieldnames, delimiter='\t')
        if not fichierexiste:
            writer.writeheader()
        writer.writerow(log)


def args_parse() -> argparse.Namespace:
    """Fonction qui parse les arguments"""
    parser = argparse.ArgumentParser(description="Commande pour journaliser un message -- ©2020, par Xavier Gagnon",
                                     epilog="PS si aucun argument n'est fourni, il vous seront demandés.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--liste', action='store_true', help='Afficher les logs')
    group.add_argument('-b', '--browse', action='store_true', help='Afficher les logs dans le navigateur')
    parser.add_argument('-t', metavar='{n,a,e}', dest='type', choices=['n', 'a', 'e'], help='Type de log',
                        default='notification',
                        type=str)
    parser.add_argument('--type', metavar='{notification,avertissement,erreur}', dest='type',
                        choices=['notification', 'avertissement', 'erreur'],
                        default='notification',
                        help='Type de log',
                        type=str)
    parser.add_argument('-u', '--user', metavar='USER', help="Nom de l'utilisateur", dest='utilisateur',
                        default=getpass.getuser(),
                        type=str)
    parser.add_argument('message', metavar='message', help='Message à journalier', type=str, nargs='*')
    return parser.parse_args()


if __name__ == '__main__':
    main()
