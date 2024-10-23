from bodies import Planet
import mainEngine

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 50)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
ORANGE = (255, 165, 50)
PURPLE = (148, 0, 211)
GREY = (128, 128, 128)

class Simulation():
    def __init__(self, **kwargs):
        self.nom = kwargs.get("Nom_Simu")
        self.FPS = kwargs.get("FPS")
        self.G = kwargs.get("G")
        self.dt = kwargs.get("dt")
        self.SPACE_X = kwargs.get("SPACE_X")
        self.SPACE_Y = kwargs.get("SPACE_Y")
        self.ECHELLE_RAYON = kwargs.get("ECHELLE_RAYON")
        self.UNIVERSE_CENTER = kwargs.get("UNIVERSE_CENTER")
        self.solarSystem = kwargs.get("solarSystem")

    def launch(self):
        mainEngine.simulation(self)

if __name__ == "__main__":
    # Constantes astronomiques
    G = -6.67384e-11
    FPS = 300

    # Intervalle de temps (en secondes)
    dt = 7.2e4  # correspond à environ 1 jour (86400 secondes approximées à moins car simulation trop lente sinon)
    SPACE_X = 1e13
    SPACE_Y = 1e13
    UNIVERSE_CENTER = (SPACE_X/2,SPACE_Y/2)
    ECHELLE_RAYON = 600


    ### PLANETES ###
    solarSystem = [] #Initialisation de la liste de planètes


    """ COMMENT CREER UNE PLANETE :
    solarSystem.append(Planet(
        nom="PLANETE",
        masse = 0 # Masse en kg
        rayon = 0 # Masse en m
        position = [0,0] # Position dans l'Espace
        vitesse = [0, 0] # Vitesse initiale
        acceleration=[0, 0] # Accélération initiale
        couleur=WHITE
    ))

    """

    # Création des planètes
        # Mercure

    solarSystem.append(Planet(
        nom="Mercure",
        masse=3.3011e23,  
        rayon=2.4397e6,  
        position=[57.9e9, 0],  
        vitesse=[0, 47.87e3],  
        acceleration=[0, 0],
        couleur=WHITE
    ))

        # Vénus

    solarSystem.append(Planet(
        nom="Vénus",
        masse=4.8675e24,
        rayon=6.0518e6,
        position=[108.2e9, 0],
        vitesse=[-0.3e3, 35.02e3],
        acceleration=[0, 0], 
        couleur=PURPLE
    ))

    # Terre

    solarSystem.append(Planet(
        nom="Terre",
        masse=5.972e24,
        rayon=6.371e6,
        position=[149.5e9, 0],
        vitesse=[-0.2e3, 29.8e3],
        acceleration=[0, 0],
        couleur=BLUE
    ))

    # Mars
    solarSystem.append(Planet(
        nom="Mars",
        masse=6.4171e23,
        rayon=3.39e6,
        position=[227.9e9, 0],
        vitesse=[-0.15e3, 24.077e3],
        acceleration=[0, 0],
        couleur=RED
    ))

    # Jupiter
    solarSystem.append(Planet(
        nom="Jupiter",
        masse=1.8982e27,
        rayon=6.9911e7,
        position=[778.5e9, 0],
        vitesse=[-0.1e3, 13.07e3],
        acceleration=[0, 0],
        couleur=ORANGE
    ))

    # Saturne
    solarSystem.append(Planet(
        nom="Saturne",
        masse=5.6834e26,
        rayon=5.8232e7,
        position=[1.429e12, 0],
        vitesse=[-0.08e3, 9.68e3],
        acceleration=[0, 0],
        couleur=GREEN
    ))

    # Uranus
    solarSystem.append(Planet(
        nom="Uranus",
        masse=8.6810e25,
        rayon=2.5362e7,
        position=[2.871e12, 0],
        vitesse=[-0.05e3, 6.80e3],
        acceleration=[0, 0],
        couleur=BLUE
    ))

    # Neptune

    solarSystem.append(Planet(
        nom="Neptune",
        masse=1.02413e26,
        rayon=2.4622e7,
        position=[4.495e12, 0],
        vitesse=[-0.03e3, 5.43e3],
        acceleration=[0, 0],
        couleur=WHITE
    ))

    # Soleil
    solarSystem.append(Planet(
        nom="Soleil",
        masse=1.989e30,
        rayon=6.955e8,
        position=[0,0],
        vitesse=[0, 0],
        acceleration=[0, 0],
        couleur=YELLOW
    ))

    #Définition Simulation
    S = Simulation(Nom_Simu = "SystemeSolaire",
                   FPS = FPS,
                   G = G,
                   dt = dt,
                   SPACE_X = SPACE_X,
                   SPACE_Y = SPACE_Y,
                   ECHELLE_RAYON = ECHELLE_RAYON,
                   UNIVERSE_CENTER = UNIVERSE_CENTER,
                   solarSystem = solarSystem
                   )

    S.launch()
