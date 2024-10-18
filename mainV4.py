import pygame
import sys
from bodies import Planet
from bodies import runge_kutta
from collections import defaultdict

# Initialisation de Pygame
pygame.init()

# Définition des constantes du programme
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 50)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
ORANGE = (255, 165, 50)
PURPLE = (148, 0, 211)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gravity simulation (SPACE: show orbits, '
                           'keypad +/- : zoom in/out)')

# Mire qui indique le centre de la fenêtre d'affichage et qui permet d'observer le mouvement du Soleil
# Couleur de la croix
CROSS_COLOR = (0, 0, 0)  # Blanc

# Position du centre de la fenêtre
center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2

# Longueur des bras de la croix
cross_length = 10

# Dessiner la croix
def draw_centered_cross(window, center_x, center_y, cross_length, color):
    # Ligne horizontale
    pygame.draw.line(window, color, (center_x - cross_length, center_y), (center_x + cross_length, center_y), 2)
    # Ligne verticale
    pygame.draw.line(window, color, (center_x, center_y - cross_length), (center_x, center_y + cross_length), 2)


# Constantes astronomiques
masseSoleil = 1.989e30
rayonSoleil = 6.955e8
G = 6.67384e-11

# Intervalle de temps (en secondes)
dt = 7.2e4  # correspond à environ 1 jour (86400 secondes approximées à moins car simulation trop lente sinon)

# Échelles pour l'affichage
echelleDistances = SCREEN_HEIGHT * 2.0e-12 # défaut
echelleRayonSoleil = SCREEN_HEIGHT * 3.0e-11 # défaut
echelleRayonsPlanete = SCREEN_HEIGHT * 1.0e-6 # défaut

facteurDistance = 5.0e11  # Facteur d'échelle des distances
facteurRayon = 1.0e8  # Facteur d'échelle des rayons

# Création du Soleil et des planètes fictives
solarSystem = []

# Soleil (pas besoin de le bouger, donc on n'utilise pas Planet pour lui)
sun_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

def realToDisplay(x,y,window_x,window_y,space_x,space_y):
    x = x*window_x/space_x
    y = y*window_y/space_y
    return x,y

# Création des planètes
# Mercure
mercure = Planet(
    nom="Mercure",
    masse=3.3011e23,  # Masse de Mercure en kg
    rayon=(2.4397e6),  # Rayon de Mercure en mètres
    position=[(57.9e9), 0],  # Distance au Soleil en m sur l'axe x
    vitesse=[-0.5e3, 47.87e3],  # Vitesse en m/s (sur l'axe y)
    acceleration=[0, 0],  # Accélération initiale
    couleur=WHITE
)
solarSystem.append(mercure)

# Vénus
venus = Planet(
    nom="Vénus",
    masse=4.8675e24,  # Masse de Vénus en kg
    rayon=6.0518e6,  # Rayon de Vénus en mètres
    position=[108.2e9, 0],  # Distance au Soleil en m sur l'axe x
    vitesse=[-0.3e3, 35.02e3],  # Vitesse en m/s (sur l'axe y)
    acceleration=[0, 0],  # Accélération initiale
    couleur=PURPLE
)
solarSystem.append(venus)

# Terre
terre = Planet(
    nom="Terre",
    masse=5.972e24,  # Masse de la Terre en kg
    rayon=6.371e6,  # Rayon de la Terre en mètres
    position=[149.5e9, 0],  # Distance au Soleil en m sur l'axe x
    vitesse=[-0.2e3, 29.8e3],  # Vitesse en m/s (sur l'axe y)
    acceleration=[0, 0],  # Accélération initiale
    couleur=BLUE
)
solarSystem.append(terre)

# Mars
mars = Planet(
    nom="Mars",
    masse=6.4171e23,  # Masse de Mars
    rayon=3.39e6,  # Rayon de Mars
    position=[227.9e9, 0],  # Distance au Soleil (sur l'axe x)
    vitesse=[-0.15e3, 24.077e3],  # Vitesse tangentielle sur l'axe y
    acceleration=[0, 0],  # Accélération initiale
    couleur=RED
)

# Jupiter
jupiter = Planet(
    nom="Jupiter",
    masse=1.8982e27,  # Masse de Jupiter en kg
    rayon=6.9911e7,  # Rayon de Jupiter en mètres
    position=[778.5e9, 0],  # Distance au Soleil en m sur l'axe x
    vitesse=[-0.1e3, 13.07e3],  # Vitesse en m/s (sur l'axe y)
    acceleration=[0, 0],  # Accélération initiale
    couleur=ORANGE
)
solarSystem.append(jupiter)

# Saturne
saturne = Planet(
    nom="Saturne",
    masse=5.6834e26,  # Masse de Saturne en kg
    rayon=5.8232e7,  # Rayon de Saturne en mètres
    position=[1.429e12, 0],  # Distance au Soleil en m sur l'axe x
    vitesse=[-0.08e3, 9.68e3],  # Vitesse en m/s (sur l'axe y)
    acceleration=[0, 0],  # Accélération initiale
    couleur=GREEN
)
solarSystem.append(saturne)

# Uranus
uranus = Planet(
    nom="Uranus",
    masse=8.6810e25,  # Masse d'Uranus en kg
    rayon=2.5362e7,  # Rayon d'Uranus en mètres
    position=[2.871e12, 0],  # Distance au Soleil en m sur l'axe x
    vitesse=[-0.05e3, 6.80e3],  # Vitesse en m/s (sur l'axe y)
    acceleration=[0, 0],  # Accélération initiale
    couleur=BLUE
)
solarSystem.append(uranus)

# Neptune
neptune = Planet(
    nom="Neptune",
    masse=1.02413e26,  # Masse de Neptune en kg
    rayon=2.4622e7,  # Rayon de Neptune en mètres
    position=[4.495e12, 0],  # Distance au Soleil en m sur l'axe x
    vitesse=[-0.03e3, 5.43e3],  # Vitesse en m/s (sur l'axe y)
    acceleration=[0, 0],  # Accélération initiale
    couleur=WHITE
)
solarSystem.append(neptune)

# Soleil
soleil = Planet(
    nom="Soleil",
    masse=2e30,  # Masse de Neptune en kg
    rayon=6.96342e5,  # Rayon de Neptune en mètres
    position=[SCREEN_WIDTH // 2, SCREEN_HEIGHT //2],  # Distance au Soleil en m sur l'axe x
    vitesse=[0, 0],  # Vitesse en m/s (sur l'axe y)
    acceleration=[0, 0],  # Accélération initiale
    couleur=YELLOW
)
solarSystem.append(soleil)

keysPressed = defaultdict(bool)

def ScanKeyboard():
    for evt in pygame.event.get():
        if evt.type in [pygame.KEYDOWN, pygame.KEYUP]:
            keysPressed[evt.key] = evt.type == pygame.KEYDOWN

zoom = 1.0

bClearScreen = True

# Position de la caméra (coordonnées du centre de la vue)
#camera_x = 0
#camera_y = 0

# Boucle principale
running = True
while running:
    ScanKeyboard()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Si la fenêtre d'animation est fermée
            running = False  # Termine la boucle principale

    # Mettre le fond en noir
    window.fill(BLACK)

    # Ajuster les échelles en fonction du zoom
    echelleDistances = SCREEN_HEIGHT * 2.0e-12 * zoom
    echelleRayonSoleil = SCREEN_HEIGHT * 3.0e-11 * zoom
    echelleRayonsPlanete = SCREEN_HEIGHT * 1.0e-6 * zoom

    # Création du Soleil
    pygame.draw.circle(window, YELLOW, sun_position, int(rayonSoleil * echelleRayonSoleil))
    
    # Mise à jour des planètes avec Runge-Kutta
    runge_kutta(solarSystem, G, dt)
    for planet in solarSystem:
        planet.selfVanish(solarSystem, sun_position, rayonSoleil)
        planet.selfDraw(window, echelleDistances, echelleRayonsPlanete, sun_position, SCREEN_WIDTH, SCREEN_HEIGHT, lambda x, y: realToDisplay(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, 1e13 * zoom, 1e13 * zoom))
    
    pygame.display.flip()

    # Gestion du zoom
    if keysPressed[pygame.K_KP_PLUS]:
        zoom /= 0.99  # Augmenter le zoom pour rapprocher
    if keysPressed[pygame.K_KP_MINUS]:
        zoom *= 0.99  # Réduire le zoom pour éloigner
    if keysPressed[pygame.K_ESCAPE]:
        break
    
    # Dessiner la croix au centre
    draw_centered_cross(window, center_x, center_y, cross_length, CROSS_COLOR)

    # Mettre à jour l'affichage
    pygame.display.update()

    # Vitesse d'exécution
    pygame.time.delay(30)

# Fermeture de PyGame à la fin de l'execution
pygame.quit()
sys.exit()