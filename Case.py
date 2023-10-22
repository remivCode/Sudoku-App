# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 09:01:18 2023

@author: rem3D
"""

class Case:
    def __init__(self,ligne, colonne):
        self.ligne = ligne
        self.colonne = colonne
        self.valeur = 0
        self.definir_region()
        
    def __repr__(self):
        """
        Permet d'afficher une instance case: (ligne, colonne, valeur)

        Returns
        -------
        None
        
        Params:
        -------
        None
        """
        return f"({self.ligne}, {self.colonne}, {self.valeur})"
    
            
    def definir_region(self):
        """
        Définie la région associée à la case. Les régions sont numérotées de 1 à 9 en partant d'en haut à gauche et en allant de gauche 
        à droite

        Returns:
        -------
        None.
        
        Params:
        -------
        None.

        """
        if self.ligne in range(3):
            if self.colonne in range(3):
                self.region = 1
            if self.colonne in range(3,6):
                self.region = 2
            if self.colonne in range(6,9):
                self.region = 3
        if self.ligne in range(3,6):
            if self.colonne in range(3):
                self.region = 4
            if self.colonne in range(3,6):
                self.region = 5
            if self.colonne in range(6,9):
                self.region = 6
        if self.ligne in range(6,9):
            if self.colonne in range(3):
                self.region = 7
            if self.colonne in range(3,6):
                self.region = 8
            if self.colonne in range(6,9):
                self.region = 9
                
if __name__ == "__main__":
    c = Case(1,2)