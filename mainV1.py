import pygame, sys
import math
from pygame.locals import QUIT

# Initialisation de Pygame
pygame.init()

# Définition des constantes du programme
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 50)
BLUE = (50, 50, 255)
RED = (255, 50, 50)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulation de l'Orbite Planétaire")

# Constantes astronomiques
masseSoleil = 1.989e30
rayonSoleil = 6.955e8
rayonPlanete = 6.2e6
G = 6.67384e-11
masseTerre = 5.972e24

# Distance au Soleil et vitesse initiale de la planète
d0 = 149.5e9  # distance initiale en m
v0 = 29.8e3   # vitesse initiale en m/s

# Intervalle de temps (en secondes)
dt = 7.2e4  # correspond à environ 1 jour

# Échelles pour l'affichage
echelleDistances = SCREEN_HEIGHT * 2.0e-12
echelleRayonSoleil = SCREEN_HEIGHT * 3.0e-11
echelleRayonsPlanete = SCREEN_HEIGHT * 1.0e-9

# Rayons mis à l'échelle
R = rayonSoleil * echelleRayonSoleil
r_planete = rayonPlanete * echelleRayonsPlanete

# Position initiale de la planète sur l'axe x
x = d0
y = 0

# Vitesse initiale de la planète sur l'axe y
vx = 0
vy = v0

# Fonction pour calculer la force gravitationnelle
def calcule_force_gravitationnelle(masse_planete, pos_planete):
    # - car force attractive
    dx = -pos_planete[0]  # distance entre la planète et le Soleil sur l'axe x
    dy = -pos_planete[1]  # distance sur l'axe y
    distance = math.sqrt(dx**2 + dy**2)
    
    # Loi de la gravitation de Newton
    force = G * masseSoleil * masse_planete / distance**2
    theta = math.atan2(dy, dx)
    
    fx = math.cos(theta) * force
    fy = math.sin(theta) * force
    return fx, fy

# Boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False  # Termine la boucle principale

    # Calcul de la force gravitationnelle
    fx, fy = calcule_force_gravitationnelle(masseTerre, (x, y))

    # Mise à jour de la vitesse de la planète (intégration de la force)
    ax = fx / masseTerre  # accélération axiale
    ay = fy / masseTerre  # accélération sur y
    vx += ax * dt
    vy += ay * dt

    # Mise à jour de la position de la planète
    x += vx * dt
    y += vy * dt

    # Mettre le fond en noir
    window.fill(BLACK)

    # Création Soleil
    pygame.draw.circle(window, YELLOW, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), int(R))

    # Mise à l'échelle de la position de la planète pour l'affichage
    x_affiche = SCREEN_WIDTH // 2 + int(x * echelleDistances)
    y_affiche = SCREEN_HEIGHT // 2 + int(y * echelleDistances)



    # Dessiner la Terre
    pygame.draw.circle(window, BLUE, (x_affiche, y_affiche), int(r_planete))

    # Mettre à jour l'affichage
    pygame.display.update()

    # Vitesse d'exécution
    pygame.time.delay(30)

# Fermeture de PyGame à la fin de l'execution
pygame.quit()
sys.exit()