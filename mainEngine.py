import pygame
import sys
from bodies import Planet
from bodies import runge_kutta
from collections import defaultdict

#################################################################
# CE FICHIER N'EST PAS INDEPENDANT                              #
# POUR LANCER UNE SIMULATION, EXECUTER UN FICHIER DE SIMULATION #
# CE FIHIER Y SERA IMPORTE                                      #
#################################################################

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 50)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
ORANGE = (255, 165, 50)
PURPLE = (148, 0, 211)
GREY = (128, 128, 128)
STEP = 100

def simulation(config):
    # Initialisation de Pygame
    print(config.G)
    pygame.init()
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Gravity simulation (SPACE: show orbits, '
                               'keypad +/- : zoom in/out)')
    clock = pygame.time.Clock()

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

    def realToDisplay(x,y,window_x,window_y,space_x,space_y):
        x = (x*window_x/space_x)
        y = (y*window_y/space_y)
        return x,y

    #Variable de simu
    zoom = 1.0
    # Boucle principale
    running = True
    show_orbits = False # Variable pour contrôler l'affichage des trajectoires
    follow_index = 0 # Indice (dans la liste solarSystem) de la planete suivie, quand on en suit une
    follow_mode = 0         #Mode de suivi: 0 DEFAULT = Centré sur UNIVERSE_CENTER
                            #               1 FOCUS = Centré sur une planète
                            #               2 FREE = MOUVEMENT LIBRE

    curCenter = config.UNIVERSE_CENTER #Initialisation centrage
    
    window.fill(BLACK)
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si la fenêtre d'animation est fermée
                running = False  # Termine la boucle principale
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    zoom -= 0.1  # Augmenter le zoom pour rapprocher
                    print(zoom)
                elif event.key == pygame.K_h:
                    zoom += 0.1  # Réduire le zoom pour éloigner
                    print(zoom)
                elif event.key == pygame.K_SPACE:
                    show_orbits = not show_orbits  # Bascule de l'affichage des trajectoires
                elif event.key == pygame.K_ESCAPE:
                    running = False  # Quitte la simulation
                elif event.key == pygame.K_m: #Changer le mode de suivi
                    follow_mode = (follow_mode + 1) % 3
                elif event.key == pygame.K_j: #Changer la planète suivi
                    follow_mode = 1
                    follow_index = (follow_index - 1) % len(config.solarSystem)
                    print(follow_index)
                elif event.key == pygame.K_k: #Changer la planète suivi
                    follow_mode = 1
                    follow_index = (follow_index + 1) % len(config.solarSystem)
                    print(follow_index)
                    
                elif event.key == pygame.K_z: #Changer la planète suivi
                    follow_mode = 2
                    curCenter = [curCenter[0], curCenter[1] + config.SPACE_Y / STEP]

                elif event.key == pygame.K_s: #Changer la planète suivi
                    follow_mode = 2
                    curCenter = [curCenter[0], curCenter[1] - config.SPACE_Y / STEP]

                elif event.key == pygame.K_d: #Changer la planète suivi
                    follow_mode = 2
                    curCenter = [curCenter[0] - config.SPACE_X/STEP, curCenter[1]]

                elif event.key == pygame.K_q: #Changer la planète suivi
                    follow_mode = 2
                    curCenter = [curCenter[0] + config.SPACE_X/STEP, curCenter[1]]
                    

        # Mettre le fond en noir uniquement si les orbites ne sont pas affichées
        if not show_orbits:
            window.fill(BLACK)
        
        # Mise à jour des planètes avec Runge-Kutta
        runge_kutta(config.solarSystem, config.G, config.dt)

        # Gestion suivi

        if follow_mode == 0:
            curCenter = config.UNIVERSE_CENTER
        elif follow_mode == 1:
            pos = config.solarSystem[follow_index].position
            curCenter = (config.SPACE_X/2 - pos[0]*zoom, config.SPACE_Y/2 - pos[1]*zoom)
            #print(config.solarSystem[follow_index].nom, pos, curCenter)
        elif follow_mode == 2:
            pass
        

        # Affichage des planètes
        for planet in config.solarSystem:
            planet.selfDraw(
                window,
                config.ECHELLE_RAYON,
                curCenter,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                zoom,
                lambda x, y: realToDisplay(x,y,SCREEN_WIDTH,SCREEN_HEIGHT,config.SPACE_X,config.SPACE_Y))
        
        # Dessiner la croix au centre
        draw_centered_cross(window, center_x, center_y, cross_length, CROSS_COLOR)


        pygame.display.flip()
        pygame.display.update()
        clock.tick(config.FPS)

    # Fermeture de PyGame à la fin de l'execution
    pygame.quit()

if __name__ == "__main__":
    simulation()
