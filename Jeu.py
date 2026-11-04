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

# coeur a defendre : pose au bout du chemin, juste avant la sortie
coeur = pygame.image.load('coeur.png')
fin_x, fin_y = Classe.coordonnees[-1]  # dernier point du parcours
coeur_rect = coeur.get_rect(center=(fin_x - 70, fin_y + 24))  # centre sur la piste

# petites coeurs de vie : memes proportions que coeur.png, en haut a droite
coeur_redimention = pygame.transform.scale(coeur, (24, 20))
vie_x, vie_y = 700, 50  # centre du premier coeur
coeur_vie = coeur_redimention.get_rect(center=(vie_x, vie_y))  # gabarit fixe : on le deplace sans le modifier

liste_balles = []  # lasers en vol
compteur = 0  # images ecoulees depuis le dernier tir

compteur_apparition = 0

angle = 0  # orientation de la tour (0 = droite quand il n'y a plus d'ennemi)

vie = 3

police = pygame.font.SysFont("Arial", 64)
game_over = False

horloge = pygame.time.Clock()

### BOUCLE DE JEU  ###
running = True # variable pour laisser la fenêtre ouverte


while running : # boucle infinie pour laisser la fenêtre ouverte
    # dessin du fond
    screen.blit(fond,(0,0))

    # le coeur est dessine avant les ennemis pour qu'ils passent devant
    screen.blit(coeur, coeur_rect)

    # un coeur par vie restante
    for i in range(3) :
        if i < vie :
            screen.blit(coeur_redimention, (vie_x + i * 32, vie_y))

    # visee : sur le premier ennemi de la liste (le plus avance)
    if liste_ennemis :
        cible = liste_ennemis[0]
        dx, dy = cible.position - la_tour.position - 8, cible.hauteur - la_tour.hauteur - 8
        # angle en degres ; -90 car les canons de tour.png pointent vers le haut
        angle = -math.degrees(math.atan2(dy, dx)) - 90

    img = pygame.transform.rotate(la_tour.image, angle)
    # recentrage obligatoire : rotate() agrandit l'image, +32 = demi-taille de la tour
    screen.blit(img, img.get_rect(center=(la_tour.position + 32, la_tour.hauteur + 32)))

    # tir continu : un laser toutes les la_tour.cadence images, vers l'ennemi
    if liste_ennemis : # plus d'ennemi a l'ecran : la tour ne tire pas
        compteur += 1
        if compteur >= la_tour.cadence :
            compteur = 0
            liste_balles.append(Classe.Balle(la_tour.position + 32, la_tour.hauteur + 32, dx, dy))

    ### Gestion des événements  ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
            running = False # running est sur False
            sys.exit() # pour fermer correctement

    #recommence une partie, seulement si la precedente est perdue
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over :
            liste_ennemis.clear()
            liste_balles.clear()
            vie = 3
            game_over = False
            compteur = 0
            compteur_apparition = 0
            angle = 0
            mechant = Classe.Ennemi_1()
            liste_ennemis.append(mechant)

    # apparition d'un nouvel ennemi toutes les 90 images
    compteur_apparition += 1
    if compteur_apparition >= 90 :
        compteur_apparition = 0
        liste_ennemis.append(Classe.Ennemi_1())

    for mechant in liste_ennemis[:] :  # copie : on retire des ennemis pendant le parcours
        mechant.deplacer()
        screen.blit(mechant.image, (mechant.position, mechant.hauteur))
        # contact avec le coeur : l'ennemi est detruit et fait perdre une vie
        if coeur_rect.colliderect(mechant.image.get_rect(topleft=(int(mechant.position), int(mechant.hauteur)))) :
            liste_ennemis.remove(mechant) # suppression de l'ennemi qui touche le coeur
            vie -= 1
    
    if vie <= 0 :
        game_over = True

    # deplacement et dessin des lasers
    for balle in liste_balles :
        balle.deplacer()
        img = pygame.transform.rotate(balle.image, balle.angle)
        screen.blit(img, img.get_rect(center=(balle.position, balle.hauteur)))
        if balle.position < 0 or balle.position > 900 or balle.hauteur < 0 or balle.hauteur > 600 :
            liste_balles.remove(balle) # suppression de la balle si elle sort de l'écran
        
        elif liste_ennemis and balle.position < liste_ennemis[0].position + 64 and balle.position > liste_ennemis[0].position - 64 and balle.hauteur < liste_ennemis[0].hauteur + 64 and balle.hauteur > liste_ennemis[0].hauteur - 64 :
            liste_balles.remove(balle) # suppression de la balle si elle touche l'ennemi
            liste_ennemis.remove(liste_ennemis[0]) # suppression du premier ennemi si il est touché

    if game_over == True :
        screen.fill((30,30,30))
        texte = police.render("GAME OVER", True, (255, 0, 0))
        screen.blit(texte, texte.get_rect(center=(450, 300)))  # centré dans la fenêtre 900x600
        texte = police.render("Appuie sur R pour recommencer", True, (255, 0, 0))
        screen.blit(texte, texte.get_rect(center=(450, 450)))
        pygame.display.update()
        horloge.tick(60)

    pygame.display.update()
    horloge.tick(60)
