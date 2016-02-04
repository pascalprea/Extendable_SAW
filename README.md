# Extendable_SAW
Two linear programs to generate extendable Self-Avoiding Walks (SAW), one in Z^n, the other on ZxZ. 
The second is less general but runs faster than the other

Both are implementations of the algorithm described in :
P. PREA, M. ROUAULT & F. BRUCKER,
An Optimal Algorithm to Generate Extendable Self-Avoiding Walks in Arbitrary Dimension

####################################################################

Extendable.py 
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


#######################################################################


Two_dimensional_Basic_Extendables.py 
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



In both programs : THE DRAWING USES matplotlib LIBRARY

