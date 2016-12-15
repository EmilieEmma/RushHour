# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 23:11:46 2016

@author: emilie
"""

try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here

import dijk_shortest as djka   
import numpy as np
import Car as voiture
from sets import Set
import time
import matplotlib.pyplot as plt

#positionButVoitureRouge = (2,5)
#configuration2D = lst = [[0] * colonnes] * lignes
#dicoConfigVoisins = {}
dicoCoords = {}
dicoVoitures = {}    # dico key : voiture value : voiture, couleur, taille, orientation
dicoConfigVoisines = {}
pileVoisinsATraiter= set()
dicoNoeudsDejaTraite = {}
coutRHC = 0
coutRHM = -1
#strFileName= "puzzles/test/question1.text"
#strFileName= "puzzles/test/question1b.text"
#strFileName="puzzles/test/test1.text"
#strFileName="puzzles/test/test2.text"
#strFileName="puzzles/test/test3.text"
#strFileName="puzzles/debutant/jam10.txt"
#strFileName="puzzles/debutant/jam2.txt"
#strFileName="puzzles/debutant/jam3.txt"
#strFileName="puzzles/intermediaire/jam18.txt"
#strFileName="puzzles/expert/jam31.txt"
strFileName="puzzles/expert/jam32.txt"
#strFileName="puzzles/expert/jam33.txt"
#strFileName="puzzles/expert/jam34.txt"
#strFileName="puzzles/expert/jam39.txt"
#strFileName="puzzles/expert/jam40.txt"
expertDirectory = "puzzles/expert/"
debutantDirectory = "puzzles/debutant/"
avanceDirectory = "puzzles/avance/"
intermediaireDirectory = "puzzles/intermediaire/"

from os import listdir
from os.path import isfile, join

totalFiles = []
expertFiles = [f for f in listdir(expertDirectory) if isfile(join(expertDirectory, f))]
debutantFiles = [f for f in listdir(debutantDirectory) if isfile(join(debutantDirectory, f))]
avanceFiles = [f for f in listdir(avanceDirectory) if isfile(join(avanceDirectory, f))]
intermediaireFiles = [f for f in listdir(intermediaireDirectory) if isfile(join(intermediaireDirectory, f))]
[totalFiles.append(f) for f in listdir(expertDirectory) if isfile(join(expertDirectory, f))]
[totalFiles.append(f) for f in listdir(debutantDirectory) if isfile(join(debutantDirectory, f))]
[totalFiles.append(f) for f in listdir(avanceDirectory) if isfile(join(avanceDirectory, f))]
[totalFiles.append(f) for f in listdir(intermediaireDirectory) if isfile(join(intermediaireDirectory, f))]


def affiche_error(message):
    # On crée une fenêtre, racine de notre interface
    fenetre = Tk()

    # On affiche le label dans la fenêtre
    texte1 = Label(fenetre, text=message, fg='red')
    # On affiche le label dans la fenêtre
    texte1.pack()
    

    c = Canvas(fenetre, width=(100), height=(100), bg='ivory')
    c.pack(side=TOP, padx=5, pady=5)
    
    boutonCharger = Button(fenetre, text='Charger', command = fenetre.bind)
    boutonCharger.pack(side=LEFT, padx=5, pady=5)
    boutonResoudre = Button(fenetre, text='Resoudre', command = fenetre.bind)
    boutonResoudre.pack(side=LEFT, padx=50, pady=5)
    boutonQuitter = Button(fenetre, text='Quitter', command = fenetre.destroy)
    boutonQuitter.pack(side=RIGHT, padx=5, pady=5)
    
    # On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
    fenetre.mainloop()

def affichage(dicoCoords):
    # On crée une fenêtre, racine de notre interface
    fenetre = Tk()

    # On crée un label dont le 1er parametre est l interface racine
    # On affiche le label dans la fenêtre
    texte1 = Label(fenetre, text="clef : " + clef, fg='red')
    # On affiche le label dans la fenêtre
    texte1.pack()
    
    texte2 = Label(fenetre, text="coutRHC total : " + str(coutRHC) + "  coutRHM total : " + str(coutRHM), fg='red')
    # On affiche le label dans la fenêtre
    texte2.pack()
    
    nbX = int(dimensionsGrille[0])
    nbY = int(dimensionsGrille[1])
    pas = 600/nbX
    listidrec=nbX*[[]] 
    listidtxt=nbX*[[]] 
    nom = ""

    c = Canvas(fenetre, width=(nbX*100), height=(nbY*100), bg='ivory')
    c.pack(side=TOP, padx=5, pady=5)
    
    for i in range(nbX): 
        listidrec[i]=nbX*[-1] 
        listidtxt[i]=nbX*[-1] 
    for i in range(nbX): 
        for j in range(nbY): 
            nom = dicoCoords[(i,j)].getNom() if dicoCoords[(i,j)] != None else ""
            listidrec[i][j] = c.create_rectangle(pas*i, pas*j, pas*(i+1), pas*(j+1), fill='#FFFFFF' if nom == "" else dicoCoords[(i,j)].getCouleur() )
            listidtxt[i][j] = c.create_text((pas*i + pas/2), (pas*j + pas/2), text=(nom))
    boutonCharger = Button(fenetre, text='Charger', command = fenetre.bind)
    boutonCharger.pack(side=LEFT, padx=5, pady=5)
    boutonResoudre = Button(fenetre, text='Resoudre', command = fenetre.bind)
    boutonResoudre.pack(side=LEFT, padx=50, pady=5)
    boutonQuitter = Button(fenetre, text='Quitter', command = fenetre.destroy)
    boutonQuitter.pack(side=RIGHT, padx=5, pady=5)
    
    # On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
    fenetre.mainloop()


def lectureFichier(strFileName):
    # Ouverture d'un fichier en *lecture*:    
    fichier = open(strFileName, "r")
    # ...
    # Utilisation du fichier
    # ...
    # dimensions de la grille => 1ere ligne du fichier
    dGrille = fichier.readline()
    nbX,nbY = dGrille.split()
    dimensionsGrille = (int(nbX),int(nbY))
    #print "dimensions : x : ", nbX," y: ", nbY
    configuration2D = [[0 for x in xrange(dimensionsGrille[0])] for y in xrange(dimensionsGrille[1])]

    i=0
    j=0
    # Car =>  nom, couleur, position, orientation, taille
    for ligne in fichier:
        cases = ligne.split()
        for caseValue in cases:
            if caseValue.find('g') == 0:        # on teste si la voiture rouge est sur la bonne ligne
                if j!= 2 :
                    affiche_error("la voiture rouge est sur une mauvaise ligne ")
                    sys.exit(0)
                
            if caseValue != '0' :    #presence d une voiture c: voiture , t: camion
                if not dicoVoitures.has_key(caseValue) :
                    dicoVoitures[caseValue] = voiture.make_voiture(caseValue,(i,j))
                else :
                    dicoVoitures[caseValue].majOrientation((i,j))   
                dicoCoords[(i,j)] = dicoVoitures[caseValue]
            else:
                dicoCoords[(i,j)] = None 
            configuration2D[j][i] = caseValue
            i=i+1
        i = 0 
        j=j+1
    # Fermeture du fichier
    fichier.close()
    print configuration2D
    return configuration2D, dimensionsGrille

"""
genere une clef de configuration a partir d une matrice 2D : (x,y)
renvoie une string
"""
def ConfigKeyMarqueurGenerator(configuration2D):
    i = 1
    clef = ""
    for y in xrange(dimensionsGrille[0]) :
        for x in xrange(dimensionsGrille[1]):
            # on identifier si la case est occupee et si c est le marqueur du vehicule => x!=x-1  et y!= y-1
            if configuration2D[y][x] != "0" and configuration2D[y][x] != configuration2D[y][x-1] and configuration2D[y][x] != configuration2D[y-1][x]:
                if configuration2D[y][x] == "g" :
                    conf = "g1"
                else:
                    conf = configuration2D[y][x]
                if i < 10 :
                    clef = clef + "0"+str(i)+ conf
                else:
                    clef = clef +str(i)+ conf
            i = i+1
    dicoConfigVoisines[clef] = set()  # dictionnaire de clef avec comme valeur un set (pour eviter les doublons) de clefs voisines avec leur cout
    pileVoisinsATraiter.add(clef)       # set pour eviter de traiter plusieurs fois le meme noeud 
    return clef

"""
    transforme une position (1,2,...,36) en coordonnees (x,y)
    renvoie un couple (x,y)
"""
def transformePositionCoord(pos) :
    x = (int(pos) % int(dimensionsGrille[0])) 
    if x == 0 :
        x = 6
    y = ((int(pos)-x) / (dimensionsGrille[1]))
    x = x-1
    return (x,y)

"""
    fonction mettant à jour le dictionnaire de coordonnées basée sur la clef
    (chaine de caractères) passée en paramètre
    dicoCoord => key : (x,y)  ; value : objet voiture associée à la case ou None
    entree : clef de configuration valide
    sortie : dictionnaire de coordonnées : clef=> (x,y) ; 
            valeur=> objet voiture associée à la case ou None
"""

def majDicoCoord(clef):
    x=y=0 
    for xx in xrange(dimensionsGrille[0]):
        for yy in xrange(dimensionsGrille[1]) :
            dicoCoords[(xx,yy)]=None 
     
    setCoupleVoitPos = trouverCouplesVoituresPositionVoisine(clef)
    for voit,pos in setCoupleVoitPos :
        if voit == "g1":
            voit = "g"
        orientation= dicoVoitures[voit].getOrientation()
        taille = dicoVoitures[voit].getTaille()
        x,y = transformePositionCoord(pos)
        if orientation =="h":
            for t in range(taille):
                dicoCoords[(x+t,y)] = dicoVoitures[voit]
        elif orientation == "v":
            for t in range(taille):
                dicoCoords[(x,y+t)] = dicoVoitures[voit]
    return dicoCoords
    
    
"""
fonction qui sequence les informations de la clef tous les 4 caracteres
pour retrouver idVoiture avec PositionMarqueur associe 
exemple de clef : 10t207c114g125c232t3 =>10t2 07c1 14g1 25c2 32t3
vehicule t2 en position 10
retourne un set de couple (idVoiture,Position)
"""
def trouverCouplesVoituresPositionInitiale(clef):
    #genere la clef en fonction du tableau 2D
    clef = ConfigKeyMarqueurGenerator(configuration2D)
    Iter = len(clef)/4      #definit le nombre d 'iterations pour la boucle for
    first= 0
    dataSet = Set()
    for i in range(Iter):       # iteration de 4 en 4 pour isoler les positions de chaque voiture ( "17g1") a partir de la clef
        dataSet.add((clef[first+2:4+first],clef[first:4+first-2]))
        first = first+ 4    
    return dataSet   # set de couple (voiture, position)
"""
    idem => est utilisee lors des iterations
"""    
def trouverCouplesVoituresPositionVoisine(clef):
    #genere la clef en fonction du tableau 2D
    Iter = len(clef)/4      #definit le nombre d 'iterations pour la boucle for
    first= 0
    dataSet = Set()
    for i in range(Iter):
        dataSet.add((clef[first+2:4+first],clef[first:4+first-2]))
        first = first+ 4    
    return dataSet
    
"""
   cree un dictionnaire de toute les positions occupees:
   key : position, valeur: idVoiture
   retourne le dictionnaire
"""
def setPositionsOccupees(setCouplesVoituresPositions) : #setCouplesVoituresPositions => set de couple (voiture, position)
    dicoPositionsOccupees = {}      # a partir d'une position occupee nous obtenons la voiture 
    for v,p in setCouplesVoituresPositions:
        if v == "g1":
            v="g"
        taille = dicoVoitures[v].getTaille()
        if dicoVoitures[v].getOrientation() == "h":
            for i in range(0,int(taille)):
                dicoPositionsOccupees[int(p)+i] = v
        else:
            for i in range(0,int(taille)*int(dimensionsGrille[1]),int(dimensionsGrille[1])):
                dicoPositionsOccupees[int(p)+i] = v
    return dicoPositionsOccupees  # dictionnaire : a partir d'une position occupee nous obtenons la voiture


"""
on constitue un dictionnaire de cases (voisines) ou un vehicule donne peut se deplacer
"""
def listeCasesValides(voit,position,dPositionsOccupees):
    setCoordVoisins = set()
    libre = 1
    if voit =="g1":
        voit = "g"
    taille = dicoVoitures[voit].getTaille()    
# test si orientation verticale ou horizontale
    if dicoVoitures[voit].getOrientation() == "h":
        # on calcule la position min et max de la ligne [de 1 a 36]
        pMin = int(position) - (int(position) % int(dimensionsGrille[1]))+1
        gMax = int(position) + int(dimensionsGrille[1]) - (int(position) % int(dimensionsGrille[1]))
        pMax = gMax - int(taille) +1    # calcule la position max sur la ligne de l avant du vehicule    
        #on traverse la partie droite de la ligne sur laquelle se trouve la voiture
        for p1 in range(int(position)+1, pMax+1):
            # si la future position de la tete du vehicule est vide ou si elle est occupee par le vehicule lui meme
            if not dPositionsOccupees.has_key(p1)  or dPositionsOccupees[p1] == voit :
                #on teste si les autres parties du vehicule peuvent aussi s y deplacer          
                for i in range(1,taille):
                    if dPositionsOccupees.has_key(p1+i)  and dPositionsOccupees[p1+i] != voit :
                        libre = 0
                if libre :
                    setCoordVoisins.add(p1)
                libre =1
            else:
                break
        #on traverse la partie gauche de la ligne sur laquelle se trouve la voiture
        for p1 in range(int(position)-1, pMin-1,-1):
            # si la future position de la tete du vehicule est vide ou si elle est occupee par le vehicule lui meme
            if not dPositionsOccupees.has_key(p1) or dPositionsOccupees[p1] == voit :
                #on teste si les autres parties du vehicule peuvent aussi s y deplacer
                for i in range(1,taille):
                    if dPositionsOccupees.has_key(p1+i)  and dPositionsOccupees[p1+i] != voit :
                        libre = 0
                if libre :
                    setCoordVoisins.add(p1)
                libre =1
            else:
                break
    else:
        # meme resonnement pour les vehicules positionnes verticalement
        pMin = (int(position) % int(dimensionsGrille[0])) 
        if pMin == 0 :
            pMin = 6
        gMax = (int(dimensionsGrille[0]) * int(dimensionsGrille[1])) - (int(dimensionsGrille[0]) - pMin) 
        pMax = gMax - (( int(taille)-1)*dimensionsGrille[0])
        #on traverse la partie basse de la colonne sur laquelle se trouve la voiture
        for p1 in range(int(position)+int(dimensionsGrille[0]), pMax+1,int(dimensionsGrille[0])):
            # si la future position de la tete du vehicule est vide ou si elle est occupee par le vehicule lui meme
            if not dPositionsOccupees.has_key(p1) or dPositionsOccupees[p1] == voit :
                #on teste si les autres parties du vehicule peuvent aussi s y deplacer attention a l incrementation
                for i in range((dimensionsGrille[0]),(taille-1)*int(dimensionsGrille[0])+1,int(dimensionsGrille[0])):
                    if dPositionsOccupees.has_key(p1+i)  and dPositionsOccupees[p1+i] != voit :
                        libre = 0
                if libre :
                    setCoordVoisins.add(p1)
                libre =1
            else:
                break
        #on traverse la partie haute de la colonne sur laquelle se trouve la voiture
        for p1 in range(int(position)-int(dimensionsGrille[0]), pMin-1,-int(dimensionsGrille[0])):
            # si la future position de la tete du vehicule est vide ou si elle est occupee par le vehicule lui meme
            if not dPositionsOccupees.has_key(p1) or dPositionsOccupees[p1] == voit :
                #on teste si les autres parties du vehicule peuvent aussi s y deplacer attention a l incrementation
                for i in range((dimensionsGrille[0]),(taille-1)*int(dimensionsGrille[0])+1,int(dimensionsGrille[0])):
                    if dPositionsOccupees.has_key(p1+i)  and dPositionsOccupees[p1+i] != voit :
                        libre = 0
                if libre :
                    setCoordVoisins.add(p1)
                libre =1
            else:
                break
    # on retourne un set de coordonnée voisines
    return setCoordVoisins
        
"""
touve les cases voisines d un vehicule ou son deplacement est possible
retourne un dictionnaire : clef: voiture ;valeur: liste de positions du marqueur de la voiture
"""
def trouverVoisinsValides(clef, dPositionsOccupees):
    setVoituresPos = trouverCouplesVoituresPositionVoisine(clef)
    dicoModifPositionVoitures = {}
    for voit,position in setVoituresPos :
        listPositions = []
        newMove = listeCasesValides(voit,position,dPositionsOccupees) # on recupere un set de coordonnées voisines
        # on traverse ce set et on creer la clef de configuration associee que l on place dans un dictionnaire        
        for i in newMove:
            if i <10:
                listPositions.append("0"+str(i)+voit)
            else:
                listPositions.append(str(i)+voit)
        if listPositions != [] :
            dicoModifPositionVoitures[voit] = listPositions
    return dicoModifPositionVoitures

"""
trouve l'indice d'une sous chaine de caractere dans une chaine de caratere
renvoie l indice
"""    
def find_str(s, char):
    index = 0
    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index
            index += 1
    return -1

"""
calcule le nombre de cases de deplacement du vehicule
"""
def calculCoutArcVoisin(oldSubStr,newSubStr,voiture):
    oldPos = oldSubStr[0:2]
    newPos = newSubStr[0:2]
    cout = np.abs(int(oldPos)-int(newPos))
    if voiture == "g1":
        voiture = "g"
    if dicoVoitures[voiture].getOrientation() == "v" :
        cout = cout / dimensionsGrille[0]
    return cout


"""
genere les clefs de configuration voisines a une clef passee en parametre
renvoie un dictionnaire de clef de config avec un set de couple (ses voisins,cout de deplacement)
"""
def creerConfigVoisines(clef,voisinsValides):
    for key,value in voisinsValides.items() :
        for ind in range(0,len(value)):
            # on isole l'index de la partie de la clef à modifier
            indexSubStr = find_str(clef,key)
            oldSubStr = clef[indexSubStr-2:indexSubStr+2]       
            newSubStr = value[ind]
            newKey = clef.replace(oldSubStr,newSubStr)
            cout = calculCoutArcVoisin(oldSubStr,newSubStr,key)
            if not dicoConfigVoisines.has_key(newKey) :
                dicoConfigVoisines[newKey] = set()
            if newKey != clef :
                dicoConfigVoisines[newKey].add((clef,cout))
                dicoConfigVoisines[clef].add((newKey,cout))
            if not dicoNoeudsDejaTraite.has_key(newKey):
                pileVoisinsATraiter.add(newKey)
    dicoNoeudsDejaTraite[clef]=clef
    return dicoConfigVoisines

"""
    genere un graphe complet de noeuds de configuration 
"""

def generationDuGraphe(configuration2D,dimensionsGrille):
    # lecture du fichier et on cree un dictionnaire de voitures, une matrice 2D et un couple de dimensions de la grille    
    clefInitiale = clef = ConfigKeyMarqueurGenerator(configuration2D)
    
    setCouplesVoituresPositions = trouverCouplesVoituresPositionInitiale(clef)
    dPositionsOccupees = setPositionsOccupees(setCouplesVoituresPositions)
    voisinsValides = trouverVoisinsValides(clef,dPositionsOccupees)
    creerConfigVoisines(clef,voisinsValides)
    i=0
    while len(pileVoisinsATraiter) > 0:
        clef = pileVoisinsATraiter.pop()
        setCouplesVoituresPositions = trouverCouplesVoituresPositionVoisine(clef)   # set de couple (voiture, position)
        dPositionsOccupees = setPositionsOccupees(setCouplesVoituresPositions)      # dictionnaire : a partir d'une position occupee nous obtenons la voiture
        voisinsValides = trouverVoisinsValides(clef,dPositionsOccupees)
        creerConfigVoisines(clef,voisinsValides)
        i=i+1
    return clefInitiale

"""
fonction generant tous les arcs existants entre une clef 
(une configuration valide) est sa clef voisine (une configuration voisines valide) 
avec son coût associé (nombre de cases de déplacement du véhicule)

entree : dictionnaire de toutes les configurations (clef), 
        associe a la liste de tous ses voisins directs (valeur)
sortie : couple :   - liste triplets (clef de configuration valide, 
                                      clef de configuratioin voisine valide, 
                                         cout de deplacement entre les 2) 
                    - liste de clefs (configurations valides) buts sans doublons
"""

def genereEdges(dicoConfigVoisines, positionBut) :
    edges = []
    clefsBut = set()
    for clef in dicoConfigVoisines.iterkeys() :
        for (clefVoisin,cout) in dicoConfigVoisines[clef] :
            edges.append((clef, clefVoisin, cout))
            if clef.find(positionBut) != -1 :
                clefsBut.add(clef)
            if clefVoisin.find(positionBut) != -1 :
                clefsBut.add(clefVoisin)
    return (edges, clefsBut)     

###  APPELS DES FONCTIONS
configuration2D,dimensionsGrille = lectureFichier(strFileName)    
clefInitiale = generationDuGraphe(configuration2D,dimensionsGrille)          # clef initiale pour Dijkstra
print "\n\n ====================================== \n\n"

###### on cherche le meilleur chemin pour RHC

edges, clefsBut = genereEdges(dicoConfigVoisines, "17g1") 
#print "EDGES : ", edges , "\n\n"
resultRHC=(None,None)       # resultat trouvé pour RHC : couple de valeur(clef de la configuration but, chemin trouvé correspondant) 
dijk = None
coutMiniRHM =  float("inf")
coutMiniRHC = float("inf")

for clefBut in clefsBut:
    # dijk 3-tuple : coutRHC,coutRHM, cheminOptimal RHC
    dijk = djka.dijkstra(edges, clefInitiale, clefBut)
    if coutMiniRHC > dijk[0] :
        coutMiniRHC = dijk[0]
        resultRHC = (clefBut,dijk)

clefBut,cheminRHC = resultRHC
print "MEILLEUR CHEMIN : ", cheminRHC
print "CLEF BUT RHC : " , clefBut

# trouver etapes de resolutions :
coutRHC = cheminRHC[0]
coutRHM = cheminRHC[1]
listeConfig = cheminRHC[2].split(',')
#print "listeConfig ", listeConfig

#affichage graphique du resultat du plus court chemin (non optimise car on cree à chaque configuration une nouvelle fenetre)
for clef in listeConfig:
    affichage(majDicoCoord(clef))



###### on cherche le meilleur chemin pour RHM
debut = time.time()    
for clefBut in clefsBut:
    # dijk 3-tuple : coutRHC,coutRHM, cheminOptimal RHM
    dijk = djka.dijkstra(edges, clefInitiale, clefBut)
    if coutMiniRHM > dijk[1] :
        coutMiniRHM = dijk[1]
        resultRHM = (clefBut,dijk)

clefBut,cheminRHM = resultRHM
print "MEILLEUR CHEMIN : ", cheminRHM
print "CLEF BUT RHM : " , clefBut
fin = time.time()

coutRHC = cheminRHM[0]
coutRHM = cheminRHM[1]
listeConfig = cheminRHM[2].split(',')


#affichage graphique du resultat du plus court chemin (non optimise car on cree à chaque configuration une nouvelle fenetre)
for clef in listeConfig:
    affichage(majDicoCoord(clef))


print "Nombre de configurations réalisables :", len(clefsBut)
print "fichier : ",strFileName, "temps d execution ", (fin - debut), " secondes "
