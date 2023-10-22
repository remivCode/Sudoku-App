#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Case import Case
from random import shuffle
import copy
import time

class Sudoku:
    
    def __init__(self, difficulty):
        start = time.time()
        self.difficulty = difficulty
        self.counter = 0                    #Compteur qui va permettre de compter le nombre de solutions pour une grille donnée afin de vérifier l'unicité des solutions
        
        self.grid_solution = self.createGrid()
        self.adjacence_solution = self.createAdjacence(self.grid_solution)
        self.grilleSolution(self.grid_solution)
        
        self.grid = copy.deepcopy(self.grid_solution)
        self.adjacence = self.createAdjacence(self.grid)          #Dictionnaire contenant pour chaque case les cases sur une même ligne, même colonne et même carré
        
        self.enleverCases()
        
        #Test des différentes grilles du temps de chargement
        if __name__ == "__main__":
            self.printTableau(self.grid_solution)
            print("\n")
            self.printTableau(self.grid)
            print("\n")
            end = time.time()
            self.duree = end-start
            print(self.duree)
        
    def relancerPartie(self):
        """
        Permet d'appeler les différentes méthodes pour créer les grilles

        Returns:
        -------
        None
        
        Params:
        -------
        None.
        """
        self.grid_solution = self.createGrid()
        self.adjacence_solution = self.createAdjacence(self.grid_solution)
        self.grilleSolution(self.grid_solution)
        self.grid = copy.deepcopy(self.grid_solution)
        self.adjacence = self.createAdjacence(self.grid)
        self.enleverCases()
    
    def createGrid(self):
        """
        Créer une grille de cases vides

        Returns:
        -------
        Grille
        
        Params:
        -------
        None.

        """
        num = 1
        grid = []
        
        for i in range(9):
            ligne = []
            for j in range(9):
                ligne.append(Case(i,j))         #Chaque case [numéro (de 1 à 81), valeur]
                num += 1
            grid.append(ligne)
            
        return grid
            
    def printTableau(self, grille):
        """
        Permet d'afficher une grille dans la console (Méthode ne servant qu'au test de la classe)

        Returns:
        -------
        None
        
        Params:
        -------
        Grille

        """     
        for ligne in grille:
            print(ligne)
            
    def parcoursLigne(self, grille, case):
        """
        Parcours la ligne d'une case spécifique et renvoie toutes les autres cases présentes sur cette ligne

        Returns:
        -------
        Liste de d'éléments de type Case
        
        Params:
        -------
        Instance de type Case, grille

        """
        ligne_index = case.ligne
        ligne = []
        for x in range(9):
            if grille[ligne_index][x] != case:
                ligne.append(grille[ligne_index][x])
        return ligne
    
    def parcoursColonne(self, grille, case):
        """
        Parcours la colonne d'une case spécifique et renvoie toutes les autres cases présentes sur cette colonne

        Returns:
        -------
        Liste de d'éléments de type Case
        
        Params:
        -------
        Instance de type Case, grille

        """
        colonne_index = case.colonne
        colonne = []
        for y in range(9):
            if grille[y][colonne_index] != case:
                colonne.append(grille[y][colonne_index])
        return colonne
    
    def parcoursRegion(self, grille, case):
        """
        Parcours la région 3x3 d'une case spécifique et renvoie toutes les autres cases présentes dans cette région

        Returns:
        -------
        Liste de d'éléments de type Case
        
        Params:
        -------
        Instance de type Case, grille

        """
        region = []
        index_region = case.region
        origine_ligne = 0               #Définie la ligne de la case en haut à gauche de la région considérée
        origine_colonne = 0             #Définie la colonne de la case en haut à gauche de la région considérée
        
        if index_region == 1:           #Pour chaque index de région, on associe la position "d'origine" de cette région à la case en haut à gauche de la région
            origine_ligne = 0
            origine_colonne = 0
        if index_region == 2:
            origine_ligne = 0
            origine_colonne = 3
        if index_region == 3:
            origine_ligne = 0
            origine_colonne = 6
        if index_region == 4:
            origine_ligne = 3
            origine_colonne = 0
        if index_region == 5:
            origine_ligne = 3
            origine_colonne = 3
        if index_region == 6:
            origine_ligne = 3
            origine_colonne = 6
        if index_region == 7:
            origine_ligne = 6
            origine_colonne = 0
        if index_region == 8:
            origine_ligne = 6
            origine_colonne = 3
        if index_region == 9:
            origine_ligne = 6
            origine_colonne = 6
        
        for ligne in range(3):
            for colonne in range(3):
                if grille[origine_ligne + ligne][origine_colonne + colonne] != case:
                    region.append(grille[origine_ligne + ligne][origine_colonne + colonne])
        return region
            
        
    def createAdjacence(self, grille):
        """
        Créer la liste d'adjacence qui va nous permettre d'implémenter la régle du sudoku

        Returns
        -------
        dictionnaire d'adjacence
        
        Params
        -------
        Grille

        """
        adjacence = {}
        
        for i in range(9):                                              #On parcours chaque case tu tableau
            for case in grille[i]:
                for case_ligne in self.parcoursLigne(grille, case):             #On ajoute chaque case sur la même ligne à la liste d'adjacence
                    if case not in adjacence.keys():
                        adjacence[case] = [case_ligne]
                    else:
                        if case_ligne not in adjacence[case]:
                            adjacence[case].append(case_ligne)
                        
                for case_ligne in self.parcoursColonne(grille, case):           #On ajoute chaque case sur la même colonne à la liste d'adjacence
                    if case_ligne not in adjacence[case]:
                        adjacence[case].append(case_ligne)
                    
                for case_ligne in self.parcoursRegion(grille, case):            #On ajoute chaque case sur la même région à la liste d'adjacence
                    if case_ligne not in adjacence[case]:
                        adjacence[case].append(case_ligne)
                    
        return adjacence
                    
    def nombreValide(self, case, nombre, adjacence):
        """
        Vérifie si un nombre peut être placé dans une case selon les règles du sudoku

        Returns
        -------
        Bool
        
        Params
        -------
        Case, nombre

        """
        for current in adjacence[case]:
            if current.valeur == nombre and current != 0:
                return False
                
        return True
        

    def grilleRemplie(self, grille):
        """
        Permet de vérifier si une grille est entièrement remplie (plus de case aillant 0 comme valeur)

        Returns
        -------
        Bool
        
        Params
        -------
        Grille

        """
        for i in range(9):
            for case in grille[i]:
                if case.valeur == 0:
                    return False
                
        return True

    def grilleSolution(self, grille):
        """
        Algorithme de backtracking permettant de créer une grille de solution. Elle prend en paramètre une grille solution vide d'abord.
        Le principe de cet algorithme est que pour chaque case, on choisit une valeure qui pourrait convenir, on explore jusqu'au bout si cette 
        valeur convient vraiment, et si elle ne convient pas, on remonte pour la changer.
        Returns
        -------
        False tant qu'aucune solution n'est trouvé, True quand il n'y a plus de case vide (solution trouvée)
        
        Params
        -------
        Grille

        """
        possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        for i in range(9):
            for case in grille[i]:
                if case.valeur == 0:
                    shuffle(possible)
                    for nombre in possible:
                        if self.nombreValide(case, nombre, self.adjacence_solution):
                            case.valeur = nombre
                            if self.grilleRemplie(grille):              #Une fois que la grille est remplie (plus de 0), la fonction renvoit True
                                return True
                            else:
                                if self.grilleSolution(grille):            #Si la grille n'est pas complète, on répète l'opération jusqu'à ce qu'elle le soit
                                    return True
                    
                    break           #Les instructions de break et continue servent à arrêter les deux boucles for en même temps pour re-parcourir l'entièretée de la grille à chaque mauvaise solution finale
            else:
                continue
            break
            

        case.valeur=0
        #La ligne précèdente est importante pour éviter les solutions où l'algorithme parcours toute la grille en trouvant une solution partielle
        #(contenant des 0). Lorsque cela se produit la fonction récursive renvoit False et il faut ajouter la ligne précédente pour mettre à 0 la dernière case pour ensuite pouvoir tester les nombre suivants dans la liste de nombre si c'est possible (sinon on remonte).
        return False
    
    def resoudreSudoku(self, grille):
        """
        Algorithme de backtracking permettant de résoudre une grille donnée. Elle prend en paramètre une grille partiellement remplie.
        Le principe est le même que l'algorithme de génération de sudoku. Cette méthode sera utilisé pour vérifier l'unicité des solutions d'une grille donnée.
        Returns
        -------
        False dans tous les cas
        
        Params
        -------
        Grille

        """
        possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        if self.counter > 1:        #On ne veut pas continuer à explorer si il y a déjà plus d'une solution
            return
        
        for i in range(9):
            for case in grille[i]:
                if case.valeur == 0:
                    shuffle(possible)
                    for nombre in possible:
                        if self.nombreValide(case, nombre, self.adjacence):
                            case.valeur = nombre
                            if self.grilleRemplie(grille):              #Une fois que la grille est remplie (plus de 0), la fonction renvoit True
                                self.counter += 1                       #On rentre dans cette condition lorsqu'on trouve une solution donc on incrémente le compteur
                                break                                   #Dans cette méthode, on veut continuer à chercher lorsqu'on trouve une solution donc on sort des boucles for pour renvoyer False et remonter pour trouver de nouvelles solutions potentielles
                            else:
                                if self.resoudreSudoku(grille):         #Si la grille n'est pas complète, on répète l'opération jusqu'à ce qu'elle le soit
                                    return 
                    
                    break           #Les instructions de break et continue servent à arrêter les deux boucles for en même temps pour re-parcourir l'entièretée de la grille à chaque mauvaise solution finale
            else:
                continue
            break
            
        case.valeur=0
        #La ligne précèdente est importante pour éviter les solutions où l'algorithme parcours toute la grille en trouvant une solution partielle
        #(contenant des 0). Lorsque cela se produit la fonction récursive renvoit False et il faut ajouter la ligne précédente pour mettre à 0 la dernière case pour ensuite pouvoir tester les nombre suivants dans la liste de nombre si c'est possible (sinon on remonte).
        #(mieux expliqué dans la description détaillé de la méthode grilleSolution)
        return False
    
    def casesNonVide(self, grille):
        """
        Méthode permettant de renvoyer une liste de toutes les cases non vides d'une grille

        Returns
        -------
        Liste
        
        Params
        -------
        Grille

        """
        non_vide = []
        for i in range(9):
            for case in grille[i]:
                if case.valeur != 0:
                    non_vide.append(case)
                    
        return non_vide
    
    def casesVide(self, grille):
        """
        Permet de chercher toutes les cases vides restantes de la grille en cours
        
        Returns
        -------
        Liste des cases vides
        
        Params
        -------
        Grille
        
        """
        case_vides = []
        for l in range(9):
            for case in grille[l]:
                if case.valeur == 0:
                    case_vides.append(case)
                    
        return case_vides
    
    def enleverCases(self):
        """
        Méthode permettant d'enlever des cases de la grille solution tout en vérifiant l'unicité des solutions de la grille proposée.
        Pour limiter le nombre de calculs et le temps d'exécution, on teste en prenant des cases vides aléatoirement si avec une grille solution on peut trouver une unique solution
        correspondant aux critères de difficulté. Sinon on change de grille solution en reprenant toutes les autres fonctions (ce qui est rapide)

        Returns
        -------
        None
        
        Params
        -------
        None

        """
        if self.difficulty == 1:                #On associe chaque difficulté à un nombre de cases à laisser remplies
            nbr_case = 40
        if self.difficulty == 2:
            nbr_case = 35
        if self.difficulty == 3:
            nbr_case = 25
        
        non_vide_a_tester = self.casesNonVide(self.grid)                 #On initialise toutes les cases de la grille remplie dans une liste
        nbr_non_vide = len(self.casesNonVide(self.grid))
        resolution = True
        
        while resolution and nbr_non_vide > nbr_case:        #Tant q'on a pas le nombre de cases souhaité ou qu'on a plus de cases non_vide à tester
            shuffle(non_vide_a_tester)
            case = non_vide_a_tester.pop()               #On choisit une case non_vide de la grille et on la supprime de la liste
            nbr_non_vide -= 1
            case.valeur = 0                     #On la "vide"
            self.counter = 0
            self.delai = 0
            self.resoudreSudoku(self.grid)      #On essaye de résoure (rapidement) le sudoku en aillant enlevé cette case et en vérifiant qu'il n'y ait pas plusieurs solutions avec self.counter
            if self.counter != 1:               
                resolution = False
                
        # print(nbr_non_vide)
        if nbr_non_vide > nbr_case+5:
            self.relancerPartie()           #Si l'algorithme ne trouve pas de grille ayant entre le nombre de case souhaité +5, ou prend trop de temps, on relance en créant une nouvelle solution
        #On peut tester l'algo en printant le nombre de passage dans cette condition ainsi que le nombre de cases remplies avant de rentrer dans la condition.
     
    def indice(self):
        """
        Permet de modifier la grille en cours pour remplacer une de ses cases vide par une
        case de la grille solution
        
        Returns
        -------
        None
        
        Params
        -------
        None
        
        """
        vide = self.casesVide(self.grid)
        shuffle(vide)
        
        case_vide = vide[0]
        ligne = case_vide.ligne
        colonne = case_vide.colonne
        
        case_indice = self.grid_solution[ligne][colonne]
        
        return ligne, colonne, case_indice.valeur
    
    def erreurSudoku(self):
        """
        Vérifie si il y a une erreur dans la liste
        Returns
        -------
        None si pas d'erreur, La première case d'erreur si il y a une erreur
        
        Params
        -------
        None
        
        """
        for l in range(9):
            for case in self.grid[l]:
                case_solution = self.grid_solution[case.ligne][case.colonne]
                if case.valeur != case_solution.valeur and case.valeur != 0:
                    return case
                    
        return
    

if __name__ == "__main__":
    a = Sudoku(3)