import math
import pygame
import copy

class Planet:
    def __init__(self, nom, masse, rayon, position, vitesse, acceleration, couleur):
        self.nom = nom
        self.masse = masse
        self.rayon = rayon
        self.position = position  # (x, y)
        self.vitesse = vitesse  # (vx, vy)
        self.acceleration = acceleration  # (ax, ay)
        self.couleur = couleur

    def gravite(self, autres_planetes, G):
        """Calcule l'accélération en fonction des autres planètes et du Soleil."""
        ax, ay = 0, 0
        #print("GRAVITE")
        for autre_planete in autres_planetes:
            if autre_planete != self:
                dx = autre_planete.position[0] - self.position[0]
                dy = autre_planete.position[1] - self.position[1]
                if dx > 1e140: print(dx, dy)
                distance = math.sqrt(dx**2 + dy**2)
                if dx > 1e140: print(distance)
                force = -G * autre_planete.masse / distance**2
                ax += force * (dx / distance)
                ay += force * (dy / distance)
        return ax, ay
        
    def selfVanish(self, solarSystem, position_soleil, rayon_soleil):
        """Supprime la planète si elle est recouverte par le Soleil."""
        dx = self.position[0] - position_soleil[0]
        dy = self.position[1] - position_soleil[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < (self.rayon + rayon_soleil):
            solarSystem.remove(self)

    def selfDraw(self, window, ECHELLE_RAYON, centrage, SCREEN_WIDTH, SCREEN_HEIGHT, convertFun):
        """Affiche une planète dans la fenêtre Pygame."""

        rayon = convertFun(self.rayon, self.rayon)[0] * ECHELLE_RAYON
        x_affiche,y_affiche = convertFun(centrage[0] + self.position[0], centrage[1] + self.position[1])
        #x_affiche,y_affiche = centrage[0] + x_affiche, centrage[1] + y_affiche
        
        #print(self.nom,self.position[0], centrage[0], self.position[0]+centrage[0])
        #realToDisplay(x,y,1000,1000,1e13,1e13)
        
        # Ne dessiner que si la planète est dans la fenêtre
        pygame.draw.circle(window, self.couleur, (x_affiche, y_affiche), rayon)


def runge_kutta(planetes, G, dt):
    k1v = []
    k1x = []
    k2v = []
    k2x = []
    k3v = []
    k3x = []
    k4v = []
    k4x = []
    acc = {}

    #Etape 1
    for planete in planetes: acc[planete] = planete.gravite(planetes, G)
    clone_planetes = [copy.copy(p) for p in planetes]
    for planete in planetes:
        k1v.append(acc[planete])
        k1x.append(planete.vitesse)

    #Etape 2
    for i, planete in enumerate(planetes):
        clone_planetes[i].vitesse[0] += k1v[i][0] * dt / 2
        clone_planetes[i].vitesse[1] += k1v[i][1] * dt / 2
        clone_planetes[i].position[0] += k1x[i][0] * dt / 2
        clone_planetes[i].position[1] += k1x[i][1] * dt / 2

        acc[planete] = planete.gravite(planetes, G)
        k2v.append(acc[planete])
        k2x.append(clone_planetes[i].vitesse)

    # Etape 3
    for i, planete in enumerate(planetes):
        clone_planetes[i].vitesse[0] += k2v[i][0] * dt / 2
        clone_planetes[i].vitesse[1] += k2v[i][1] * dt / 2
        clone_planetes[i].position[0] += k2x[i][0] * dt / 2
        clone_planetes[i].position[1] += k2x[i][1] * dt / 2

        acc[planete] = planete.gravite(planetes, G)
        k3v.append(acc[planete])
        k3x.append(clone_planetes[i].vitesse)

    # Etape 4
    for i, planete in enumerate(planetes):
        clone_planetes[i].vitesse[0] += k3v[i][0] * dt / 2
        clone_planetes[i].vitesse[1] += k3v[i][1] * dt / 2
        clone_planetes[i].position[0] += k3x[i][0] * dt / 2
        clone_planetes[i].position[1] += k3x[i][1] * dt / 2

        acc[planete] = planete.gravite(planetes, G)
        k4v.append(acc[planete])
        k4x.append(clone_planetes[i].vitesse)

    
    for i, planete in enumerate(planetes):
        planete.vitesse[0] += ((k1v[i][0] + 2 * k2v[i][0] + 2 * k3v[i][0] + k4v[i][0]) * dt / 6)
        planete.vitesse[1] += ((k1v[i][1] + 2 * k2v[i][1] + 2 * k3v[i][1] + k4v[i][1]) * dt / 6)
        planete.position[0] += ((k1x[i][0] + 2 * k2x[i][0] + 2 * k3x[i][0] + k4x[i][0]) * dt / 6)
        planete.position[1] += ((k1x[i][1] + 2 * k2x[i][1] + 2 * k3x[i][1] + k4x[i][1]) * dt / 6)
