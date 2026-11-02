import pygame # importation de la librairie pygame
import Classe
import sys # pour fermer correctement l'application
from random import randint
import math # atan2 et degrees : calcul de l'angle de visee de la tour

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

# creation de la tour posee sur la carte
la_tour = Classe.Tour()

liste_balles = []  # lasers en vol
compteur = 0  # images ecoulees depuis le dernier tir

horloge = pygame.time.Clock()

### BOUCLE DE JEU  ###
running = True # variable pour laisser la fenêtre ouverte


while running : # boucle infinie pour laisser la fenêtre ouverte
    # dessin du fond
    screen.blit(fond,(0,0))

    # visee : fleche du centre de la tour vers le centre de l'ennemi (-8 = 32 - 24)
    dx, dy = mechant.position - la_tour.position - 8, mechant.hauteur - la_tour.hauteur - 8
    # angle en degres ; -90 car les canons de tour.png pointent vers le haut
    angle = -math.degrees(math.atan2(dy, dx)) - 90
    img = pygame.transform.rotate(la_tour.image, angle)
    # recentrage obligatoire : rotate() agrandit l'image, +32 = demi-taille de la tour
    screen.blit(img, img.get_rect(center=(la_tour.position + 32, la_tour.hauteur + 32)))

    # tir continu : un laser toutes les la_tour.cadence images, vers l'ennemi
    compteur += 1
    if compteur >= la_tour.cadence :
        compteur = 0
        liste_balles.append(Classe.Balle(la_tour.position + 32, la_tour.hauteur + 32, dx, dy))


    ### Gestion des événements  ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
            running = False # running est sur False
            sys.exit() # pour fermer correctement

    for mechant in liste_ennemis :
        mechant.deplacer()
        screen.blit(mechant.image, (mechant.position, mechant.hauteur))

    # deplacement et dessin des lasers
    for balle in liste_balles :
        balle.deplacer()
        img = pygame.transform.rotate(balle.image, balle.angle)
        screen.blit(img, img.get_rect(center=(balle.position, balle.hauteur)))
        if balle.position < 0 or balle.position > 900 or balle.hauteur < 0 or balle.hauteur > 600 :
            liste_balles.remove(balle) # suppression de la balle si elle sort de l'écran




    pygame.display.update()
    horloge.tick(60)
