#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 20:08:32 2021

@author: antonomaz
"""
import glob , json, re

import matplotlib.pyplot as plt
import numpy as np


def lire_fichier (chemin):
    with open(chemin) as json_data: 
        dist =json.load(json_data)

    
    return dist

def nom_fichier(chemin):
    for mot in glob.glob(chemin): 
        noms_fichiers = re.split("/", chemin)
#        print("NOM FICHIER",noms_fichiers)
        
        nomsfich = re.split("\.",  noms_fichiers[3])
#        print(nomsfich)
        
        return nomsfich

def courbe(dist_courbe_mod, courbe_dist_txt):
    liste_n_max=[1, 2, 3, 4, 5]
    x=liste_n_max
#    plt.ylim(0,1)
    plt.plot(x,courbe_dist_txt[1], label=(courbe_dist_txt[0],courbe_dist_txt[-1]), linestyle='dotted')
    plt.plot(x,courbe_dist_txt[3], label=(courbe_dist_txt[2],courbe_dist_txt[-1]), linestyle='dotted')
    plt.plot(x,courbe_dist_txt[5], label=(courbe_dist_txt[4],courbe_dist_txt[-1]), linestyle='dotted')
    plt.plot(x,courbe_dist_txt[7], label=(courbe_dist_txt[6],courbe_dist_txt[-1]), linestyle='dotted')
    plt.plot(x,dist_courbe_mod[1], label=(dist_courbe_mod[0], dist_courbe_mod[-1]))
    plt.plot(x,dist_courbe_mod[3], label=(dist_courbe_mod[2], dist_courbe_mod[-1]))
    plt.plot(x,dist_courbe_mod[5], label=(dist_courbe_mod[4], dist_courbe_mod[-1]))
    plt.plot(x,dist_courbe_mod[7], label=(dist_courbe_mod[6], dist_courbe_mod[-1]))
#    
    
    plt.ylabel("Distances")
    plt.xlabel("n_max")
    plt.axis([0,6,0,1])
    
   
    
#    
 
    
    
def stocker_courbes(nomfich, mode): 
    
    name_fig = "%s.png"%(mode)
    print(" nom de la figure ", name_fig)
#    plt.legend(ncol=2)
    plt.legend(loc="lower left",bbox_to_anchor=(0.0,0.8), ncol=2)
    plt.legend 
#    plt.legend(loc='upper left')
#    plt.legend
    plt.savefig(nomfich)
    plt.clf()
    
    return nomfich



### MAIN

##pOUR UN FICHIER
#path ="./ADAM_kraken-17_Mon-village_distances_.json"
#path_dist=lire_fichier(path)
#print(path_dist)

#liste_name_metric=[]
dist_txt=[]
dist_sm=[]
dist_md=[]
dist_lg=[]
liste_courbe =[]

path_corpora ="../DISTANCES/*"
for chemin in glob.glob("%s/*"%path_corpora):
    path_dist=lire_fichier(chemin)
#    print(path_dist)
    nomfichier= nom_fichier(chemin)
#    print(chemin)
    print(nomfichier)
    print(path_corpora)
    
    dist_txt=[]
    dist_sm=[]
    dist_md=[]
    dist_lg=[]
    liste_courbe =[]
#    print(dist_txt)
#    print(dist_sm)
#    print(dist_md)
#    print(dist_lg)
    print(liste_courbe)  
    print("NOM FICHIER",nomfichier)
    for cle, dic in path_dist.items(): 
            
        print("l'élément de clé", cle)
            
            
        for version, modele in dic.items():
            print("  ",version )
            #        print("c'est le modèle ", modele)
                    
            for name_metric, liste in modele.items():
                print("      ", name_metric)
                
    #            for i in liste:
    #                print(i)
                        
                if cle == "txt" :
    #                
                    dist_txt.append(name_metric)
    #                print(liste)
                    dist_txt.append(liste)
       
                if version == "sm--sm" :
                    dist_sm.append(name_metric)
    #                print(liste)
                    dist_sm.append(liste)
                    
                if version == "md--md" :
                    dist_md.append(name_metric)
    #                print(liste)
                    dist_md.append(liste)
                    
                if version == "lg--lg":
                    dist_lg.append(name_metric)
    #                print(liste)
                    dist_lg.append(liste)
    
    dist_txt.append("TXT")                                    
    dist_sm.append("spacy-sm") 
    dist_md.append("spacy-md") 
    dist_lg.append("spacy-lg")               
        
    
        
    liste_courbe.append(dist_sm)
    liste_courbe.append(dist_md)
    liste_courbe.append(dist_lg)
         
    print(liste_courbe[0])
    #    print(liste_courbe[1])
    #    print(liste_courbe[2])
        
        
    courbe(liste_courbe[0], dist_txt)
    stocker_courbes(chemin+"courbe_%s.png"%(liste_courbe[0][-1]), liste_courbe[0][-1])
        
    courbe(liste_courbe[1], dist_txt)
    stocker_courbes(chemin+"courbe_%s.png"%(liste_courbe[1][-1]), liste_courbe[1][-1])
        
    courbe(liste_courbe[2], dist_txt)
    stocker_courbes(chemin+"courbe_%s.png"%(liste_courbe[2][-1]), liste_courbe[2][-1])

#nomfichier[0], 


             

                

              
           
      
