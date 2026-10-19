import pygame # importation de la librairie pygame
import Classe
import sys # pour fermer correctement l'application
from random import randint

# lancement des modules inclus dans pygame
pygame.init() 

# création d'une fenêtre de 900 par 600
screen = pygame.display.set_mode((900,600))
pygame.display.set_caption("Space Invaders") # titre de la fenêtre
# chargement de l'image de fond
fond = pygame.image.load('background.png')

liste_ennemis = []
mechant = Classe.Ennemi_1()
liste_ennemis.append(mechant)

horloge = pygame.time.Clock()

### BOUCLE DE JEU  ###
running = True # variable pour laisser la fenêtre ouverte


while running : # boucle infinie pour laisser la fenêtre ouverte
    # dessin du fond
    screen.blit(fond,(0,0))

    ### Gestion des événements  ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
            running = False # running est sur False
            sys.exit() # pour fermer correctement

    for mechant in liste_ennemis :
        mechant.deplacer()
        screen.blit(mechant.image, (mechant.position, mechant.hauteur))




    pygame.display.update()
    horloge.tick(60)
