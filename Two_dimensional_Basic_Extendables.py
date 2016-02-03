#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
An implementation of the algorithm described in :
P. PREA, M. ROUAULT & F. BRUCKER,
An Optimal Algorithm to Generate Extendable Self-Avoiding Walks in Arbitrary Dimension


Generate random Extendable Self-Avoiding Walks (SAW) in ZxZ, according to parameters in the 4 global
variables just below. These variables can/must be changed (but not the rest of the program).
These variables are:

    LENGTH : the length of the

    DESSIN is a boolean.
        If DESSIN is False :
            the program simply generates NB_TESTS walks (so you can test time, ...)
        If DESSIN is True :
            The program prints the length of the path and the distance between its two extremities.
            The program draws the path
            If AFFICHAGE is True, the program also print (on the terminal) the walk as a list of points
            The program will also propose to store the data into a program that will draw this walk.
        If DESSIN is False (resp. True), then AFFICHAGE (resp. NB_TESTS) has no importance


This program just treat a particular case of "Extendable.py" but runs faster.

THE DRAWING USES matplotlib LIBRARY

"""
LENGTH = 1000000

DESSIN = True

NB_TESTS = 10

AFFICHAGE = False

########################################################################


import random
import math


Dim = 2

Origine = tuple([0] * Dim)

Liste_Des_Points = [Origine]
Dico_Des_Points = {Origine: None}


def create_minmax():
    les_minmax = []
    for coordinate in range(Dim):
        les_minmax.append({0: [0] * ((Dim - 1) * 2)})
    return les_minmax

Les_Minmax = create_minmax()

Point_Un = list(Origine)
Point_Un[0] = 1
Point_Un = tuple(Point_Un)

Liste_Ariane = [Point_Un]
Dico_Ariane = {Point_Un: 0}


def create_deplacements():
    deplacements = []
    for coordinate in range(Dim):
        deplacements.append(tuple(([0] * coordinate) + [1] + ([0] * (1 - coordinate))))
        deplacements.append(tuple(([0] * coordinate) + [-1] + ([0] * (1 - coordinate))))
    return deplacements

Deplacements = create_deplacements()


def pluss(pt_1, pt_2):
    pt = []
    for coordinate in range(Dim):
        pt.append(pt_1[coordinate] + pt_2[coordinate])
    return tuple(pt)


def moinss(pt_1, pt_2):
    pt = []
    for coordinate in range(Dim):
        pt.append(pt_1[coordinate] - pt_2[coordinate])
    return tuple(pt)

    
def insert_point(pt):
    x = pt[0]
    y = pt[1]
    Liste_Des_Points.append(pt)
    Dico_Des_Points[pt] = None
    if x not in Dico_xxx:
        Dico_xxx[x] = [y, y]
    elif y < Dico_xxx[x][0]:
        Dico_xxx[x][0] = y
    elif y > Dico_xxx[x][1]:
        Dico_xxx[x][1] = y
    if y not in Dico_y:
        Dico_y[y] = [x, x]
    elif x > Dico_y[y][1]:
        Dico_y[y][1] = x
    elif x < Dico_y[y][0]:
        Dico_y[y][0] = x
        
        
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
        
        
def white_points(candid):
    direction = moinss(Liste_Des_Points[-1], Liste_Des_Points[-2])
    if candid == pluss(Liste_Des_Points[-1], direction):
        return [pluss(Liste_Ariane[-1], direction)]
    if Liste_Ariane[-1] == pluss(Liste_Des_Points[-1], direction):
        return [pluss(candid, direction)]
    return [pluss(Liste_Ariane[-1], direction), pluss(Liste_Des_Points[-1], direction), pluss(candid, direction)]
    
    
def libre(liste_de_pt):
    for pt in liste_de_pt:
        if pt in Dico_Des_Points:
            return False
    return True


def ajout_point():
    pt_courant = Liste_Des_Points[-1]
    random.shuffle(Deplacements)
    on_continue = True
    num_voisin = 0
    while on_continue and num_voisin < 4:
        candidat = pluss(pt_courant, Deplacements[num_voisin])
        xx = candidat[0]
        yy = candidat[1]
        if candidat not in Dico_Des_Points:
            on_continue = False
            if (xx not in Dico_xxx) or (yy > Dico_xxx[xx][1]):
                insert_point(candidat)
                nouveau_fil((xx, yy+1))
            elif yy < Dico_xxx[xx][0]:
                insert_point(candidat)
                nouveau_fil((xx, yy - 1))
            elif (yy not in Dico_y) or (xx > Dico_y[yy][1]):
                insert_point(candidat)
                nouveau_fil((xx + 1, yy))
            elif xx < Dico_y[yy][0]:
                insert_point(candidat)
                nouveau_fil((xx - 1, yy))
            elif candidat in Dico_Ariane:
                insert_point(candidat)
                racourcir_fil(Dico_Ariane[candidat])
            else:
                points_blancs = white_points(candidat)
                if libre(points_blancs):
                    insert_point(candidat)
                    for pt in points_blancs:
                        if pt in Dico_Ariane:
                            racourcir_fil(Dico_Ariane[pt] + 1)
                        else:
                            ajout_dans_fil(pt)
                else:
                    on_continue = True
        num_voisin += 1


def creation_chemin():
    global Liste_Ariane
    global Dico_Ariane    
    global Liste_Des_Points
    global Dico_Des_Points
    global Dico_xxx
    global Dico_y
    Liste_Des_Points = [(0, 0)]
    Dico_Des_Points = {(0, 0): None}
    Dico_xxx = {0: [0, 0]}
    Dico_y = {0: [0, 0]}
    Liste_Ariane = [(1, 0)]
    Dico_Ariane = {(1, 0): 0}
    num_pt = 1
    while num_pt < LENGTH:
        num_pt += 1
        ajout_point()
    return math.sqrt(Liste_Des_Points[-1][0] ** 2 + Liste_Des_Points[-1][1] ** 2)


def serie_de_tests(nb):
    for num_test in range(nb):
        creation_chemin()


#############################
#                           #
#   FONCTIONS GRAPHIQUES    #
#                           #
#############################


def affichage_chemin():
    import matplotlib.pyplot as plt
    liste_x = []
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
        liste_x.append(pt[0])
        liste_y.append(pt[1])
        if (pt[0]) > x_max:
            x_max = pt[0]
        elif pt[0] < x_min:
            x_min = pt[0]
        if (pt[1]) > y_max:
            y_max = pt[1]
        elif pt[1] < y_min:
            y_min = pt[1]
    plt.plot(x_min - 1, y_min - 1)
    plt.plot(x_max + 1, y_max + 1)
    plt.plot(liste_x, liste_y, 'b-')
    plt.plot(ariadne_x, ariadne_y, 'r-')
    plt.show()
    return [liste_x, liste_y]

        
def je_fais_un_programme_qui_stocke_et_dessine_le_chemin(path):
    list_x = path[0]
    list_y = path[1]
    titre = 'Draw_a_2D-extendable_SAW_length_' + str(LENGTH) + '___nb' + str(random.randint(1, 99999999)) + ".py"
    print("the drawing program's name is : \n\n" + titre)
    print("\n\nit's a long name, to avoid confusion")
    fich = open(titre, 'a')
    fich.write("\n#! /usr/bin/env python\n# -*- coding: utf-8 -*-\n\n")
    fich.write("import matplotlib.pyplot as plt\nimport numpy as np\n")
    fich.write("\nimport math")
    fich.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n ")
    fich.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n ")
    fich.write("\n\nLx =" + str(list_x))
    fich.write("\n\nLy = " + str(list_y))
    fich.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    fich.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n ")
    fich.write("\n(x,y) = (Lx[-1], Ly[-1])")
    fich.write("\nprint ' ' ")
    fich.write("\nprint ' ' ")
    fich.write("\nprint 'length :    ' + str (len(Lx))")
    fich.write("\nprint 'distance between extremities :   ' + str (round (math.sqrt (x**2 + y**2), 3))   ")
    fich.write("\nprint '  ' ")
    fich.write("\nprint ' ' ")
    fich.write("\n\n\n\nplt.plot(Lx, Ly, 'b-')")
    fich.write("\n\nplt.show()\n\n")
    fich.write("print ' ' \n\n")
    fich.write("\n\nprint ' ' ")
    fich.close()


def petit_affichage():
    print('\n\n\n\n\n\n\nlongueur :' + str(LENGTH))
    (x, y) = Liste_Des_Points[-1]
    print('distance :' + str(round(math.sqrt(x ** 2 + y ** 2), 3)) + '\n\n')


def je_fais_un_joli_dessin():
    creation_chemin()
    petit_affichage()
    if AFFICHAGE:
        print('\n\n\n\n' + str(Liste_Des_Points))
        petit_affichage()
    path = affichage_chemin()
    print('\nYou like this drawing ?')
    print('Save the data\n    Yes --> 17\n    No --> 0')
    reponse = raw_input('Your choice : ')
    if reponse != '0':
        je_fais_un_programme_qui_stocke_et_dessine_le_chemin(path)


#############################
#                           #
#     CORPS DU PROGRAMME    #
#                           #
#############################

    
if DESSIN:
    je_fais_un_joli_dessin()
else:
    serie_de_tests(NB_TESTS)
print('\n\nThis is the end...')
print(' ')