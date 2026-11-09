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
fond = pygame.image.load('Image/background.png')

liste_ennemis = [] # ennemis a l'ecran ; le premier de la liste est le plus avance
mechant = Classe.Ennemi_1() # premier ennemi de la partie
liste_ennemis.append(mechant)

# creation de la tour posee sur la carte
la_tour = Classe.Tour('tour_de_base') 
# coeur a defendre : pose au bout du chemin, juste avant la sortie
coeur = pygame.image.load('Image/coeur.png')
fin_x, fin_y = Classe.coordonnees[-1]  # dernier point du parcours
coeur_rect = coeur.get_rect(center=(fin_x - 70, fin_y + 24))  # centre sur la piste

# petits coeurs de vie : memes proportions que coeur.png
coeur_redimention = pygame.transform.scale(coeur, (24, 20))

liste_balles = []  # lasers en vol
compteur = 0  # images ecoulees depuis le dernier tir

liste_tours = [la_tour]

compteur_apparition = 0 # images ecoulees depuis le dernier ennemi cree

angle = 0  # orientation de la tour (0 = droite quand il n'y a plus d'ennemi)

vie = 3 # vies restantes : autant de coeurs affiches en haut

score = 0 # points gagnes

piece = 20 # argent de depart : de quoi payer une tour de base (20 pieces)

# piece de monnaie affichee apres le texte Argent (pygame ne lit pas le .avif : version png)
# minuscules obligatoires : 'piece.png' existe vraiment sous ce nom
piece_image = pygame.transform.scale(pygame.image.load('Image/piece.png'), (32, 32))

# police pixel art style arcade (Police Press Start 2P, dossier Font/)
chemin_police = 'Font/PressStart2P-Regular.ttf'
police_gameOver = pygame.font.Font(chemin_police, 48)
police_message = pygame.font.Font(chemin_police, 16)
police_score = pygame.font.Font(chemin_police, 16)
game_over = False




horloge = pygame.time.Clock() # sert a limiter le jeu a 60 images par seconde

### BOUCLE DE JEU  ###
running = True # variable pour laisser la fenêtre ouverte


while running : # boucle infinie pour laisser la fenêtre ouverte
    ### Gestion des événements  ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
            running = False # running est sur False
            sys.exit() # pour fermer correctement

    # recommence une partie, seulement si la precedente est perdue
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over :
            liste_ennemis.clear()
            liste_balles.clear()
            la_tour = Classe.Tour('tour_de_base')
            liste_tours = [la_tour]
            vie = 3
            game_over = False
            compteur = 0
            compteur_apparition = 0
            angle = 0
            mechant = Classe.Ennemi_1()
            liste_ennemis.append(mechant)
            score = 0
            piece = 20 # l'argent repart au montant de depart
            prix = 10 # le prix de l'amelioration repart de zero

    # partie perdue : on affiche l'ecran de fin et on arrete la simulation
    if game_over :
        screen.fill((30,30,30))
        texte = police_gameOver.render("GAME OVER", True, (255, 0, 0))
        screen.blit(texte, texte.get_rect(center=(450, 300)))  # centré dans la fenêtre 900x600
        texte = police_message.render(f"Score : {score}", True, (255, 0, 0))
        screen.blit(texte, texte.get_rect(center=(450, 400)))
        texte = police_message.render("Appuie sur R pour recommencer", True, (255, 0, 0))
        screen.blit(texte, texte.get_rect(center=(450, 450)))
        pygame.display.update()
        horloge.tick(60)
        continue  # on repart au debut de la boucle : rien n'avance pendant le game over

    # dessin du fond
    screen.blit(fond,(0,0))

    # infos du joueur alignees a gauche sur x=640 : coeurs, score, argent
    for i in range(vie) :  # un coeur par vie restante
        screen.blit(coeur_redimention, (640 + i * 30, 43))
    # texte Argent suivi de l'image de la piece
    texte = police_score.render(f'Score :{score}', True, (0, 0, 0))
    screen.blit(texte, (640, 75))
    texte = police_score.render(f'Argent :{piece}', True, (0, 0, 0))
    screen.blit(texte, (640, 105))
    screen.blit(piece_image, (640 + texte.get_width() + 2, 96)) # la piece vient juste apres le texte

    x_mouse , y_mouse = pygame.mouse.get_pos()
    if x_mouse < la_tour.position + 64 and x_mouse > la_tour.position and y_mouse < la_tour.hauteur + 64 and y_mouse > la_tour.hauteur :
        texte = police_score.render(f"{la_tour.prix_amelioration}", True, (0, 0, 0))
        screen.blit(texte, (la_tour.position, la_tour.hauteur - 20))
        screen.blit(piece_image, (la_tour.position + texte.get_width() + 2, la_tour.hauteur - 28)) # la piece vient juste apres le texte
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and piece >= la_tour.prix_amelioration :
            la_tour.cadence -= 2 # cadence de tir plus rapide si on clique sur la tour
            piece -= la_tour.prix_amelioration # chaque clic coute 10 pieces
            la_tour.prix_amelioration = (la_tour.prix_amelioration * 3)//2 # le prix de l'amelioration double a chaque fois

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3  :
        img = pygame.transform.rotate(la_tour.image, angle)
        # recentrage obligatoire : rotate() agrandit l'image, +32 = demi-taille de la tour
        screen.blit(img, img.get_rect(center=(la_tour.position + 32, la_tour.hauteur + 32)))



    # le coeur est dessine avant les ennemis pour qu'ils passent devant
    screen.blit(coeur, coeur_rect)

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
    for x in liste_tours :
        if liste_ennemis : # plus d'ennemi a l'ecran : la tour ne tire pas
            compteur += 1
            if compteur >= x.cadence :
                compteur = 0
                liste_balles.append(Classe.Balle(x.position + 32, x.hauteur + 32, dx, dy,x.degats)) # le laser part du centre de la tour, vers l'ennemi

    # apparition d'un nouvel ennemi toutes les INTERVALLE_APPARITION images
    compteur_apparition += 1
    if compteur_apparition >= 180 :
        compteur_apparition = 0
        liste_ennemis.append(Classe.Ennemi_1())

    for mechant in liste_ennemis[:] :  # copie : on retire des ennemis pendant le parcours
        mechant.deplacer()
        screen.blit(mechant.image, (mechant.position, mechant.hauteur))
        # contact avec le coeur : l'ennemi est detruit et fait perdre une vie
        if mechant.position > 780 :
            liste_ennemis.remove(mechant) # suppression de l'ennemi qui touche le coeur
            vie -= 1
    
    if vie <= 0 : # plus de coeur : la partie est perdue
        game_over = True

    # deplacement et dessin des lasers
    for balle in liste_balles[:] : # copie : on retire des balles pendant le parcours
        balle.deplacer()
        img = pygame.transform.rotate(balle.image, balle.angle)
        screen.blit(img, img.get_rect(center=(balle.position, balle.hauteur)))
        if balle.position < 0 or balle.position > 900 or balle.hauteur < 0 or balle.hauteur > 600 :
            liste_balles.remove(balle) # suppression de la balle si elle sort de l'écran
        
        elif liste_ennemis and balle.position < liste_ennemis[0].position + 64 and balle.position > liste_ennemis[0].position - 64 and balle.hauteur < liste_ennemis[0].hauteur + 64 and balle.hauteur > liste_ennemis[0].hauteur - 64 :
            liste_ennemis[0].prendre_degats(balle.degats) # l'ennemi prend les degats de la balle
            if liste_ennemis[0].vivant == False : # si l'ennemi est mort
                liste_ennemis.remove(liste_ennemis[0]) # suppression du premier ennemi si il est touché
                score += 120 # gain par ennemi detruit
                piece += 6 # pieces gagnees par ennemi detruit
            liste_balles.remove(balle) # suppression de la balle si elle touche l'ennemi



        

    pygame.display.update() # affiche tout ce qui vient d'etre dessine
    horloge.tick(60) # 60 images par seconde au maximum
