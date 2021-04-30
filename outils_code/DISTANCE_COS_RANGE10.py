#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 12:58:46 2021

@author: antonomaz
"""


import re
import glob
import spacy
import json
import sklearn
import os
import shutil
from sklearn.neighbors import DistanceMetric
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.cluster import AgglomerativeClustering
# from sklearn.metrics import pairwise_distances
# from sklearn import metrics
# import matplotlib.pyplot as plt
# import numpy as np


def liste_resultats(texte, nlp=spacy.load("fr_core_news_sm")):
    doc = nlp(texte)
    list_resultats =[]
    for ent in doc.ents:
        if ent.label_=="LOC":
            list_resultats.append(ent.text)
    return (list_resultats)


def lire_fichier (chemin):
    f = open(chemin , encoding = 'utf−8')
    chaine = f.read ()
    f.close ()
    return chaine

def stocker( chemin, contenu):

    w =open(chemin, "w")
    w.write(json.dumps(contenu , indent = 2))
    w.close()
    print(chemin)
    


def get_distances(texte1, texte2, N=1, liste_name =["jaccard", "braycurtis","dice", "cosinus"] ):
    dico = {}
    for metric_name in liste_name :
        dico[metric_name] = []
        liste_resultat_dist2 = []
        for n_max in range(1, N+1):###range([min, default = 0], max, [step, default = 1]) 
            V = CountVectorizer(ngram_range=(1,n_max ), analyzer='char') 
            X = V.fit_transform([texte1, texte2]).toarray()
            if metric_name!= "cosinus" :  
                dist = DistanceMetric.get_metric(metric_name)     
                distance_tab1=dist.pairwise(X)
                liste_resultat_dist2.append(distance_tab1[0][1])
            else: 
                distance_tab1=sklearn.metrics.pairwise.cosine_distances(X) 
                liste_resultat_dist2.append(distance_tab1[0][1])
            dico[metric_name] = liste_resultat_dist2
    return dico


## MAIN


path_corpora = "../DATA/corpora/*/"
# dans "corpora" un subcorpus = toutes les versions 'un texte'

for modele in ["sm","md", "lg"]:
#for modele in ["sm"]:
    print("Starting with modèle %s"%modele)
    nlp = spacy.load("fr_core_news_%s"%modele)
    
    for subcorpus in glob.glob("%s/*/"%path_corpora):
         
        print("Processing %s"%subcorpus)
        print(glob.glob("%s/*.txt"%subcorpus))
        for path in glob.glob("%s/*.txt"%subcorpus): 
            print(path)
            
            path_output = "%s_%s_spacy.json"%(path, modele)
            print(path_output)
            
            if os.path.exists(path_output)==True:
                print(f"Already Done {path_output}")
                
                continue
            
            filename = re.split("/", path)[-1]
#            print("****************FILENAME",filename)
            auteur,titre, version = re.split("_|\\\.", filename)
            texte = lire_fichier(path)
            entites = liste_resultats(texte, nlp)
            #entites= ["toto", "titi"]
#            
            stocker(path_output, entites)
#           
#    
#
#
path_to_evaluate = path_corpora 
## = "../data_Audoux/corpora/"

#print("*****VERSION OCR", version_OCR)
for subcorpus in glob.glob("%s/*"%path_corpora):
    if os.path.isdir(subcorpus) ==False:
        continue
           
        
   
    dico_out = {}
    dist_txt = {}
    for file_type in ["txt", "json"]:
        liste_compare = []
        for path_file in glob.glob("%s/*.%s"%(subcorpus, file_type)):
            
            
            filename = re.split("/", path_file)[-1]
            #print(filename)
            elems = re.split("_|\\.", filename)
            auteur,titre, version, modele = elems[0], elems[1],elems[-2], elems[-3]
#            print(modele)
            print("ELEMS", modele)
            if file_type =="txt":
                liste_compare.append([version, lire_fichier(path_file)])
            else:
                liste_compare.append([modele, lire_fichier(path_file)])
                
        print([x[0]for x in liste_compare])
        # liste_compare = [[version, toto[:1000]] for version, toto in liste_compare]#list comprehension
        dico_out[file_type] = {}
        for ID1 in range(len(liste_compare)):
            version1 = liste_compare[ID1][0]
            for ID2 in range(ID1+1, len(liste_compare)):
                version2 = liste_compare[ID2][0]
                dico_dist = get_distances(liste_compare[ID1][1], liste_compare[ID2][1], N=5)
                paire = "%s--%s"%(version1, version2)
                dico_out[file_type][paire] = dico_dist
    
    
       
    stocker("%s_%s_distances.json"%(subcorpus,titre), dico_out)
    
   
   

