import math  # hypot et atan2 : direction et angle des lasers
import pygame  # necessaire pour charger les images et les sons
from random import randint 


coordonnees = [
    (-100, 303),    # entree, a gauche
    (126, 303),  # premier virage
    (126, 125),  # montee
    (305, 125),  # haut du S
    (305, 363),  # bas du S
    (546, 363),  # virage du bas
    (546, 245),  # haut de la remontee
    (900, 245),  # sortie a droite
]

class Ennemi_1() : # classe pour créer les ennemis
    def __init__(self) :
        self.image = pygame.image.load('ennemi_1.png') 
        self.position = coordonnees[0][0]  # position horizontale initiale
        self.hauteur = coordonnees[0][1]   # position verticale initiale
        self.etape = 1  # étape actuelle du parcours
        self.vitesse = 5  # pixels parcourus à chaque image
        self.vivant = True

    def deplacer(self):
        if self.etape >= len(coordonnees):  # arrivé au bout du chemin
            return
        cible_x, cible_y = coordonnees[self.etape]
        if self.position < cible_x:
            self.position += min(self.vitesse, cible_x - self.position)
        elif self.position > cible_x:
            self.position -= min(self.vitesse, self.position - cible_x)
        elif self.hauteur < cible_y:
            self.hauteur += min(self.vitesse, cible_y - self.hauteur)
        elif self.hauteur > cible_y:
            self.hauteur -= min(self.vitesse, self.hauteur - cible_y)
        else:
            self.etape += 1  # point atteint, on vise le suivant


class Tour ():
    def __init__(self):
        self.image = pygame.image.load('tour.png')
        self.position = 400
        self.hauteur = 200
        self.cadence = 1000  # nombre d'images entre deux tirs

class Balle ():  # un laser tire par la tour
    def __init__(self, x, y, dx, dy):
        self.image = pygame.image.load('laser.png')
        self.vitesse = 40  # pixels parcourus a chaque image
        distance = math.hypot(dx, dy) or 1  # or 1 : evite la division par zero
        self.dx = dx / distance * self.vitesse  # deplacement par image
        self.dy = dy / distance * self.vitesse
        self.angle = -math.degrees(math.atan2(dy, dx)) - 90  # -90 : le laser pointe vers le haut
        self.position = x  # centre de la balle
        self.hauteur = y

    def deplacer(self):
        self.position += self.dx
        self.hauteur += self.dy
