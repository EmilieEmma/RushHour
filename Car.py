# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 22:23:16 2016

@author: emilie
"""
couleursVoitures = ["#FFA500","#00FF00","#660033","#9933CC","#660000","#990000","#FF9966","#FFCC33",
            "#00FFFF","#0066FF","#003399","#666666","#CCFF33","#00CC99"]

couleursCamions = ["#00FFFF","#0066FF","#003399","#666666","#CCFF33","#00CC99",
            "#330000","#660000","#00FF00","#660033","#9933CC","#990000","#FF9966","#FFCC33"]

class Voiture(object):
    couleur = ""
    nom = ""
    orientation= ""
    taille = 0
    marqueur = (-1,-1)

    # The class "constructor" - It's actually an initializer 
    def __init__(self, nom, couleur, taille,marqueur):
        self.nom = nom
        self.couleur = couleur
        self.taille = taille
        self.marqueur = marqueur
    
    def __str__(self):
        """
        Override du toString de la grille entree
        """
        return "nom:"+str(self.nom)+" - coul:"+str(self.couleur)+" taille :" + str(self.taille) + " orient:" + str(self.orientation) #+ "\n"
        
    def getNom(self):
        return self.nom

    def getCouleur(self):
        return self.couleur    
    
    def getOrientation(self):
        return self.orientation       

    def getTaille(self):
        return self.taille      
    
    def majOrientation(self,coordTest):
        x,y = coordTest
        if x != self.marqueur[0] :
            self.orientation = "h"
        elif y != self.marqueur[1] :
            self.orientation = "v"

def make_voiture(nom, marqueur):
    if(nom[0] == 'g'):
        taille = 2
        couleur = "#FF0000"
    elif(nom[0] == 'c'):
        taille = 2
        couleur = couleursVoitures[int(nom[1])-1]
    elif(nom[0] == '0'):
        return 
    else:
        taille = 3
        couleur = couleursCamions[int(nom[1])-1]
    return Voiture(nom, couleur, taille,marqueur)