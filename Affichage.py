# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter as tk
from tkinter import ttk
from ttkwidgets import TickScale
import csv
from tkinter import scrolledtext
from tkinter import messagebox
from Sudoku import Sudoku
from User import User
import pygame
from time import strftime, gmtime
import math
import os
from datetime import datetime

class Main():
    
    def __init__(self):
        self.racine = tk.Tk()
        self.racine.title('SODOKU')
        
        #Création des variables globales
        self.connected = False
        
        #Création de la fenêtre d'acceuil
        self.fenetre_principale(self.racine)
        
    def fenetre_principale(self, root):
        '''
        cette fonction permet de créer une fenetre top level utilisée comme fenetre d'accueil et appelle la fonction "widget_fen_principale"

        Returns
        -------
        None.

        '''
        #Création de la fenêtre
        self.accueil = tk.Toplevel(root)
        self.accueil.resizable(False, False)
        
        #Initialization des variables
        self.image_oeil = tk.PhotoImage(file = os.path.join("Data", "Images", "open_eye.png"))            #Mettre en os.path.join
        self.image_logo = tk.PhotoImage(file = os.path.join("Data", "Images", "logo_sudoku.png"))
        self.image_icon = tk.PhotoImage(file = os.path.join("Data", "Images", "icon_sudoku.png"))
        
        #Création de l'icone des fenêtres
        self.racine.iconphoto(True, self.image_icon)
        
        #Configuration des styles
        self.style = ttk.Style()
        self.style.configure("topSection.TButton", background = "light blue")
        
        #Création des widgets
        self.widget_fen_accueil()
        
        #Création de l'instance de statistiques de l'utilisateur
        if not self.connected:                  #On vérifie si l'utilisateur n'est pas déjà connecté pour qu'il n'est pas à se reconnecter à chaque fois qu'il revient à l'acceuil
            self.userStat = User()
        
        
    def widget_fen_accueil (self):
        '''
        Créer les widgets de la fenêtre d'accueil
        
        Params
        ------
        None.
        
        Returns
        -------
        None.

        '''
        
        if self.connected:
            self.afficherInfoUser()
        else:
            self.topSectionNotConnected = tk.Frame(self.accueil, bg="light blue")
            self.topSectionNotConnected.grid(row=0, column=0, columnspan=3)
        
            self.bouton1 = ttk.Button(self.topSectionNotConnected, text = "S'identifier", style="topSection.TButton")
            self.bouton1.grid(row=0, column=3, pady=5, sticky=tk.E)
            self.bouton1.bind('<Button-1>', self.login)
            
            self.bouton2 = ttk.Button(self.topSectionNotConnected, text = "Créer un compte", style="topSection.TButton")
            self.bouton2.grid(row=0, column=2, padx=(100,0), pady=5, sticky=tk.E)
            self.bouton2.bind('<Button-1>', self.signup)
            
            self.bouton3 = ttk.Button(self.topSectionNotConnected, text = "Classement", style="topSection.TButton")
            self.bouton3.grid(row=0, column=0, padx=(5,200), pady=5, sticky=tk.W)
            self.bouton3.bind('<Button-1>', self.afficherClassement)
            
            
        self.logo_frame = ttk.Label(self.accueil, image=self.image_logo)
        self.logo_frame.grid(row = 2, column=0, columnspan=4, pady=(20,10)) 
        
        self.titreDifficulte = tk.Label(self.accueil, text="Difficulté")
        self.titreDifficulte.grid(row=3, column=0, columnspan=4, padx=20, pady=(20,0))
        
        self.variableDifficulty = tk.IntVar()
        self.scaleDifficulte = TickScale(self.accueil, resolution=1, from_=1, to=3, tickinterval=1, showvalue=False, digits=0, variable=self.variableDifficulty)
        self.scaleDifficulte.grid(row=4, column=0, columnspan=4, padx=20, pady=5)
        
        self.bouton4 = ttk.Button(self.accueil, text = "Lancer la partie")
        self.bouton4.bind("<Button-1>", lambda event, difficulty=1: self.fenetreJeu(event, difficulty))         #valeur de la difficulté a récupérer
        self.bouton4.grid(row=5, column=2, padx =20, pady=(5,20))
        
        self.quitter = ttk.Button(self.accueil, text = "Quitter l'application")
        self.quitter.bind("<Button-1>", self.quitterApp)
        self.quitter.grid(row=5, column=0, padx=5, pady=(5,20))
        
        self.accueil.focus()
        
    def quitterApp(self, event):
        '''
        Permet de quitter l'application
        
        Returns
        -------
        None.
        
        Params
        -------
        Event

        '''
        if tk.messagebox.askokcancel("", "Etes-vous sur de vouloir quitter l'application?"):
            self.accueil.destroy()
            self.racine.destroy()
        
    def login (self, event):
        '''
        cette fonction permet d'ouvir une nouvelle TOPLEVEL qui va proposer à l'utilisateur de s'identifier avec son login et son mot de passe'
        
        Returns
        -------
        None.
        
        Params
        -------
        Event

        '''
    
        self.log = tk.Toplevel(self.accueil)
        self.log.resizable(False,False)
        self.log.focus()
        
        self.label_log_NomUtilisateur = ttk.Label(self.log, text = "Nom d'utilisateur : ")
        self.label_log_NomUtilisateur.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.entry_log_NomUtilisateur = ttk.Entry(self.log, text = '')
        self.entry_log_NomUtilisateur.grid(row=0, column=1, sticky=tk.E, padx=5, pady=5)
        
        self.label_log_MDP = ttk.Label(self.log, text = "Mot de passe : ")
        self.label_log_MDP.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.entry_log_MDP = ttk.Entry(self.log, text = '', show="*")
        self.entry_log_MDP.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)
        
        self.log_bouton_afficherMDP = ttk.Button(self.log, image= self.image_oeil)
        self.log_bouton_afficherMDP.bind("<ButtonPress-1>", lambda event, entry=self.entry_log_MDP: self.afficherMDP(event, entry))
        self.log_bouton_afficherMDP.bind("<ButtonRelease-1>", lambda event, entry=self.entry_log_MDP: self.nonAfficherMDP(event, entry))
        self.log_bouton_afficherMDP.grid(row=1, column=2, sticky=tk.E)
        
        self.log_Valider = ttk.Button(self.log, text = 'Valider' )
        self.log_Valider.bind("<Button-1>", self.connecter)
        self.log_Valider.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)
        
    def afficherClassement(self, event):
        """
        Permet d'ouvrir une fenêtre affichant le top5
        
        Parameters
        ----------
        Event

        Returns
        -------
        None.

        """
        self.classement = tk.Toplevel(self.accueil)
        self.classement.resizable(False,False)
        
        self.titreClassement = tk.Label(self.classement, text = "Classement")
        self.titreClassement.grid(row=0, column=0, columnspan=3)
        
        self.separator = ttk.Separator(self.classement, orient="horizontal")
        self.separator.grid(row=1, column=0, columnspan=3, ipadx=60, pady=5)
        
        self.leftColor = tk.Frame(self.classement, bg="light blue", width=50, height=200)
        self.leftColor.grid(row=2, column=0, rowspan=5)
        
        self.rightColor = tk.Frame(self.classement, bg="light blue", width=50, height=200)
        self.rightColor.grid(row=2, column=2, rowspan=5)
        
        classement = self.userStat.getClassement()

        if len(classement) < 5:
            for i in range(5-len(classement)):
                classement.append(None)                 #Pour pouvoir afficher le top5 même si il n'y a pas encore 5 joueurs enregistrés

        self.premier = tk.Label(self.classement, text=f"1er: {classement[0]}", width=20)
        self.premier.grid(row=2, column=1)
        self.deuxieme = tk.Label(self.classement, text=f"2ème: {classement[1]}", width=20)
        self.deuxieme.grid(row=3, column=1)
        self.troisieme = tk.Label(self.classement, text=f"3ème: {classement[2]}", width=20)
        self.troisieme.grid(row=4, column=1)
        self.quatrieme = tk.Label(self.classement, text=f"4ème: {classement[3]}", width=20)
        self.quatrieme.grid(row=5, column=1)
        self.cinquieme = tk.Label(self.classement, text=f"5ème: {classement[4]}", width=20)
        self.cinquieme.grid(row=6, column=1, padx=(0,5))

        
    def afficherInfoUser(self):
        '''
        Permet de changer l'affichage de l'acceuil pour afficher les infos de l'utilisateur connecté
        
        Returns
        -------
        None.
        
        Params
        -------
        Event

        '''
        try:                                                    #Si on est déjà connecté, on n'enlève pas la top section non connectée
            self.topSectionNotConnected.grid_remove()
        except:
            pass
        
        self.topSectionConnected = tk.Frame(self.accueil, bg="light blue")
        self.topSectionConnected.grid(row=0,column=0,columnspan=3)
        
        self.bouton3 = ttk.Button(self.topSectionConnected, text = "Classement", style="topSection.TButton")
        self.bouton3.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.bouton3.bind('<Button-1>', self.afficherClassement)
        
        self.deconnecter = ttk.Button(self.topSectionConnected, text = "Déconnecter", style="topSection.TButton")
        self.deconnecter.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.deconnecter.bind('<Button-1>', self.deconnecterUser)
        
        self.statAvance = ttk.Button(self.topSectionConnected, text="Statistiques avancées", style="topSection.TButton")
        self.statAvance.grid(row=0, column=2, padx=(5,200), pady=5, sticky=tk.W)
        self.statAvance.bind('<Button-1>', self.statistiques)
        
        self.afficheId = tk.Label(self.topSectionConnected, text = self.userStat.current_user, bg="light blue")
        self.afficheId.grid(row=0, column=3, padx=5, sticky="nsew", pady=5)
        self.createBarreInfo(self.afficheId, "Votre nom d'utilisateur")
        
        try:
            self.afficheMeilleurTemps = tk.Label(self.topSectionConnected, text = strftime("%Mmin %Ss", gmtime(self.userStat.meilleur_temps)), bg="light blue")         #On évite l'erreur si le temps à afficher est l'infini (lors de la création d'un compte)
        except:
            self.afficheMeilleurTemps = tk.Label(self.topSectionConnected, text = "00min 00s", bg="light blue")
        
        self.afficheMeilleurTemps.grid(row=0, column=6, padx=5, sticky="nsew", pady=5)
        self.createBarreInfo(self.afficheMeilleurTemps, "Votre meilleur temps actuelle, lancez une nouvelle partie\n pour tenter de l'améliorer!")
        
        self.affichePoints = tk.Label(self.topSectionConnected, text =f"{int(self.userStat.points)} Points", bg="light blue")
        self.affichePoints.grid(row=0, column=5, padx=5, sticky="nsew", pady=5)
        self.createBarreInfo(self.affichePoints, "Votre score, gagnez des points à chaque fois\n que vous finissez un sudoku!")
        
        if self.userStat.classement == 1:
            texte_classement = f"{self.userStat.classement}er"
        else:
            texte_classement = f"{self.userStat.classement}ème"
        
        self.afficheClassement = tk.Label(self.topSectionConnected, text = texte_classement, bg="light blue")
        self.afficheClassement.grid(row=0, column=4, padx=5, sticky="nsew", pady=5)
        self.createBarreInfo(self.afficheClassement, "Votre classement, mesurez vous aux meilleurs joueurs\n et tentez d'obtenir la meilleur position!")
        
    def createBarreInfo(self, widget, text):
        """
        Permet de détecter quand on passe sur un élément sur lequel on veut afficher une barre d'info contenant un texte
        
        Params
        -------
        Widget en question, texte à afficher
        
        Returns
        -------
        None.

        """
        def enter(event):
            self.showBarreInfo(text)
        def leave(event):
            try:                                #Même si il n'y a pas de raison de leave sans qu'il n'y ait de barre d'info, on évite l'erreur
                self.barreInfo.destroy()
            except:
                pass
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)   
        
    def showBarreInfo(self, text):
        """
        Permet d'afficher une barre d'info en bas à gauche d'un élément
        
        Params
        -------
        Texte à afficher
        
        Returns
        -------
        None.

        """
        self.barreInfo = tk.Toplevel(self.racine)
        barreInfo = tk.Label(self.barreInfo, text=text, bg='#e6e6e6')
        barreInfo.pack()
 
        self.barreInfo.overrideredirect(True) #Pour enlever la barre en haut de la fenêtre toplevel
 
        x = self.racine.winfo_pointerx() + 20
        y = self.racine.winfo_pointery() + 20
        self.barreInfo.geometry("+{}+{}".format(x, y))
        
    def deconnecterUser(self, event):
        """
        Change l'affichage de la fenêtre d'accueil et déconnecte l'utilisateur de la classe user
        
        Returns
        -------
        None.

        """
        if tk.messagebox.askokcancel("","Êtes-vous sur de vouloir vous déconnecter?"):
            self.connected = False
            self.userStat = User()
            self.accueil.destroy()
            self.fenetre_principale(self.racine)
        
    def signup(self, event):
        """
        cette fonction permet d'ouvvrir une nouvelle TOPLEVEL qui gère l'affichage pour créer un nouveau compte 

        Returns
        -------
        None.

        """
        self.sign = tk.Toplevel(self.accueil)
        self.sign.resizable(False,False)
        self.sign.focus()
        
        self.label_NomUtilisateur = ttk.Label(self.sign, text = "Nom d'utilisateur: ")
        self.label_NomUtilisateur.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.entry_NomUtilisateur = ttk.Entry(self.sign, text = '')
        self.entry_NomUtilisateur.grid(row=0, column=1, sticky=tk.E, padx=5, pady=5)
        
        self.label_MDP= ttk.Label(self.sign, text = "Mot de passe: ")
        self.label_MDP.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.entry_MDP = ttk.Entry(self.sign, show="*", text="")
        self.entry_MDP.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)
        
        self.bouton_afficherMDP = ttk.Button(self.sign, image= self.image_oeil)
        self.bouton_afficherMDP.bind("<ButtonPress-1>", lambda event, entry=self.entry_MDP: self.afficherMDP(event, entry))
        self.bouton_afficherMDP.bind("<ButtonRelease-1>", lambda event, entry=self.entry_MDP: self.nonAfficherMDP(event, entry))
        self.bouton_afficherMDP.grid(row=1, column=3, sticky=tk.E)
        
        self.label_ConfirmMDP = ttk.Label(self.sign, text = "Confirmer mot de passe: ")
        self.label_ConfirmMDP.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.entry_ConfirmMDP = ttk.Entry(self.sign, show="*")
        self.entry_ConfirmMDP.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)
        
        self.bouton_afficherConfirmerMDP = ttk.Button(self.sign, image= self.image_oeil)
        self.bouton_afficherConfirmerMDP.bind("<ButtonPress-1>", lambda event, entry=self.entry_ConfirmMDP: self.afficherMDP(event, entry))
        self.bouton_afficherConfirmerMDP.bind("<ButtonRelease-1>", lambda event, entry=self.entry_ConfirmMDP: self.nonAfficherMDP(event, entry))
        self.bouton_afficherConfirmerMDP.grid(row=2, column=3, sticky=tk.E)
        
        self.bouton_creerCompte = ttk.Button(self.sign, text = 'Créer mon compte')
        self.bouton_creerCompte.bind("<Button-1>", self.creerCompte)
        self.bouton_creerCompte.grid(row=3, column=1, sticky=tk.E, padx=5, pady=5)
        
    def afficherMDP(self, event, entry):
        """
        Rends le text écrit dans une entry donnée en paramètre visible
        Returns
        -------
        None.

        Params
        -------
        Event, widget entry
        """
        entry.config(show = "")
        
    def nonAfficherMDP(self, event, entry):
        """
        Rends le text écrit dans une entry donnée en paramètre invisible
        Returns
        -------
        None.

        Params
        -------
        Event, widget entry
        """
        entry.config(show = "*")          
    
    def creerCompte(self, event):
        """
        Utilise la classe User pour créer un compte si toutes les conditions sont remplies
        
        Returns
        -------
        None.

        Params
        -------
        Event
        """
        id_ = self.entry_NomUtilisateur.get() 
        mdp = self.entry_MDP.get()
        cmdp =  self.entry_ConfirmMDP.get()
        
        if id_ and mdp and cmdp:
            
            if id_ not in self.userStat.data.keys():
                
                if mdp == cmdp:
                    self.userStat.ajouter_utilisateur_json(id_, mdp)
                    self.userStat.lire_data_user(id_, mdp)
                    self.sign.destroy()
                    self.afficherInfoUser()
                    self.connected = True
                else:
                    self.entry_MDP.delete(0,tk.END)
                    self.entry_ConfirmMDP.delete(0,tk.END)
                    tk.messagebox.showerror("", "Mot de passe incorrect.")
                    
            else:
                self.entry_NomUtilisateur.delete(0,tk.END)
                self.entry_MDP.delete(0,tk.END)
                self.entry_ConfirmMDP.delete(0,tk.END)
                tk.messagebox.showerror("", "Ce nom d'utilisateur est déjà utilisé.")
                
        else:
            self.entry_NomUtilisateur.delete(0,tk.END)
            self.entry_MDP.delete(0,tk.END)
            self.entry_ConfirmMDP.delete(0,tk.END)
            tk.messagebox.showerror("", "Veuillez remplir tous les champs.")
        
    def connecter(self, event):
        """
        Utilise la classe User pour reconnaitre un utilisateur et récupérer ses informations
        
        Returns
        -------
        None.

        Params
        -------
        Event
        """
        user = self.entry_log_NomUtilisateur.get()
        mdp = self.entry_log_MDP.get()
        
        if user and mdp:
            
            if user in self.userStat.data.keys():
                
                if self.userStat.data[user]['mdp'] == mdp:
                    self.userStat.lire_data_user(user, mdp)
                    self.log.destroy()
                    self.afficherInfoUser()
                    self.connected = True
                else:
                    self.entry_log_MDP.delete(0,tk.END)
                    tk.messagebox.showerror("", "Mot de passe incorrect.")
                    
            else:
                self.entry_log_MDP.delete(0,tk.END)
                self.entry_log_NomUtilisateur.delete(0,tk.END)
                tk.messagebox.showerror("", "Ce nom d'utilisateur n'existe pas.")
                
        else:
            self.entry_log_MDP.delete(0,tk.END)
            self.entry_log_NomUtilisateur.delete(0,tk.END)
            tk.messagebox.showerror("","Veuillez remplir tous les champs.")
            
    
    def statistiques(self, event):
        """
        cette fonction permet de gerer l'affichage pour les statistiques du joueur enregistré au préalable

        Returns
        -------
        None.

        Params
        -------
        Event
        """
        self.stats = tk.Toplevel(self.accueil)
        self.stats.resizable(False,False)
        
        self.nomUtilisateur = tk.Label(self.stats, text = self.userStat.current_user)
        self.nomUtilisateur.grid(row=0, column=0, columnspan=3)
        
        self.separator = ttk.Separator(self.stats, orient="horizontal")
        self.separator.grid(row=1, column=0, columnspan=3, ipadx=70, pady=5)
        
        self.leftColor = tk.Frame(self.stats, bg="light blue", width=50, height=200)
        self.leftColor.grid(row=2, column=0, rowspan=5)
        
        self.rightColor = tk.Frame(self.stats, bg="light blue", width=50, height=200)
        self.rightColor.grid(row=2, column=2, rowspan=5)
        
        self.label_nbrpartie = ttk.Label(self.stats, text = f"Nombre de parties: {self.userStat.nombre_de_parties}", width=25)
        self.label_nbrpartie.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.createBarreInfo(self.label_nbrpartie, "Votre nombre de total de parties de sudoku réussies")
        
        self.label_tpsmoyen = ttk.Label(self.stats, text = f"Temps moyen: {self.userStat.temps_moyen}", width=25)
        self.label_tpsmoyen.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        self.createBarreInfo(self.label_tpsmoyen, "Votre temps moyen de résolution des sudoku, toutes difficultées confondues")
        
        try:
            self.label_meilleurtps = ttk.Label(self.stats, text = strftime("Meilleur temps: %Mmin %Ss", gmtime(self.userStat.meilleur_temps)), width=25)
        except:
            self.label_meilleurtps = ttk.Label(self.stats, text = "Meilleur temps: 00min 00s", width=25)
        self.label_meilleurtps.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        self.createBarreInfo(self.label_meilleurtps, "Votre meilleur temps acteul, toutes difficulées confondues")
        
        self.TpsTot = ttk.Label(self.stats, text = f"Temps total: {self.userStat.temps_total}", width=25)
        self.TpsTot.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        self.createBarreInfo(self.TpsTot, "Votre temps total de jeu")
        
        self.nbrParties = ttk.Label(self.stats, text = f"Classement: {self.userStat.classement}", width=25)
        self.nbrParties.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        self.createBarreInfo(self.nbrParties, "Votre classement actuel")
        
#%% Fenetre de jeu
    def fenetreJeu(self, event, difficulty):
        """
        Permet de créer la fenêtre de jeu et de récupérer une grille de sudoku de la classe sudoku

        Parameters
        ----------
        Event, Difficultée: int

        Returns
        -------
        None.

        """
        self.accueil.destroy()
        
        #Récupération du sudoku
        self.sudoku = Sudoku(self.variableDifficulty.get())
        
        #Création de la fenêtre
        self.fenetre_jeu = tk.Toplevel(self.racine)
        self.fenetre_jeu.resizable(False,False)
        self.fenetre_jeu.focus()
        
        #Création de la frame de sudoku
        self.grille = ttk.LabelFrame(self.fenetre_jeu, relief="sunken", padding = (20, 10), text = "Sudoku")
        self.grille.grid(row=0, column=0, padx=(20, 10), pady=(20, 20), rowspan=3)
        
        #Création du chronomètre
        self.frame_chronometre = ttk.LabelFrame(self.fenetre_jeu, text = "Chronomètre", width = 50)
        self.frame_chronometre.grid(row=0, column=1, padx=(30,10), pady=(30,10), ipadx=10, ipady=10, sticky=tk.N)
        
        self.timespan = 0
        self.temps = 0
        
        self.chrono = ttk.Label(self.frame_chronometre, font=("Helvetica", 20), text = "00:00")
        self.chrono.pack()
        self.updateChrono()
        
        #Création de la frame de stats
        self.game_stats = ttk.LabelFrame(self.fenetre_jeu, padding = (20, 10), text = "Statistiques", width = 50)
        self.game_stats.grid(row=1, column=1, padx=(30,10), pady=(30, 10), sticky = tk.N, ipadx=10, ipady=10)
        
        if self.connected:
            self.statId = tk.Label(self.game_stats, text = self.userStat.current_user)
            self.statId.grid(row=0, column=0, padx=5, sticky="nsew", pady=5)
            self.createBarreInfo(self.statId, "Votre nom d'utilisateur")
            
            try:
                self.statMeilleurTemps = tk.Label(self.game_stats, text = strftime("%Mmin %Ss", gmtime(self.userStat.meilleur_temps)))         #On évite l'erreur si le temps à afficher est l'infini (lors de la création d'un compte)
            except:
                self.statMeilleurTemps = tk.Label(self.game_stats, text = "00min 00s")
            
            self.statMeilleurTemps.grid(row=3, column=0, padx=5, sticky="nsew", pady=5)
            self.createBarreInfo(self.statMeilleurTemps, "Votre meilleur temps actuelle, lancez une nouvelle partie\n pour tenter de l'améliorer!")
            
            self.statPoints = tk.Label(self.game_stats, text =f"{int(self.userStat.points)} Points")
            self.statPoints.grid(row=1, column=0, padx=5, sticky="nsew", pady=5)
            self.createBarreInfo(self.statPoints, "Votre score, gagnez des points à chaque fois\n que vous finissez un sudoku!")
            
            if self.userStat.classement == 1:
                texte_classement = f"{self.userStat.classement}er"
            else:
                texte_classement = f"{self.userStat.classement}ème"
            
            self.statClassement = tk.Label(self.game_stats, text = texte_classement)
            self.statClassement.grid(row=2, column=0, padx=5, sticky="nsew", pady=5)
            self.createBarreInfo(self.statClassement, "Votre classement, mesurez vous aux meilleurs joueurs\n et tentez d'obtenir la meilleur position!")        
        else:
            self.messageNonConnecte = tk.Label(self.game_stats, text="Connectez-vous\n pour accéder\n à vos statistiques")
            self.messageNonConnecte.pack()

        #Création de la frame d'options
        self.game_options = ttk.LabelFrame(self.fenetre_jeu, padding = (0, 20), text = "Options")
        self.game_options.grid(row=2, column=1, padx=(30,10), pady=(30, 30), sticky=tk.S, ipadx=10, ipady=10)
        
        self.bouton_retour_accueil = ttk.Button(self.game_options, text = "Accueil", width = 15)
        self.bouton_retour_accueil.bind("<Button-1>", self.retourAccueil)
        self.bouton_retour_accueil.pack(side=tk.TOP)
        
        self.bouton_indice = ttk.Button(self.game_options, text="Indice", width = 15)
        self.bouton_indice.bind("<Button-1>", self.indice)
        self.bouton_indice.pack(side=tk.TOP)
        
        self.bouton_fin = ttk.Button(self.game_options, text="Valider la grille", width = 15)
        self.bouton_fin.bind("<Button-1>", self.verifierGrille)
        self.bouton_fin.pack(side=tk.TOP)
        
        #Création des cases du sudoku
        self.case = []
        
        for l in range(9):
            ligne = []
            for c in range(9):
                cell = tk.Entry(self.grille, width=2, font=("Helvetica", 20), relief="solid", justify= "center", validate = "key", validatecommand = (self.racine.register(self.validerCase), '%P'))
                cell.bind("<KeyRelease>", self.envoyerCase)
                cell.grid(row=l, column=c, padx=1, pady=1)
                ligne.append(cell)
            self.case.append(ligne)
            
        #Remplissage des cases
        self.remplirCases()
        
        
    def remplirCases(self):
        """
        Fais le lien entre la classe sudoku et affichage pour charger les différentes chiffres
        présents dans la grille.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        for ligne in range(9):
            for colonne in range(9):
                case_sudoku = self.sudoku.grid[ligne][colonne]
                case_affichage = self.case[ligne][colonne]
                if case_sudoku.valeur != 0:
                    case_affichage.insert(0,str(case_sudoku.valeur))
                    case_affichage["state"] = tk.DISABLED
                    case_affichage["bg"] = "light grey"
                    
    
    def validerCase(self, _input):
        """
        Méthode validate des entry des cases de sudoku, permet de vérifier
        si l'utilisateur a bien entré un chiffre entre 1 et 9.

        Parameters
        ----------
        Event

        Returns
        -------
        None.

        """
        authorisees = ["1","2","3","4","5","6","7","8","9",""]      #Liste des valeurs que l'on peut rentrer dans une case du sudoku ("" est utilisé pour pouvoir toujours utiliser les touches "Entrer" et "DEL")
        res = False
        
        if _input in authorisees:
            res = True
        
        if res == False:
            file=os.path.join("Data", "Sounds", "sounds", "Windows Background.wav")
            pygame.init()                                                             #Son d'erreur si autre chose qu'un chiffre est entré
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            
        return res
    
    def indexMartice(self, element, matrice):
        """
        Méthode permettant de renvoyer l'indice (ligne, colonne) d'une valeure dans
        une matrice 2D

        Parameters
        ----------
        Elément récherché dans la matrice, Matrice en question

        Returns
        -------
        None.

        """
        for index_l, ligne in enumerate(matrice):
            for index_c, valeur in enumerate(ligne):
                if valeur == element:
                    return (index_l, index_c)
    
    def envoyerCase(self, event):
        """
        Permet d'envoyer les informations à la classe Sudoku quand l'utilisateur modifie une
        case de la grille
        
        Parameters
        ----------
        Event

        Returns
        -------
        None.

        """
        self.fenetre_jeu.focus()         #Focus sur la fenêtre pour quitter le focus de la case
        
        case = event.widget
        
        if case.get():                  #Si la case est vide, on met la valeur à 0
            valeur = case.get()
        else:
            valeur = 0
            
        case.config(bg = "white")       #On remet le background blanc si jamais cette case était affichée avec une erreur
        
        #On met à jour notre grille dans la classe Sudoku
        ligne, colonne = self.indexMartice(case, self.case)
        case_sudoku = self.sudoku.grid[ligne][colonne]
        case_sudoku.valeur = int(valeur)
        
    def indice(self, event):
        """
        Permet d'ajouter un indice à la grille en cours en utilisant la méthode indice de la classe Sudoku
        
        Parameters
        ----------
        Event

        Returns
        -------
        None.

        """
        if not self.sudoku.grilleRemplie(self.sudoku.grid):
            self.userStat.indices += 1
            if not self.sudoku.erreurSudoku():
                ligne, colonne, valeur = self.sudoku.indice()
                case_affichage = self.case[ligne][colonne]
                
                case_affichage.insert(0,valeur)
                case_affichage["bg"] = "light grey"
                case_affichage["state"] = tk.DISABLED
                
                self.sudoku.grid[ligne][colonne].valeur = valeur    #On met à jour la grille de jeu en cours
            else:
               case_erreur = self.sudoku.erreurSudoku()
               self.case[case_erreur.ligne][case_erreur.colonne].config(bg = "salmon")
            
    def retourAccueil(self,event):
        """
        Affiche une messagebox demandant à l'utilisateur de confirmer qu'il veut bien quitter la
        partie
        
        Parameters
        ----------
        Event

        Returns
        -------
        None.

        """
        if messagebox.askokcancel("", "Etes-vous sur de vouloir quitter la partie ?\n(Votre progression ne sera pas sauvegardée)"):
            self.fenetre_jeu.destroy()
            self.fenetre_principale(self.racine)
            
    def verifierGrille(self,event):
        """
        Vérifie si il n'y a pas d'erreurs dans la grille et renvoi un message en fonction
        
        Parameters
        ----------
        Event

        Returns
        -------
        None.

        """
        if not self.sudoku.casesVide(self.sudoku.grid):
            if not self.sudoku.erreurSudoku():
                self.chrono.after_cancel(self.chrono_id)
                if self.terminerPartie():
                    return              #On return pour ne pas afficher le message d'erreur si la grille est valide
      
        tk.messagebox.showerror("", "La grille n'est pas valide, essayez d'utiliser le bouton indice.")
            
            
    def terminerPartie(self):
        """
        Permet de terminer une partie en récupérant toutes les informations et en 
        fermant et ouvrant les différentes fenêtres.
        
        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        print(self.connected)
        #Récupération des données
        temps = self.timespan-1             #-1 car le chrono met une seconde à s'arrêter (un tour dans la boucle avant de s'arrêter)
        points_partie = self.userStat.actualiser_data_user(temps, self.variableDifficulty.get())
        if not self.userStat.current_user:
            text = f"Bravo, vous avez réussi le sudoku!\nVous avez résolu le sudoku en {temps} secondes!"
        else:
            text = f"Bravo, vous avez réussi le sudoku!\nVous avez résolu le sudoku en {temps} secondes et gagné {int(points_partie)} points!"
        
        if tk.messagebox.showinfo("", text):
            self.fenetre_jeu.destroy()
            self.fenetre_principale(self.racine)
            return True
        
    def updateChrono(self):
        """
        Met en place le chrono dans la fenêtre de jeu
        
        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        self.time = datetime.fromtimestamp(self.timespan)
        self.affichageChrono = self.time.strftime("%M:%S")
        self.chrono.config(text = self.affichageChrono)
        self.chrono_id = self.chrono.after(1000,self.updateChrono)
        self.timespan += 1
        
    
                
app = Main()
app.racine.mainloop()