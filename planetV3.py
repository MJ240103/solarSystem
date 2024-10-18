import math
import pygame

class Planet:
    def __init__(self, nom, masse, rayon, position, vitesse, acceleration, couleur):
        self.nom = nom
        self.masse = masse
        self.rayon = rayon
        self.position = position  # (x, y)
        self.vitesse = vitesse  # (vx, vy)
        self.acceleration = acceleration  # (ax, ay)
        self.couleur = couleur

    def setPosition(self, dt):
        """Met à jour la position de la planète en fonction de sa vitesse et de l'intervalle de temps."""
        self.vitesse[0] += self.acceleration[0] * dt
        self.vitesse[1] += self.acceleration[1] * dt
        self.position[0] += self.vitesse[0] * dt
        self.position[1] += self.vitesse[1] * dt

    def applyGravity(self, masse_soleil, position_soleil, G):
        """Met à jour l'accélération de la planète en fonction de la gravité exercée par le Soleil."""
        dx = position_soleil[0] - self.position[0]
        dy = position_soleil[1] - self.position[1]
        distance = math.sqrt(dx**2 + dy**2)
        force = G * masse_soleil * self.masse / distance**2
        theta = math.atan2(dy, dx)
        self.acceleration[0] = math.cos(theta) * force / self.masse
        self.acceleration[1] = math.sin(theta) * force / self.masse

    def selfDraw(self, window, echelle_distance, echelle_rayon, centrage, SCREEN_WIDTH, SCREEN_HEIGHT, convertFun):
        """Affiche une planète dans la fenêtre Pygame."""

        
        rayon = convertFun(self.rayon, self.rayon)[0]/(echelle_rayon)
        print(rayon, echelle_rayon)
        x_affiche,y_affiche = convertFun(centrage[0] + self.position[0], centrage[1] + self.position[1])
        x_affiche,y_affiche = centrage[0] + x_affiche, centrage[1] + y_affiche
        
        #print(x_affiche,y_affiche, centrage)
        #realToDisplay(x,y,1000,1000,1e13,1e13)
        
        # Ne dessiner que si la planète est dans la fenêtre
        pygame.draw.circle(window, self.couleur, (x_affiche, y_affiche), rayon)