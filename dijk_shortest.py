# -*- coding: utf-8 -*-

from collections import defaultdict
from heapq import *


def dijkstra(arcs, clefInitiale, clefBut):
    dicoVoisinsCouts = defaultdict(list)   # transforme liste en dico
    for noeudA,noeudB,coutRHC in arcs:     # noeudA, noeudB, coutRHC
        dicoVoisinsCouts[noeudA].append((coutRHC,noeudB))  #dico[noeudA]= (coutRHC,coutRHM,noeudB)

    queue, NoeudsDejaVisites = [(0,0,clefInitiale,"")], set()     #initialisation de la queue avec noeud depart coutRHC=0, et le chemin
                                    # set de noeud deja visite
    while queue:                        
        (coutRHC,coutRHM,noeudA,chemin) = heappop(queue) #heap queue 
        if noeudA not in NoeudsDejaVisites:
            NoeudsDejaVisites.add(noeudA)
            if chemin == "":
                chemin = noeudA
            else:
                chemin = chemin +","+noeudA
            if noeudA == clefBut: 
                return (coutRHC,coutRHM, chemin)
            for c, noeudB in dicoVoisinsCouts.get(noeudA, ()):
                if noeudB not in NoeudsDejaVisites:
                    heappush(queue, (coutRHC+c,coutRHM+1, noeudB, chemin)) #heap queue 
    return float("inf")
