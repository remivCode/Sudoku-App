#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 09:55:33 2023

@author: matheo
"""

import json
import math
import os

class User():

    def __init__(self):
        
        self.json_file = os.path.join("Data", "Users", "data_user.json")
        self.data = {}
        #self.colonnes = ['pseudo', 'mdp', 'meilleur temps', 'nombre de parties','temps total','temps moyen','classement']
        self.current_user= ''
        self.mdp = ''
        self.meilleur_temps = math.inf
        self.nombre_de_parties = 0
        self.temps_total = 0.0
        self.temps_moyen = 0.0
        self.points = 0
        self.classement = len(self.data)+1
        self.indices = 0
        self.lire_donnees_json()
        
    def lire_donnees_json(self):

        """

        Ici on lit le json et on attribue ses valeurs dans le dictionnaire data

        """
        try:                                            #On essaye de lire le fichier et on le créer si il n'existe pas
            with open(self.json_file, 'r') as f:
                self.data = json.load(f)
        except:
            with open(self.json_file, 'w') as f:
                json.dump(self.data, f)
            
                
    def ajouter_utilisateur_json(self, pseudonyme, mdp):

        """
        Ajoute un utilisateur dans le json avec son mdp
        
        Returns
        -------
        None
        
        Params
        -------
        String identifiant, String mot de passe
        

        """
        self.lire_donnees_json()
        self.data[pseudonyme] = {'mdp': mdp,'meilleur temps' : math.inf, 'nombre de parties': 0,'temps total' : 0,'temps moyen': 0,'points': 0, 'classement': len(self.data)+1}
        with open(self.json_file, 'w') as f:
            json.dump(self.data, f)
            
        
    def lire_data_user(self, user, mdp):

        """ 
        Cette méthode permet d'accéder aux données de l'utilisateur 
        dont le pseudonyme est self.current_user et actualise les stats de cet utilisateur.
        
        Returns
        -------
        None
        
        Params
        -------
        String identifiant, String mot de passe
        
        """
        
        info = self.data[user]
        self.current_user = user
        self.mdp = info['mdp']
        self.meilleur_temps = info['meilleur temps']
        self.nombre_de_parties = info['nombre de parties']
        self.temps_total = info['temps total']
        self.temps_moyen = info['temps moyen']
        self.points = info['points']
        self.classement = info['classement']  
        
    
    def actualiser_data_user(self, temps, difficulty):

        """ 
        On actualise les stats de l'utilisateur actuel dans le fichier json.
        
        Returns
        -------
        Float points gagnés pour cette partie
        
        Params
        -------
        Float temps, Int difficulté

        """
        if self.current_user:
            data = self.data[self.current_user]
            
            if temps < self.meilleur_temps and self.indices < 10:
                self.meilleur_temps = temps
            data['meilleur temps'] = self.meilleur_temps
            
            self.nombre_de_parties += 1
            data['nombre de parties'] = self.nombre_de_parties
            
            self.temps_total += temps
            data['temps total'] = self.temps_total
            
            self.temps_moyen = self.temps_total//self.nombre_de_parties
            data['temps moyen'] = self.temps_moyen
            
            points_partie = self.updatePoints(temps, difficulty)
            data['points'] = self.points
            
            self.updateClassement()
            
            with open(self.json_file, 'w') as f:
                json.dump(self.data, f)
                
            return points_partie
    

    def updatePoints(self, temps, difficulty):
        """
       On définit le nombre de points à ajouter en fonction de la difficultée, du temps et du nombre d'indices utilisés
       
        Returns
        -------
        Float point gagné pour cette partie
        
        Params
        -------
        Float temps, Int difficulté

        """
        
        #On défini le coef suivant le temps passé à résoudre le sudoku
        if temps >= 2700:
            coef_tps = 1
            
        elif temps >= 1800:
            coef_tps = 2
            
        elif temps >= 1200:
            coef_tps = 3
            
        elif temps >= 600:
            coef_tps = 4
            
        elif temps >= 0:
            coef_tps = 5
        
        #On défini le coefficient multiplicateur en fonction de la difficulté de sudoku
        if difficulty == 1:
            coef_dif = 1
        
        elif difficulty == 2:
            coef_dif = 1.25
            
        elif difficulty == 3:
            coef_dif = 1.5
            
        #On défini le coef pour le nombre d'indices utilisés
        if self.indices >= 15:
            coef_ind = 0
        elif self.indices >= 10:
            coef_ind = 0.25
        
        elif self.indices >= 4:
            coef_ind = 0.5
            
        elif self.indices >= 2:
            coef_ind = 0.75
        
        elif self.indices >= 0:
            coef_ind = 1
            
        point_ajoute = 100*coef_tps*coef_dif*coef_ind
        self.points += point_ajoute
        
        return point_ajoute
        
    
    def updateClassement(self):
        """
        Permet de redéfinir le classement des utilisateurs
        
        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        userList = []
        
        for user in self.data.keys():
            userList.append(self.data[user])
                
        while userList:
            minUser = userList[0]
            for user in userList:
                if user != userList:
                    if user['points'] < minUser['points']:
                        minUser = user
                    
            minUser['classement'] = len(userList)
            userList.remove(minUser)
                    
    def getClassement(self):
        """
        Permet de récupérer une liste du classement dans l'ordre
        
        Parameters
        ----------
        None.

        Returns
        -------
        Liste d'utilisateurs classé du meilleur au moins bon

        """
        classement=[]
        for i in range(1,len(self.data.keys())+1):
            for user in self.data.keys():
                if self.data[user]["classement"] == i:
                    classement.append(user)
                    
        return classement
            
            
                    
                    
                    
        
            

if __name__ == "__main__":
    stat = User()
    # stat.ajouter_utilisateur_json("tristan", "voiture")
    # stat.ajouter_utilisateur_json("baptiste", "voiture")
    stat.lire_data_user('tristan','voiture') # pour lire les données attribuées à tristan
    stat.actualiser_data_user(5,1) # d'actualise tout bien dans le json
    # stat.lire_data_user('baptiste','voiture')
    # stat.actualiser_data_user(5,1)
    # stat.lire_data_user('baptiste','voiture') # pour lire les données attribuées à tristan
    # stat.actualiser_data_user(5,1)
        