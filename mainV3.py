import pygame
import sys
from planetV3 import Planet
from bouton import Bouton  

# Initialisation de Pygame
pygame.init()

# Définition des constantes du programme
BLACK = (0, 0, 0)
GREY = (128,128,128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 50)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
ORANGE = (255, 165, 50)
PURPLE = (148, 0, 211)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Génerer fenêtre

pygame.display.set_caption("Simulation de l'Orbite Planétaire") #titre de la fenêtre d'affichage

# Constantes astronomiques
masseSoleil = 1.989e30
rayonSoleil = 6.955e8
G = 6.67384e-11

# Intervalle de temps (en secondes)
dt = 7.2e4  # correspond à environ 1 jour

# Échelles pour l'affichage
echelleDistances = SCREEN_HEIGHT * 2.0e-12  # Échelle des distances
echelleRayonSoleil = SCREEN_HEIGHT * 3.0e-11  # Échelle pour le Soleil
echelleRayonsPlanete = SCREEN_HEIGHT * 1.0e-6  # Échelle pour les planètes

# Création des planètes
solarSystem = []

# Soleil
sun_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Création des planètes
# Mercure
mercure = Planet(
    nom="Mercure",
    masse=3.3011e23,
    rayon=2.4397e6,
    position=[57.9e9, 0],
    vitesse=[0, 47.87e3],
    acceleration=[0, 0],
    couleur=WHITE
)
solarSystem.append(mercure)

# Vénus
venus = Planet(
    nom="Vénus",
    masse=4.8675e24,
    rayon=6.0518e6,
    position=[108.2e9, 0],
    vitesse=[0, 35.02e3],
    acceleration=[0, 0],
    couleur=PURPLE
)
solarSystem.append(venus)

# Terre
terre = Planet(
    nom="Terre",
    masse=5.972e24,
    rayon=6.371e6,
    position=[149.5e9, 0],
    vitesse=[0, 29.8e3],
    acceleration=[0, 0],
    couleur=BLUE
)
solarSystem.append(terre)

# Mars
mars = Planet(
    nom="Mars",
    masse=6.4171e23,
    rayon=3.39e6,
    position=[227.9e9, 0],
    vitesse=[0, 24.077e3],
    acceleration=[0, 0],
    couleur=RED
)
solarSystem.append(mars)

# Jupiter
jupiter = Planet(
    nom="Jupiter",
    masse=1.8982e27,
    rayon=6.9911e7,
    position=[778.5e9, 0],
    vitesse=[0, 13.07e3],
    acceleration=[0, 0],
    couleur=ORANGE
)
solarSystem.append(jupiter)

# Saturne
saturne = Planet(
    nom="Saturne",
    masse=5.6834e26,
    rayon=5.8232e7,
    position=[1.429e12, 0],
    vitesse=[0, 9.68e3],
    acceleration=[0, 0],
    couleur=GREEN
)
solarSystem.append(saturne)

# Uranus
uranus = Planet(
    nom="Uranus",
    masse=8.6810e25,
    rayon=2.5362e7,
    position=[2.871e12, 0],
    vitesse=[0, 6.80e3],
    acceleration=[0, 0],
    couleur=BLUE
)
solarSystem.append(uranus)

# Neptune
neptune = Planet(
    nom="Neptune",
    masse=1.02413e26,
    rayon=2.4622e7,
    position=[4.495e12, 0],
    vitesse=[0, 5.43e3],
    acceleration=[0, 0],
    couleur=WHITE
)
solarSystem.append(neptune)

# Fonction de transformation des coordonnées, d'échelle
def realToDisplay(x, y, window_x, window_y, space_x, space_y):
    x = x * window_x / space_x    #(x,y) coordonnées réelles; window_i = dimensions de la fenêtre d'affichage
    y = y * window_y / space_y
    return x, y

# Création du bouton pause
pause_bouton = Bouton(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 760, 100, 40, "pause", WHITE, GREY, GREY)

# Boucle principale
running = True # Tant que running est true le programme continue de tourner
paused = False  # Variable pour suivre l'état de pause
while running:
    for event in pygame.event.get(): #Traite les interactions souris utilisateur par exemple
        if event.type == pygame.QUIT:  # Si la fenêtre d'animation est fermée la boucle s'arrêtera
            running = False  # Encore heureux mdr

        # Si le bouton est cliqué alterner entre pause et reprise
        if pause_bouton.is_clicked(event): # Vérifie si le bouton pause à été cliqué
            paused = not paused #Si l'animation est en pause elle reprend, sinon elle se "pause " :)
            pause_bouton.toggle_pause() #Lorsque l'on passe de l'état "pause" à "lancer" le texte change

    # Mettre le fond en noir
    window.fill(BLACK)

    # Création du Soleil
    pygame.draw.circle(window, YELLOW, sun_position, int(rayonSoleil * echelleRayonSoleil))

    # Mise à jour des planètes uniquement si l'animation n'est pas en pause => sinon problème d'affichage 
    if not paused: #Si l'animation est en pause le bloc ne s'execute pas, donc les planètes sont immobiles mais elles restent visibles sur l'écran 
        for planet in solarSystem:
            planet.applyGravity(masseSoleil, sun_position, G)
            planet.setPosition(dt)

    # Dessin des planètes à chaque frame, même si l'animation est en pause => sans cette commande les planètes disparaissent lors de la pause
    for planet in solarSystem:
        planet.selfDraw(window, echelleDistances, echelleRayonsPlanete, sun_position, SCREEN_WIDTH, SCREEN_HEIGHT, lambda x, y: realToDisplay(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, 1e13, 1e13))

    # Afficher le bouton pause
    pause_bouton.draw(window) 

    # Mettre à jour l'affichage
    pygame.display.update()

    # Vitesse d'exécution
    pygame.time.delay(30)

# Fermeture de PyGame à la fin de l'exécution
pygame.quit()
sys.exit()
