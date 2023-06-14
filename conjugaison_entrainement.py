import json

import unidecode

import numpy as np

from numpy.random import choice

from tkinter import *

import random



def uniformisation_proba(dico_voc, probability_distribution):

    if len(dico_voc) == len(probability_distribution):
        return probability_distribution
    else:
        proba_uniforme = 1/len(probability_distribution)
        probability_distribution = np.append(
            probability_distribution, np.array(
                [proba_uniforme]*(len(dico_voc)-len(probability_distribution))))
        return probability_distribution / np.sum(probability_distribution)

def reinit_proba(dico_voc, path_proba_distribution):
    n = len(dico_voc)
    proba_uniforme = 1/n
    probability_distribution = np.array([proba_uniforme]*n)
    np.save(
        path_proba_distribution, probability_distribution)


def session_traduction(langue="esp", nb_mot_a_traduire=50, proba_reinit = False):

    path_dico_voc = r"C:\Users\louis.reumaux\Documents\ptg\dico.json"
    path_proba_distribution = r"C:\Users\louis.reumaux\Documents\ptg\probability_distribution_por.npy"
    dico_voc = json.load(open(
        path_dico_voc, "r", encoding='utf-8'))
    probability_distribution = np.load(
        path_proba_distribution)

    list_of_candidates = dico_voc.keys()

    if proba_reinit == True:
        reinit_proba(dico_voc, path_proba_distribution)

    probability_distribution = uniformisation_proba(
        dico_voc, probability_distribution)

    draw = choice(list(list_of_candidates), nb_mot_a_traduire,
                  p=probability_distribution, replace=False)
    i = 0
    error = 0

    while i < len(draw):
        mot_a_traduire = draw[i]
        indice_mot_a_traduire = np.where(
            np.array(list(list_of_candidates)) == mot_a_traduire)[0][0]
        liste_trad = [unidecode.unidecode(
            trad.lower()) for trad in dico_voc[mot_a_traduire]] if isinstance(dico_voc[mot_a_traduire], list) else [unidecode.unidecode(dico_voc[mot_a_traduire].lower())]
        traduction_officielle = [trad.lower().strip() for trad in dico_voc[mot_a_traduire]] if isinstance(
            dico_voc[mot_a_traduire], list) else [dico_voc[mot_a_traduire]]
        print("Si tu appuies sur entrée sans rien écrire tu as la réponse")
        traduction_user = input(
            f"Traduis le mot '{mot_a_traduire}': ").strip().lower()
        essai = 1
        while unidecode.unidecode(traduction_user) not in liste_trad:
            if traduction_user == "" or essai >= 2:
                draw = np.append(draw, mot_a_traduire)
                if i < nb_mot_a_traduire:
                    error += 1
                for trad_officielle in traduction_officielle:
                    print("Traduction : " + trad_officielle + "\n")
                break
            traduction_user = input(
                f"Traduis le mot '{mot_a_traduire}' : ").strip().lower()
            essai += 1
        if essai < 2 or traduction_user != "":
            for trad in traduction_officielle:
                if unidecode.unidecode(
                        trad) == unidecode.unidecode(traduction_user):
                    if traduction_user != trad:
                        print(f"\nAttention aux accents : {trad}\n")
                    else:
                        print("\nBravo tu as l'orthographe exacte !\n")
                    probability_distribution[indice_mot_a_traduire] *= 3/4
                    if i % 10 == 0:
                        avancee = np.round(i / len(draw) * 100, 2)
                        print("\nProgression : " + str(avancee) + " % \n")

        if unidecode.unidecode(traduction_user) not in liste_trad:
            probability_distribution[indice_mot_a_traduire] *= 5/3
        if traduction_user != "" and essai < 2:
            for trad in traduction_officielle:
                if unidecode.unidecode(
                        trad) != unidecode.unidecode(traduction_user):
                    print("Autre traduction : " + trad + "\n")
        i += 1
    success_rate = np.round(1 - (error / nb_mot_a_traduire), 2) * 100
    print("\nTu as terminé la session de traduction !")
    print(f"\nTu as un taux de réussité de {success_rate} %")
    probability_distribution = probability_distribution / np.sum(probability_distribution)
    np.save(
        path_proba_distribution, probability_distribution)


session_traduction("por", 100)



#conjugaison_verbe_entier_hasard("por", 15, True)



# conjugaison_de_base("por")

