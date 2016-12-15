# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 09:22:52 2016

@author: emilie
"""
import matplotlib.pyplot as plt
#from numpy import arange, array,one,linalg
#from pylab import plot,show

strFileName="plot/plot_dijkstra_plot"
plotTmps=[]
plotNbConfig=[]
plotFileName=[]

def lectureFichier(strFileName):
    # Ouverture d'un fichier en *lecture*:    
    fichier = open(strFileName, "r")

    # Car =>  nom, couleur, position, orientation, taille
    for lignes in fichier: 
        champs = lignes.split()
        plotFileName.append(champs[0])
        plotNbConfig.append(champs[1])
        plotTmps.append(champs[2])
        
    # Fermeture du fichier
    fichier.close()
    #print plotFileName," --- ", plotNbConfig, " =====> ", plotTmps
    return plotFileName, plotNbConfig,plotTmps


"""
def generePlot():

    
    Affiche et sauvegarde le plot des temps moyens d execution
    avec nbInst iteration pour N=M=10,20,30,40,50
    
    rangeN = range(N_MIN,N_MAX+N_STEP,N_STEP)
    listTps =  list()
    for N in rangeN:
        tps = resQC(N, nbInst)
        if not tps is None:
            listTps.append(tps)
    if listTps == []:
        return None
    tabTps = np.array(listTps)
    
    plt.plot(rangeN,tabTps,'ro-')
    # on donne un titre
    plt.title("Temps en fonction de N")
    # on attribut des labels au axes
    plt.xlabel("Taille de la grille (N,N=M)")
    plt.ylabel("Temps d'execution (secondes)")
    plt.grid()
    # on sauvegarde la figure dans un dossier plot
    plt.savefig("Plots/plotQuestC.png")
    plt.show()
"""

plotFileName, plotNbConfig,plotTmps = lectureFichier(strFileName)


print plotFileName, plotNbConfig,plotTmps
print min(plotNbConfig),min(plotTmps)
miniNbConfig = min(plotNbConfig)
miniTmps = min(plotTmps)

plt.scatter(plotNbConfig,plotTmps)
plt.title("Dijkstra\n  Temps d'execution / Nombre de configurations valides")
plt.xlabel('nb de configurations valides')
plt.ylabel('temps d execution')
# on sauvegarde la figure dans un dossier plot
#plt.savefig("plot/plot_dijkstra.png")
plt.show()

"""plt.plot(miniNbConfig,plotNbConfig,'ro-')
# on donne un titre
plt.title("Temps en fonction de N")
# on attribut des labels au axes
plt.xlabel("Taille de la grille (N,N=M)")
plt.ylabel("Temps d'execution (secondes)")
plt.grid()
# on sauvegarde la figure dans un dossier plot
plt.savefig("plot/plot_dijkstra.png")
plt.show()
"""
"""
z=len(plotNbConfig) 
y=plotNbConfig[0] 
for i in range(z): 
    if y>plotNbConfig[i] and plotNbConfig[i] !="-1": 
        print plotNbConfig[i]
        y=plotNbConfig[i]
print "plotNbConfig ",y

rangeN = range(N_MIN,N_MAX+N_STEP,N_STEP)

plt.plot(rangeN,tabTps,'ro-')
# on donne un titre
plt.title("Temps en fonction de N")
# on attribut des labels au axes
plt.xlabel("Taille de la grille (N,N=M)")
plt.ylabel("Temps d'execution (secondes)")
plt.grid()
# on sauvegarde la figure dans un dossier plot
plt.savefig("plot/plot_dijkstra.png")
plt.show()
"""