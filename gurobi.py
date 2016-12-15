# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 01:52:17 2016

@author: emilie
"""

#import numpy as np
from gurobipy import *
import copy
import time

#strFileName= "puzzles/test/question1.text"
#strFileName="puzzles/test/test1.text"
strFileName="puzzles/test/test2.text"
#strFileName="puzzles/test/test3.text"
#strFileName="puzzles/debutant/jam10.txt"
#strFileName="puzzles/expert/jam31.txt"
#strFileName="puzzles/expert/jam32.txt"
#strFileName="puzzles/expert/jam33.txt"
#strFileName="puzzles/expert/jam34.txt"
#strFileName="puzzles/expert/jam39.txt"
#strFileName="puzzles/expert/jam40.txt"

listeN = [14,25,31,50]
N = listeN[0]

dimensionsGrille=(-1,-1)
nb_ligne = 0

"""
fonction ouvrant un fichier txt et generant une matrice 2D de configuration initiale
"""
def lectureFichier(strFileName):
    # Ouverture d'un fichier en *lecture*:    
    fichier = open(strFileName, "r")
    # dimensions de la grille => 1ere ligne du fichier
    dGrille = fichier.readline()
    nbX,nbY = dGrille.split()
    dimensionsGrille = (int(nbX),int(nbY))
    # initialisation de la matrice 2D de configuration initiale
    configuration2D = [[0 for x in xrange(dimensionsGrille[0])] for y in xrange(dimensionsGrille[1])]

    i=0
    j=0
    # passe a travers tout le fichier
    for ligne in fichier:
        cases = ligne.split()
        for caseValue in cases:
            configuration2D[j][i] = caseValue
            i=i+1
        i = 0 
        j=j+1
    # Fermeture du fichier
    fichier.close()
    print configuration2D
    return configuration2D, dimensionsGrille


      
def genereConfigInitiale(matrice,nbLigne):
    dicoVehicInfo = {}
    dicoConfigInit = {}     # dico de conversion coordonnées - marqueur
    taille = -1
    ecart = -1
    for i in range(len(matrice)):
        for j in range(len(matrice[i])) :
            
            if matrice[i][j] not in dicoVehicInfo.keys() and matrice[i][j] != '0' :
                if matrice[i][j] not in dicoConfigInit.keys():
                    dicoConfigInit[matrice[i][j]] = i*nbLigne+j+1
                # on teste le type de vehicule et on en deduit sa taille
                if matrice[i][j][0] == 't':
                        taille = 3
                else:
                        taille = 2
                # on recupere l orientation du vehicule et sa position dans la ligne / colonne 
                if i == len(matrice)-1 and j != len(matrice[i])-1 and matrice[i][j+1] != matrice[i][j] : 
                    orientation = "v"
                    ecart = j
                elif i != len(matrice)-1 and matrice [i+1][j] == matrice[i][j]:
                    orientation = "v"
                    ecart = j
                elif j == len(matrice[i])-1 and i != len(matrice)-1 and matrice[i+1][j] != matrice[i][j] :
                    orientation = "h"
                    ecart = i
                elif j != len(matrice[i])-1 or matrice [i][j+1] == matrice[i][j]:
                    orientation = "h"
                    ecart = i
                dicoVehicInfo[matrice[i][j]] = [orientation,ecart,taille]
                
    return dicoVehicInfo,dicoConfigInit

"""
    fonction generant la contrainte : on fixe la position du marqueur des vehicules 
    dans la configuration intiale  
"""
# contraite de la pos de depart des vehicules 
def genereContraintePosIniVehicules(m,dicoX,dicoConfigInit):
    for i in dicoConfigInit.keys():
        print " addconstraint ", i,dicoConfigInit[i],0
        m.addConstr( dicoX[i,dicoConfigInit[i],0] == 1)
 

def genereContMemeNbVehicPerTurn(m,N,dicoX,dicoVehicInfo):
    nb_voiture = len(dicoVehicInfo.keys())  # nombre de voitures totales par jeu
    for k in range (N+1):
        m.addConstr(quicksum(dicoX[(a,b,c)] for a,b,c in dicoX.keys() if c == k) == nb_voiture)

# vi*xi,j,k - somme sur mi,j de (z,i,m,k) pour tout i,j,k
def genereCont1_VerifOccupCase(m,N,dicoX,dicoZ,dicoVehicInfo,dimensionsGrille):
    for i in dicoVehicInfo.keys():
        vi = dicoVehicInfo[i][2]  
        tmp = sorted([j for a,j,b in dicoX.keys() if a==i and b==0])
        #tmp = [j for a,j,b in x.keys() if a==i and b==0]
        for k in range(N+1):
            for j in tmp:
                if dicoVehicInfo[i][0] == "h":
                    listePositionsRangee = range((dicoVehicInfo[i][1])*dimensionsGrille[0]+1,(dicoVehicInfo[i][1]+1)*dimensionsGrille[0]+1)
                    #tmp2 = [  1 , 2 , 3 ,4 ,5 , 6]
                else:
                    listePositionsRangee = range((dicoVehicInfo[i][1])+1,dimensionsGrille[0]*dimensionsGrille[1]+1,dimensionsGrille[0])
                    #tmp2 = [ 1 ,7 , 13 ...... 31]
                mij  = listePositionsRangee[listePositionsRangee.index(j):listePositionsRangee.index(j)+vi] # recup la sous-liste mij
                #print i,j,k,mij
                
                m.addConstr( vi*  dicoX[(i,j,k)] <= quicksum(dicoZ[(i,m,k)] for m in mij))

"""
    Fonction  generant la contrainte : 
"""
# somme pour i de zi,j,k   j, k 
def genereCont2_Singleton(m,N,dicoZ,dicoVehicInfo,dimensionsGrille): 
    for k in range(1,N+1):
        for j in range(1,dimensionsGrille[0]*dimensionsGrille[1]+1):
            liste = []  #liste des vehicule pouvant etre en position j
            for i in dicoVehicInfo.keys():
                if dicoVehicInfo[i][0] == "h":
                    # on recupere la liste des positions possibles de la ligne
                    listePositionsRangee = range((dicoVehicInfo[i][1])*dimensionsGrille[0]+1,(dicoVehicInfo[i][1]+1)*dimensionsGrille[0]+1)
                else:
                    # on recupere la liste des positions possibles de la colonne
                    listePositionsRangee = range((dicoVehicInfo[i][1])+1,dimensionsGrille[0]*dimensionsGrille[1]+1,dimensionsGrille[0])
                if j in listePositionsRangee:                
                    liste.append(i)
            #print j,liste
            if liste != None and len(liste)>1:
                m.addConstr( quicksum(dicoZ[(i,j,k)] for i in liste)  <= 1)

"""
    fonction generant la contrainte : seules vi cases sont occupees 
    par le vehicule i dans sa rangee
    entree : N :
            m : modele gurobi
            dicoZ : dictionnaire z
            dicoVehicInfo : dictionnaire  
            dimensionsGrille : (nombre lignes, nombre colonnes)
"""
def genereCont3_OccupationVi(m,N,dicoZ,dicoVehicInfo,dimensionsGrille): 
    for i in dicoVehicInfo.keys():
        vi = dicoVehicInfo[i][2]  
        for k in range(N+1):
            if dicoVehicInfo[i][0] == "h":
                listePositionsRangee = range((dicoVehicInfo[i][1])*dimensionsGrille[0]+1,(dicoVehicInfo[i][1]+1)*dimensionsGrille[0]+1)
            else:
                listePositionsRangee = range((dicoVehicInfo[i][1])+1,dimensionsGrille[0]*dimensionsGrille[1]+1,dimensionsGrille[0])
            m.addConstr(quicksum(dicoZ[(i,j,k)] for j in listePositionsRangee) == vi)
            
"""
    fonction generant la contrainte : un vehicule peut se deplacer d une case j
    a une case l lors du kieme mouvement (y(i,j,l,k)==1) => pas d'obstacle entre j et l
    entree : 
"""
def genereCont4_PasObstacleEntreJL(m,N,dicoX,dicoY,dicoZ,dicoVehicInfo,dimensionsGrille): 
      for idVehicule in dicoVehicInfo.keys():
        tmp = sorted([j for a,j,b in dicoX.keys() if a==idVehicule and b==0])
        for k in range(1,N+1): 
            for caseJ in tmp: #j parmi les j possible
                tmp1 = copy.deepcopy(tmp)
                tmp1.remove(caseJ) 
                for caseL in tmp1: # l different de j
                        
                    if dicoVehicInfo[idVehicule][0] == "h":
                        tmp2 = range((dicoVehicInfo[idVehicule][1])*dimensionsGrille[0]+1,(dicoVehicInfo[idVehicule][1]+1)*dimensionsGrille[0]+1)
                        #tmp2 = [  1 , 2 , 3 ,4 ,5 , 6]
                    else:
                        tmp2 = range((dicoVehicInfo[idVehicule][1])+1,dimensionsGrille[0]*dimensionsGrille[1]+1,dimensionsGrille[0])
                        #tmp2 = [ 1 ,7 , 13 ...... 31]
                    if caseJ < caseL:
                        pjl  = tmp2[tmp2.index(caseJ)+1:tmp2.index(caseL)]
                    else:
                        pjl = tmp2[tmp2.index(caseL)+1:tmp2.index(caseJ)]
                    #print "idVehicule,caseJ,caseL,pjl ", idVehicule,caseJ,caseL,pjl
                        
                    liste = [(idVehicule2,b,c) for (idVehicule2,b,c) in dicoZ.keys() if idVehicule2 != idVehicule]
                    for p in pjl: 
                        m.addConstr( dicoY[(idVehicule,caseJ,caseL,k)] <= 1 - quicksum(dicoZ[(idVehicule2,b,c)] for (idVehicule2,b,c) in liste if idVehicule2 != idVehicule and b == p and c == k-1))

"""
    fonction generant la contrainte : au dernier mouvement, 
    la voiture rouge positionnee sur la case devant la sortie

"""

def genereCont5a_PositionFinVoitureRouge(m,N,dicoX): 
    m.addConstr( dicoX[('g',17,N)] == 1)

"""
    fonction generant la contrainte: deplacement d une seule voiture par tour de jeu
    entree :

"""
    
def genereCont5b_OneMovePerRound(m,N,dicoY):  
    for k in range(1,N+1):
        m.addConstr(quicksum(dicoY[(i,j,l,k)] for (i,j,l,a) in dicoY.keys() if a==k) <= 1)
"""
    fonction generant la contrainte : verification de la mise a jour du marqueur
    du vehicule i si deplacement
    entree :

"""
        
def genereCont5c_majMarqueurSiMove(m,N,dicoX,dicoY,dicoVehicInfo):
    for i in dicoVehicInfo.keys():
        # liste des cases possibles d une rangee
        casesRangee= sorted([j for a,j,b in dicoX.keys() if a==i and b==0]) 
        for k in range(1,N+1): 
            for j in casesRangee:
                print"=====>  j ",j, casesRangee
                copyCasesRangee = copy.deepcopy(casesRangee)
                copyCasesRangee.remove(j)   #on enleve la position courante
                for l in copyCasesRangee:
                    m.addConstr(dicoX[(i,l,k)] >= dicoY[(i,j,l,k)])
                    m.addConstr(dicoX[(i,j,k-1)] >= dicoY[(i,j,l,k)])
                    m.addConstr(dicoX[(i,j,k-1)] + dicoX[(i,l,k)] <= 1+dicoY[(i,j,l,k)])

"""
    fonction generant les variables de decision utilisees dans notre PL : ces sont 3 dictionnaires
    - x(i,l,k) : definit l'emplacement des marqueurs de tous les vehicules pour chaque tour
    - y(i,j,l,k) : definit les mouvements de tous les vehicules pour chaque tour
    - z(i,j,k) : definit toutes les cases occupees par tous les vehicules pour chaque tour

"""                   
def genereVarDecision(m,N,dicoVehicInfo,dimensionsGrille):
# definition des 3 dictionnaires : x(i,l,k)  -  y(i,j,l,k)   -  z(i,j,k)
    dicoX = {} # definit l'emplacement des marqueurs de tous les vehicules pour chaque tour
    dicoY = {} # definit les mouvements de tous les vehicules pour chaque tour
    dicoZ = {} # definit toutes les cases occupees par tous les vehicules pour chaque tour

    for idVoiture in dicoVehicInfo.keys():      
        for k in range(N+1): #k=0 => configuration initiale
            if dicoVehicInfo[idVoiture][0] == "h":
                for j in range(1,dimensionsGrille[1]+1):
                    coordJ = dicoVehicInfo[idVoiture][1]*dimensionsGrille[1]+j
                     # test cases valides : si la case du marqueur du vehicule est valide (l arriere de la voiture rentre dans la grille)
                    if j <= dimensionsGrille[1] - dicoVehicInfo[idVoiture][2]+1 :    
                        # dicoX : key : (idVoiture, case (de 1 a 36), k (nombre de partie du jeu)  valeur : variable gurobi correspondante)                         
                        dicoX[(idVoiture,coordJ,k)] = m.addVar(vtype=GRB.BINARY, lb=0, name = "X"+str(idVoiture)+","+str(coordJ)+","+str(k))
                                        
                    for l in range(1,dimensionsGrille[1]+1):
                        # on enleve le deplacement sur la case courante
                        # la voiture doit rentrer dans la ligne
                        if j != l and j <= dimensionsGrille[1] - dicoVehicInfo[idVoiture][2]+1:
                            coordL = dicoVehicInfo[idVoiture][1]*dimensionsGrille[1]+l
                            dicoY[(idVoiture,coordJ,coordL,k)] = m.addVar(vtype=GRB.BINARY, lb=0, name = "Y"+str(idVoiture)+","+str(coordJ)+","+str(coordL)+","+str(k))
                    # au depart pas de contrainte on considere que toutes les cases sont occupees
                    dicoZ[(idVoiture,coordJ,k)] = m.addVar(vtype=GRB.BINARY, lb=0, name = "Z"+str(idVoiture)+","+str(coordJ)+","+str(k))                            
                
            if dicoVehicInfo[idVoiture][0] == "v":
                 for j in range(0,dimensionsGrille[0]):
                     coordJ = dicoVehicInfo[idVoiture][1]+1 + dimensionsGrille[0]*j
                     # test cases valides : si la case du marqueur du vehicule est valide (l arriere de la voiture rentre dans la grille)
                     if j <= dimensionsGrille[0] - dicoVehicInfo[idVoiture][2] : 
                        dicoX[ (idVoiture,coordJ,k) ] = m.addVar(vtype=GRB.BINARY, lb=0, name = "X"+str(idVoiture)+","+str(coordJ)+","+str(k))                   
                     for l in range(dimensionsGrille[0]):  
                         # on enleve le deplacement sur la case courante
                        # la voiture doit rentrer dans la colonne
                        if j != l and j <= dimensionsGrille[0] - dicoVehicInfo[idVoiture][2]+1:
                            coordL = dicoVehicInfo[idVoiture][1]+1 + dimensionsGrille[0]*l 
                            dicoY[(idVoiture,coordJ,coordL,k)] = m.addVar(vtype=GRB.BINARY, lb=0, name = "Y"+str(idVoiture)+","+str(coordJ)+","+str(coordL)+","+str(k))                            
                    # au depart pas de contrainte on considere que toutes les cases sont occupees
                     dicoZ[(idVoiture,coordJ ,k)] = m.addVar(vtype=GRB.BINARY, lb=0, name = "Z"+str(idVoiture)+","+str(coordJ)+","+str(k))      
    return dicoX,dicoY,dicoZ

"""
    fonction d affichage des resultats obtenu dans la console

"""

def affichage(dicoY):
    cpt = 0
    for i in dicoY.keys() : 
        if dicoY[i].X == 1:
            cpt = cpt+1
            print "\nmouvement de ", i[0],"=> de la case ", i[1], " à ", i[2]
    print "-----------------------------------------"
    print "\nNombre total de déplacements : ",cpt

#------------------------------------------------------------------------------

configuration2D, dimensionsGrille = lectureFichier(strFileName)
# dicoVehicInfo : key :id du vehicule   
#                 valeur : liste de (orientation, coordoneeVariable en fonction de l orientation, taille vehicule)
# dicoConfigInit : key : id du vehicule  
#                  valeur : numero de la case (1 a 36)
dicoVehicInfo,dicoConfigInit = genereConfigInitiale(configuration2D,dimensionsGrille[1])  
# Definition du modele Gurobi
m = Model("gurobi") 
# creation des dictionnaires x,yz et generation de leurs variables de decisions
dicoX,dicoY,dicoZ= genereVarDecision(m,N,dicoVehicInfo,dimensionsGrille)
# mise a jour du modele
m.update()

# generation des contraintes du PL
genereContraintePosIniVehicules(m,dicoX,dicoConfigInit)
genereContMemeNbVehicPerTurn(m,N,dicoX,dicoVehicInfo)
genereCont1_VerifOccupCase(m,N,dicoX,dicoZ,dicoVehicInfo,dimensionsGrille) 
genereCont2_Singleton(m,N,dicoZ,dicoVehicInfo,dimensionsGrille) 
genereCont3_OccupationVi(m,N,dicoZ,dicoVehicInfo,dimensionsGrille) 
genereCont4_PasObstacleEntreJL(m,N,dicoX,dicoY,dicoZ,dicoVehicInfo,dimensionsGrille)
genereCont5a_PositionFinVoitureRouge(m,N,dicoX)
genereCont5b_OneMovePerRound(m,N,dicoY)
genereCont5c_majMarqueurSiMove(m,N,dicoX,dicoY,dicoVehicInfo)

#acceleration de la resolution
m.setParam("IntFeasTol",1e-9) 
# mise a jour du modele gurobi
m.update()
m.params.TimeLimit = 2*60

#debut = time.time()
obj = LinExpr();

objRHM =0


# ------------------- RHM -------------------------------------
for (i,j,l,k) in dicoY.keys():
    if k != 0:
        objRHM = objRHM + dicoY[(i,j,l,k)]
    # on set l'objectif : on minimise la somme de deplacements de tous les vehicules pour tous les tours
    m.setObjective(objRHM,GRB.MINIMIZE)    
    
debut = time.time()
m.optimize()
fin = time.time()

print "--------------------------- RHM ----------------------------------"
affichage(dicoY)
print "fichier : ",strFileName,  " nb variables max : " , N ,"temps d execution ", (fin - debut), " secondes "
print "\n\n"
#------------- RHC    
    
objRHC = 0
for (i,j,l,k) in dicoY.keys():
    if k != 0:
        if abs(j-l)%dimensionsGrille[0] == 0: 
            objRHC = objRHC + (abs(j-l)/dimensionsGrille[0]) * dicoY[(i,j,l,k)]
            #print "objRHC ",objRHC , dicoY[(i,j,l,k)], "\n"
        else:
            objRHC = objRHC + abs(j-l)*dicoY[(i,j,l,k)]
    m.setObjective(objRHC,GRB.MINIMIZE)  
    
debut = time.time()
m.optimize()
fin = time.time()
print "--------------------------- RHC ----------------------------------"
affichage(dicoY)
print "fichier : ",strFileName,  " nb variables max : " , N ,"temps d execution ", (fin - debut), " secondes "
 

