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
        self.image = pygame.image.load('Image/ennemi_1.png') 
        self.position = coordonnees[0][0]  # position horizontale initiale
        self.hauteur = coordonnees[0][1]   # position verticale initiale
        self.etape = 1  # étape actuelle du parcours
        self.vitesse = 2  # pixels parcourus à chaque image
        self.vivant = True
        self.vie = 5

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

    def prendre_degats(self, degats):
        self.vie -= degats
        if self.vie <= 0:
            self.vivant = False


Types_tours = {
    'tour_de_base': {'cadence': 75,  'portee': 200, 'degats': 2, 'prix': 20, 'image': 'Image/tour.png'},
    'tour_rapide': {'cadence': 30,  'portee': 150, 'degats': 1, 'prix': 30, 'image': 'Image/tour_rapide.png'},
    'tour_sniper': {'cadence': 120,  'portee': 250, 'degats': 5, 'prix': 50, 'image': 'Image/tour_sniper.png'},
}

class Tour ():
    def __init__(self, type_tour):
        infos = Types_tours[type_tour]
        self.image = pygame.image.load(infos['image'])
        self.position = 400
        self.hauteur = 200
        self.cadence = infos['cadence']  # nombre d'images entre deux tirs
        self.portee = infos['portee']  # distance maximale de tir
        self.degats = infos['degats']  # dégâts infligés par le tir
        self.prix = infos['prix']  # prix de la tour
        self.prix_amelioration = (self.prix * 3)//2 - 20  # prix de l'amélioration de la tour


class Balle ():  # un laser tire par la tour
    def __init__(self, x, y, dx, dy, degats):
        self.image = pygame.image.load('Image/laser.png')
        self.vitesse = 40  # pixels parcourus a chaque image
        distance = math.hypot(dx, dy) or 1  # or 1 : evite la division par zero
        self.dx = dx / distance * self.vitesse  # deplacement par image
        self.dy = dy / distance * self.vitesse
        self.angle = -math.degrees(math.atan2(dy, dx)) - 90  # -90 : le laser pointe vers le haut
        self.position = x  # centre de la balle
        self.hauteur = y
        self.degats = degats  # dégâts infligés par le laser

    def deplacer(self):
        self.position += self.dx
        self.hauteur += self.dy
