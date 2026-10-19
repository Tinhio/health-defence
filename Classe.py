import pygame  # necessaire pour charger les images et les sons
from random import randint 

class Ennemi_1() : # classe pour créer les ennemis
    def __init__(self) :
        self.image = pygame.image.load('ennemi_1.png') 
        self.position = -100 
        self.hauteur = 300
        self.vivant = True

    def deplacer(self):
        if self.position < 120:
            self.position += 1
        elif self.position <= 120 and self.hauteur > 120:
            self.hauteur -= 1
        elif self.position < 300 and self.hauteur <= 120:
            self.position += 1
        elif self.position <= 300 and self.hauteur < 360:
            self.hauteur += 1
        elif self.position < 540 and self.hauteur <= 360:
            self.position += 1
        elif self.position <= 540 and self.hauteur > 240:
            self.hauteur -= 1
        elif self.position < 900 and self.hauteur <= 240:
            self.position += 1

        
        