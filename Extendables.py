#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
An implementation of the algorithm described in :
P. PREA, M. ROUAULT & F. BRUCKER,
An Optimal Algorithm to Generate Extendable Self-Avoiding Walks in Arbitrary Dimension

Generate random Extendable Self-Avoiding Walks (SAW) in Z^n, according to parameters in the 6 global
variables just below. These variables can/must be changed (but not the rest of the program).
These variables are:
    DIM : the dimension of the space
    LENGTH : the length of the SAW
    BIAS : a bias in the random choice of the points. MUST BE AN INTEGER.
        If BIAS is negative, the SAW is more dense
        If BIAS is positive, the SAW is not dense.
        In both case, a great absolute value corresponds with a small effect (1 (or -1) have the strongest effect)
    DESSIN is a boolean.
        If DESSIN is False :
            the program simply generates NB_TESTS walks (so you can test time, ...)
        If DESSIN is True :
           The program prints the dimension, bias, length and distance between extremities of the path.
            The program draws the path (if DIM == 2 or 3)
            If AFFICHAGE is True (or if DIM > 3), the program also print (on the terminal)
                the walk as a list of points
            If DIM == 2 or 3, the program will also propose to store
                the data into a program that will draw this walk.
        If DESSIN is False (resp. True), then AFFICHAGE (resp. NB_TESTS) has no importance


THE DRAWING USES matplotlib LIBRARY


To generate a bi-dimensional SAW with BIAS = 0, you should rather use the program
    "Two_dimensional_Basic_Extendables.py", which is more than twice faster.
"""

#####################################################################
#             PARAMETRES QUE L'ON PEUT/DOIT CHANGER                 #
#####################################################################

DIM = 3

LENGTH = 10000

BIAS = -1

DESSIN = True

NB_TESTS = 100

AFFICHAGE = False


#####################################################################
#####################################################################


import random
import math


#####################################################################
#####################################################################
#               variables globales (DO NOT CHANGE)                  #
#####################################################################


Origine = tuple([0] * DIM)     # (0,..., 0)

Liste_Des_Points = [Origine]
Dico_Des_Points = {Origine: None}

Petite_Origine = tuple([0] * (DIM - 1))


def create_minmax():
    les_minmax = []
    for i in range(DIM):
        les_minmax.append({Petite_Origine: [0, 0]})
    return les_minmax

Les_Minmax = create_minmax()

Point_Un = list(Origine)
Point_Un[0] = 1                 
Point_Un = tuple(Point_Un)     # (1, 0,..., 0)

Liste_Ariane = [Point_Un]
Dico_Ariane = {Point_Un: 0}


def create_deplacement():
    deplacements = []
    for i in range(DIM):
        deplacements.append(tuple(([0] * i) + [1] + ([0] * (DIM - (i + 1)))))
        deplacements.append(tuple(([0] * i) + [-1] + ([0] * (DIM - (i + 1)))))
    return deplacements

Deplacements = create_deplacement()

Graphe = {}


#################################
#       Fonctions Basiques      #
#################################


def pluss(pt_1, pt_2):
    pt = []
    for coordinate in range(DIM):
        pt.append(pt_1[coordinate] + pt_2[coordinate])
    return tuple(pt)


def moinss(pt_1, pt_2):
    pt = []
    for coordinate in range(DIM):
        pt.append(pt_1[coordinate] - pt_2[coordinate])
    return tuple(pt)


def norme_manhattan(pt):
    resul = 0
    for coord in pt:
        resul += abs(coord)
    return resul


def enleve_coord(pt, coordinate):
    pt = list(pt)
    pt.pop(coordinate)
    return tuple(pt)


def voisin(pt, coord, ecart):
    resul = list(pt)
    resul[coord] = resul[coord] + ecart
    return tuple(resul)


def intersection(ensemble_1, ensemble_2):
    resul = []
    for v in ensemble_1:
        if v in ensemble_2:
            resul.append(v)
    return resul


def distance_euclidean(pt1, pt2):
    resul = 0
    for coordinate in range(DIM):
        resul += ((pt1[coordinate] - pt2[coordinate]) ** 2)
    return math.sqrt(resul)


###############################################################
#       Construction d'un Graphe + Chemin dans un Graphe      #
###############################################################


def construction_sommets_graphe(pt_base, pt, d):
    global Graphe 
    if d == 0:
        pt.reverse()
        pt = tuple(pt)
        if pt not in Dico_Des_Points:
            Graphe[pt] = []
    else:
        for dep in [-1, 0, 1]:
            construction_sommets_graphe(pt_base, pt + [pt_base[d - 1] + dep], d - 1)
            
            
def construction_aretes_graphe():
    global Graphe
    for v_1 in Graphe:
        for v2 in Graphe:
            if norme_manhattan(moinss(v_1, v2)) == 1:
                Graphe[v_1].append(v2)
                Graphe[v2].append(v_1)
    return Graphe


def construct_chemin(graphe, distance, v):
    ch = [v]
    d = distance[v]
    x = v
    while d > 0:
        for y in graphe[x]:
            if distance[y] == d - 1:
                ch.append(y)
                d -= 1
                x = y
                break
    return ch


def chemin(depart, arrivees, graphe):
    distance = {}
    for vertice in graphe:
        distance[vertice] = None
    distance[depart] = 0
    frontiere = [depart]
    k = 1
    while frontiere != []:
        new_front = []
        for vertice in frontiere:
            for vertice_2 in graphe[vertice]:
                if vertice_2 in arrivees:
                    distance[vertice_2] = k
                    return construct_chemin(graphe, distance, vertice_2)
                if distance[vertice_2] is None:
                    distance[vertice_2] = k
                    new_front.append(vertice_2)
        k += 1
        frontiere = new_front


#####################################################
#      Calcul des Probas de Selection d'un voisin   #
#####################################################


def calcul_proba(tab):
    resul = []
    for coordinate in range(len(tab)):
        if tab[coordinate] >= 0:
            if BIAS == 0:
                resul.append(coordinate)
            elif BIAS > 0:
                resul.extend([coordinate] * (BIAS - 1 + tab[coordinate]))
            else:
                resul.extend([coordinate] * (-BIAS + (2 * DIM) - 1 - tab[coordinate]))
    return resul


def calcul_nombres_infinis():
    global Graphe
    pt_courant = Liste_Des_Points[-1]
    num_voisin = 0
    Graphe = {}
    resul = []
    while num_voisin < 2 * DIM:
        candidat = pluss(pt_courant, Deplacements[num_voisin])
        som = -1
        if candidat not in Dico_Des_Points:
            som = 0
            for ind in range(DIM):
                petit_pt = enleve_coord(candidat, ind)
                if petit_pt not in Les_Minmax[ind]:
                    som += 2
                elif candidat[ind] < Les_Minmax[ind][petit_pt][0] or (candidat[ind] > Les_Minmax[ind][petit_pt][1]):
                    som += 1
            if som == 0 and candidat not in Dico_Ariane:
                if Graphe == {}:
                    construction_sommets_graphe(pt_courant, [], DIM)
                    Graphe = construction_aretes_graphe()
                    dest = intersection(Graphe, Dico_Ariane)
                chem = chemin(candidat, dest, Graphe)
                if chem is None:
                    som = -1
        resul.append(som)
        num_voisin += 1
    return resul

        
##########################################
#   Construction du SAW proprement dit   #
##########################################


def nouveau_fil(pt_base):
    global Liste_Ariane
    global Dico_Ariane     
    Liste_Ariane = [pt_base]
    Dico_Ariane = {pt_base: 0}


def racourcir_fil(index):
    while len(Liste_Ariane) > index:
        del Dico_Ariane[Liste_Ariane.pop()]


def ajout_dans_fil(pt):
    Dico_Ariane[tuple(pt)] = len(Liste_Ariane)
    Liste_Ariane.append(tuple(pt))


def insert_point(pt):
    Liste_Des_Points.append(pt)
    Dico_Des_Points[pt] = None
    for index in range(DIM):
        petit_pt = enleve_coord(pt, index)
        if petit_pt not in Les_Minmax[index]:
            Les_Minmax[index][petit_pt] = [pt[index], pt[index]]
        elif pt[index] < Les_Minmax[index][petit_pt][0]:
            Les_Minmax[index][petit_pt][0] = pt[index]
        elif pt[index] > Les_Minmax[index][petit_pt][1]:
            Les_Minmax[index][petit_pt][1] = pt[index]
                    

def ajout_point():
    global Graphe
    pt_courant = Liste_Des_Points[-1]
    les_probas = calcul_proba(calcul_nombres_infinis())
    num_voisin = random.choice(les_probas)
    candidat = pluss(pt_courant, Deplacements[num_voisin])
    for index in range(DIM):
        petit_pt = enleve_coord(candidat, index)
        if (petit_pt not in Les_Minmax[index]) or (candidat[index] > Les_Minmax[index][petit_pt][1]):
            insert_point(candidat)
            nouveau_fil(voisin(candidat, index, 1))
            break
        elif candidat[index] < Les_Minmax[index][petit_pt][0]:
            insert_point(candidat)
            nouveau_fil(voisin(candidat, index, -1))
            break
    else:
        if candidat in Dico_Ariane:
            insert_point(candidat)
            racourcir_fil(Dico_Ariane[candidat])
        else:
            dest = intersection(Graphe, Dico_Ariane)
            chem = chemin(candidat, dest, Graphe)
            insert_point(candidat)
            racourcir_fil(Dico_Ariane[chem[0]] + 1)
            for pt in chem[1: -1]:
                ajout_dans_fil(pt)


def creation_chemin(longueur):
    global Liste_Des_Points
    global Dico_Des_Points
    global Liste_Ariane
    global Dico_Ariane
    global Les_Minmax
    Liste_Des_Points = [Origine]
    Dico_Des_Points = {Origine: None}
    Les_Minmax = []
    for index in range(DIM):
        Les_Minmax.append({Petite_Origine: [0, 0]})
    Liste_Ariane = [Point_Un]
    Dico_Ariane = {Point_Un: 0}
    for nb in range(longueur):
        ajout_point()
    return math.sqrt(distance_euclidean(Liste_Des_Points[-1], Origine))

        
#############################
#                           #
#   FONCTIONS GRAPHIQUES    #
#                           #
#############################


def affichage_chemin():
    if DIM == 2:
        import matplotlib.pyplot as plt
        list_x = []
        liste_y = []
        x_max = 0
        x_min = 0
        y_max = 0
        y_min = 0
        ariadne_x = []
        ariadne_y = []
        for pt in Liste_Ariane:
            ariadne_x.append(pt[0])
            ariadne_y.append(pt[1])
        for pt in Liste_Des_Points:
            list_x.append(pt[0])
            liste_y.append(pt[1])
            if (pt[0]) > x_max:
                x_max = pt[0]
            elif pt[0] < x_min:
                x_min = pt[0]
            if (pt[1]) > y_max:
                y_max = pt[1]
            elif pt[1] < y_min:
                y_min = pt[1]
        plt.plot(x_min-1, y_min - 1)
        plt.plot(x_max+1, y_max + 1)
        plt.plot(list_x, liste_y, 'blue')
        plt.show()
        return [list_x, liste_y]
    else:
        from matplotlib import pyplot
        from mpl_toolkits.mplot3d import Axes3D
        plot3d = pyplot.figure().gca(projection='3d')
        plot3d.plot([x for x, y, z in Liste_Des_Points], [y for x, y, z in Liste_Des_Points],
                    [z for x, y, z in Liste_Des_Points], color="black")
        pyplot.show()

        
def je_fais_un_programme_qui_stocke_et_dessine_le_chemin(path):
    distance = distance_euclidean(Origine, Liste_Des_Points[-1])
    le_titre = 'Draw_an_Extendable_SAW___Length_' + str(LENGTH) + '__dimension_' + str(DIM) + '__Bias_' \
               + str(BIAS) + '____nb_' + str(random.randint(1, 999999999)) + ".py"
    print("The name of the program will be : \n\n" + le_titre)
    print("\n\nIt is long, but that avoids confusion")
    fich = open(le_titre, 'a')
    fich.write("\n#! /usr/bin/env python\n# -*- coding: utf-8 -*-\n\n")
    fich.write("\n\nprint ('Voulez-vous un dessin joli ou lisible ?')")
    fich.write("\nprint ('    joli (pretty)      : type 0')")
    fich.write("\nprint ('    lisible (readable) : type 1')")
    fich.write("\nJoli = raw_input ()")
    fich.write("\nCouleur_pt = 'red'  # on peut changer ca")
    fich.write("\nCouleur_ch = 'black'  # on peut changer ca")
    fich.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    fich.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    if DIM == 2:
        list_x = path[0]
        list_y = path[1]
        fich.write("import matplotlib.pyplot as plt\nimport numpy as np\n")
        fich.write("\nimport math")
        fich.write("\n\nLx =" + str(list_x))
        fich.write("\n\nLy = " + str(list_y))
    else:
        fich.write("\nfrom matplotlib import pyplot")
        fich.write("\nfrom mpl_toolkits.mplot3d import Axes3D")
        fich.write("\nPATH = " + str(Liste_Des_Points))
    fich.write("\nprint ' ' ")
    fich.write("\nprint ' ' ")
    fich.write("\nprint 'longueur : ' + str (" + str(len(Liste_Des_Points)) + ")")
    fich.write("\nprint 'distance :' + str (" + str(round(math.sqrt(distance), 3)) + ")")
    fich.write("\nprint 'Correction : ' + str (" + str(BIAS) + ")")
    fich.write("\nprint '  ' ")
    fich.write("\nprint ' ' ")
    if DIM == 2:
        fich.write("\nif Joli == '0' : ")
        fich.write("\n    plt.scatter (Lx, Ly, marker = 'o', color = Couleur_pt)")
        fich.write("\n\n\n\nplt.plot(Lx, Ly, color = Couleur_ch)")
        fich.write("\n\nplt.show()\n\n")
    else:
        fich.write("\nplot3d = pyplot.figure().gca(projection='3d')")
        fich.write("\nif Joli == '0' : ")
        fich.write("\n    plot3d.scatter([x for x, y, z in PATH], [y for x, y, z in PATH], "
                   "[z for x, y, z in PATH], 'O', color= Couleur_pt)")
        fich.write("\nplot3d.plot([x for x, y, z in PATH], [y for x, y, z in PATH], "
                   "[z for x, y, z in PATH], color=Couleur_ch)")
        fich.write("\npyplot.show()")
    fich.close()


def petit_affichage(d):
    print('\n\n\n\n\ndimension  : ' + str(DIM))
    print('correction : ' + str(BIAS))
    print('longueur   : ' + str(LENGTH))
    print('distance   : ' + str(round(math.sqrt(d), 3)) + '\n\n\n\n\n\n\n')


def gros_affichage(d):
    print('\n\n\n\n\n\n\n\n\n\n\n\n' + str(Liste_Des_Points) + '\n\n\n\n\n')
    petit_affichage(d)


#############################
#                           #
#     CORPS DU PROGRAMME    #
#                           #
#############################


def je_fais_un_joli_dessin():
    creation_chemin(LENGTH)
    pt_fin = Liste_Des_Points[-1]
    d = 0
    for x in pt_fin:
        d += x ** 2
    petit_affichage(d)
    if DIM == 2 or DIM == 3:
        if AFFICHAGE:
            gros_affichage(d)
        path = affichage_chemin()
        print('\nDo you like this drawing ?')
        print('Do you want to save the data ?\n    Yes --> 17\n    No --> 0')
        reponse = raw_input('Your Choice : ')
        if reponse != '0':
            je_fais_un_programme_qui_stocke_et_dessine_le_chemin(path)
    else:
        gros_affichage(d)


def serie_de_tests(total_nb):
    for nb in range(total_nb):
        creation_chemin(LENGTH)


if DESSIN:
    je_fais_un_joli_dessin()
else:
    serie_de_tests(NB_TESTS)