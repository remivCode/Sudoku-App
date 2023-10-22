Sudoku Project Version 1.0 21/05/2023

USAGE GENERAL
--------------
- Lancer le fichier Affichage.py pour lancer l'application
- Ne pas déplacer ou renommer les dossiers et fichiers du projet
- La navigation sur l'application se fait via les différents boutons
- Pour fermer définitivement l'application, cliquer sur le bouton "Quitter l'application" de la fenêtre d'accueil
- Il peut y avoir un certain temps de chargement de la grille lorsque vous lancez une partie en difficultée 3

PROCESSUS D'INSTALLATION
-------------------------
- Une fois dé-zippé, le dossier devrait contenir 4 fichiers python: Affichage.py, Sudoku.py, Case.py et User.py et trois dossier:
	- Data, contenant trois dossier Images, Sounds et Users
	- _pycache_ 
	- Rendu, contenant trois pdf et une vidéo: L'explication détaillée de notre méthode de création de sudoku et les versions actualisées de notre cahier des charges et de notre découpage fontionnel ainsi que notre vidéo de présentation
- Pour le fonctionnement du programme, dans votre terminal python:
	- pip install ttkwidgets
	- pip install pygame

ERREUR AU DEMARRAGE
--------------------
- Lorsque vous lancez l'application, il est possible que python affiche un message d'erreur: "TclError: image ‘pyimageXX’ doesn’t exist" indiquant qu'il n'arrive pas à lire les images du programme. Il suffit de redémarrer le kernel pour résoudre ce problème 
- Si une erreur de type "bgerror" survient, elle n'est pas bloquante quant au bon fonctionnement du programme mais il faut redémarrer votre éditeur python pour résoudre ce problème. (Cette erreur arrive lorsque les fenêtres sont fermées autrement que par les boutons de l'application)

AUTEURS
--------
- BURGY CORENTIN
- DELAUNE-LORIETTE MATHEO
- PEREIRA RAPHAEL
- VIALLETON REMI