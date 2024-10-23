import tkinter as tk
from tkinter import filedialog
import os
import json
from bodies import Planet
import mainEngine


def eToFloat(s): #String "1e10" -> int 10
    if "e" in s:
        print(s)
        s = s.split("e")
        print(s)
        base = float(s[0])
        expo = int(s[1])
        return base * (10**expo)
    else:
        return float(s)

def intToE(n): #int 10000 -> String "1e4"
    if abs(n) < 10:
        return str(n)
    expo = 0
    while n > 10:
        n = n/10
        expo += 1
    return "{}e{}".format(n, expo)

class Simulation(): #Objet simulation, que l'on passe à notre mainEngine
    def __init__(self, json="{}"):
        self.nom = json["Nom_Simu"]
        self.FPS = json["FPS"]
        self.G = json["G"]
        self.dt = json["dt"]
        self.SPACE_X = json["SPACE_X"]
        self.SPACE_Y = json["SPACE_Y"]
        self.ECHELLE_RAYON = json["ECHELLE_RAYON"]
        self.UNIVERSE_CENTER = json["UNIVERSE_CENTER"]
        self.solarSystem = []

        for planet in json["planetes"]:
            self.solarSystem.append(Planet(
                nom=planet["nom"],
                masse=planet["masse"],  
                rayon=planet["rayon"],  
                position=planet["position"],  
                vitesse=planet["vitesse"],  
                acceleration=planet["acceleration"],
                couleur=planet["couleur"]
            ))
            
    def simToJson(self):
        d = {}
        d["Nom_Simu"] = self.nom
        d["FPS"] = self.FPS
        d["G"] = self.G
        d["dt"] = self.dt
        d["SPACE_X"] = self.SPACE_X
        d["SPACE_Y"] = self.SPACE_Y
        d["ECHELLE_RAYON"] = self.ECHELLE_RAYON
        d["UNIVERSE_CENTER"] = self.UNIVERSE_CENTER

        d["planetes"] = []

        for planet in self.solarSystem:
            dp = {}
            dp["nom"]=planet.nom
            dp["masse"]=planet.masse
            dp["rayon"]=planet.rayon
            dp["position"]=planet.position
            dp["vitesse"]=planet.vitesse
            dp["acceleration"]=planet.acceleration
            dp["couleur"]=planet.couleur
            d["planetes"].append(dp)
        
        return json.dumps(d)
        
        
    def launch(self): #Lancer la simulation
        mainEngine.simulation(self)


class Application(tk.Frame): #Classe d'application principale
    def __init__(self, master=None):
        tk.Frame.__init__(self, master) #On définit l'objet comme étant un objet tkinter. Ainsi, "self" est une "frame" de Tkinter
        
        self.createWidgets() #Initialisation des éléments de la fenetre
        self.fetchDir(path=".", headless=True) #Récupération des fichiers .mj dans le dossier courant

        #Pour que la frame colle aux bords de la fenètre
        self.grid(sticky="nsew")
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1) 
        
        
    def createWidgets(self):

        #Selection du dossier courant
        self.dirVar = tk.StringVar() #Champ text variable
        self.showDir = tk.Entry(self,state="disabled", textvariable=self.dirVar) #Input
        self.showDir.grid(row=0, column = 0, sticky="ew")

        self.fetchDirButton = tk.Button(self, text="Changer Répertoire", command=self.fetchDir)
        self.fetchDirButton.grid(row=0, column = 1, sticky="ew")

        #Liste des fichiers .mj
        self.Lb = tk.Listbox(self)
        self.Lb.grid(row=1, column = 0, rowspan =5, sticky="NSWE")

        #Bouton pour créér une configuration
        self.CreateButton = tk.Button(self, text="Créer config", command=self.createConfig)
        self.CreateButton.grid(row = 2, column = 1, sticky="NSWE")

        #Bouton pour lancer la configuration active
        self.ImportButton = tk.Button(self, text="Lancer config", command=self.launchConfig)
        self.ImportButton.grid(row = 3, column = 1, sticky="NSWE")

        #Bouton pour modifier la configuration active
        self.ExportButton = tk.Button(self, text="Modifier config", command=self.modifyConfig)
        self.ExportButton.grid(row = 4, column = 1, sticky="NSWE")

        #Bouton pour lancer une simulation avec les valeurs en temps réel API
        self.APIButton = tk.Button(self, text="Synchronisation API", command=self.APISync)
        self.APIButton.grid(row = 5, column = 1, sticky="NSWE")

    def fetchDir(self, path = "", headless = False):
        
        # Récupérer la liste des fichiers .mj dans le dossier courant, puis les insère
        # headless = False : On ouvre une fenetre de dialogue pour sélectionner le dossier
        # headless = True : On utilise l'argument path de la fonction
        
        self.Lb.delete(0,'end')
        
        if not headless:
            path = filedialog.askdirectory().strip()
        self.dirVar.set(path)
        filesScanned = os.scandir(path = path)
        files = [file.name for file in filesScanned if file.name[-3:] == ".mj"]
        for file in files:
            self.Lb.insert(tk.END, file) #On insère chaque élément à la fin de la liste

    def listToSim(self):
        fileName = self.Lb.get(tk.ACTIVE)
        dirPath = self.dirVar.get()
        path = dirPath+"/"+fileName
        with open(path,"r") as f:
            data = f.read().replace("\n","").replace("\t","")
            obj = json.loads(data)
            sim = Simulation(obj)
        return sim

    def createConfig(self):
        pass

    def launchConfig(self): #Executer config
        sim = self.listToSim()
        sim.launch()

    def modifyConfig(self): #Ouvrir et modifier config
        sim = self.listToSim()

        #Création fenêtre et initialisation des champs
        simApp = configForm(self, sim)
        simApp.Nom_Simu_Var.set(sim.nom)
        simApp.FPS_Var.set(sim.FPS)
        simApp.G_Var.set(intToE(sim.G))
        simApp.dt_Var.set(intToE(sim.dt))
        simApp.SPACE_X_Var.set(intToE(sim.SPACE_X))
        simApp.SPACE_Y_Var.set(intToE(sim.SPACE_Y))
        simApp.UNIVERSE_CENTER_0_Var.set(intToE(sim.UNIVERSE_CENTER[0]))
        simApp.UNIVERSE_CENTER_1_Var.set(intToE(sim.UNIVERSE_CENTER[1]))
        simApp.ECHELLE_RAYON_Var.set(intToE(sim.ECHELLE_RAYON))
        
        for planet in sim.solarSystem:
            simApp.Lb.insert(tk.END, planet.nom)

        simApp.Lb.select_set(0)
        simApp.Lb.event_generate("<<ListboxSelect>>")

        sim = simApp.show()
        print(sim.nom)

    def APISync(self):
        pass


class configForm():
    def __init__(self, master, sim = {}):
        self.master = master
        self.sim = sim
        
        self.subWindow = tk.Toplevel(master)
        self.createWidgets()
        
    def createWidgets(self):
        #CONFIGURATION GENERALE
        tk.Label(self.subWindow, text="Nom_Simu").grid(row=0, column = 0)

        self.Nom_Simu_Var = tk.StringVar()
        self.subWindow.Nom_Simu = tk.Entry(self.subWindow, textvariable=self.Nom_Simu_Var)
        self.subWindow.Nom_Simu.grid(row=0, column = 1, columnspan=4, sticky="EW")

        tk.Label(self.subWindow, text="FPS").grid(row=1, column = 0)

        self.FPS_Var = tk.StringVar()
        self.FPS = tk.Entry(self.subWindow, textvariable=self.FPS_Var)
        self.FPS.grid(row=1, column = 1, columnspan=4, sticky="EW")

        tk.Label(self.subWindow, text="G").grid(row=2, column = 0)

        self.G_Var = tk.StringVar()
        self.G = tk.Entry(self.subWindow, textvariable=self.G_Var)
        self.G.grid(row=2, column = 1, columnspan=4, sticky="EW")

        tk.Label(self.subWindow, text="dt").grid(row=3, column = 0)

        self.dt_Var = tk.StringVar()
        self.dt = tk.Entry(self.subWindow, textvariable=self.dt_Var)
        self.dt.grid(row=3, column = 1, columnspan=4, sticky="EW")

        tk.Label(self.subWindow, text="SPACE_X").grid(row=4, column = 0)

        self.SPACE_X_Var = tk.StringVar()
        self.SPACE_X = tk.Entry(self.subWindow, textvariable=self.SPACE_X_Var)
        self.SPACE_X.grid(row=4, column = 1, columnspan=4, sticky="EW")

        tk.Label(self.subWindow, text="SPACE_Y").grid(row=5, column = 0)

        self.SPACE_Y_Var = tk.StringVar()
        self.SPACE_Y = tk.Entry(self.subWindow, textvariable=self.SPACE_Y_Var)
        self.SPACE_Y.grid(row=5, column = 1, columnspan=4, sticky="EW")

        tk.Label(self.subWindow, text="UNIVERSE_CENTER").grid(row=6, column = 0)

        self.UNIVERSE_CENTER_0_Var = tk.StringVar()
        self.UNIVERSE_CENTER_0 = tk.Entry(self.subWindow, textvariable=self.UNIVERSE_CENTER_0_Var)
        self.UNIVERSE_CENTER_0.grid(row=6, column = 1,sticky="EW")

        self.UNIVERSE_CENTER_1_Var = tk.StringVar()
        self.UNIVERSE_CENTER_1 = tk.Entry(self.subWindow, textvariable=self.UNIVERSE_CENTER_1_Var)
        self.UNIVERSE_CENTER_1.grid(row=6, column = 2, columnspan=3,sticky="EW")

        tk.Label(self.subWindow, text="ECHELLE_RAYON").grid(row=7, column = 0)

        self.ECHELLE_RAYON_Var = tk.StringVar()
        self.ECHELLE_RAYON = tk.Entry(self.subWindow, textvariable=self.ECHELLE_RAYON_Var)
        self.ECHELLE_RAYON.grid(row=7, column = 1, columnspan=4, sticky="EW")

        self.Lb = tk.Listbox(self.subWindow)
        self.Lb.grid(row = 8, column = 0,rowspan=8)
        self.Lb.bind('<<ListboxSelect>>',self.changePlanetSelection)

        #CONFIGURATION PLANETES
        tk.Label(self.subWindow, text="PLANETE CONFIGURATION").grid(row=8, column=1, columnspan=4,sticky="EW")

        tk.Label(self.subWindow, text="Nom").grid(row=9, column=1,sticky="W")
        self.NOM_PLANETE_Var = tk.StringVar()
        self.NOM_PLANETE = tk.Entry(self.subWindow, textvariable=self.NOM_PLANETE_Var)
        self.NOM_PLANETE.grid(row=9, column = 2, columnspan=3, sticky="WE")

        tk.Label(self.subWindow, text="Masse").grid(row=10, column=1,sticky="W")
        self.MASSE_Var = tk.StringVar()
        self.MASSE = tk.Entry(self.subWindow, textvariable=self.MASSE_Var)
        self.MASSE.grid(row=10, column = 2, columnspan=3, sticky="WE")

        tk.Label(self.subWindow, text="Rayon").grid(row=11, column=1,sticky="W")
        self.RAYON_Var = tk.StringVar()
        self.RAYON = tk.Entry(self.subWindow, textvariable=self.RAYON_Var)
        self.RAYON.grid(row=11, column = 2, columnspan=3, sticky="WE")

        tk.Label(self.subWindow, text="Position").grid(row=12, column=1,sticky="W")
        self.X_Var = tk.StringVar()
        self.Y_Var = tk.StringVar()
        self.X = tk.Entry(self.subWindow, textvariable=self.X_Var)
        self.Y = tk.Entry(self.subWindow, textvariable=self.Y_Var)
        self.X.grid(row=12, column = 2, sticky="WE")
        self.Y.grid(row=12, column = 3, columnspan=2, sticky="WE")

        tk.Label(self.subWindow, text="Vitesse").grid(row=13, column=1,sticky="W")
        self.VX_Var = tk.StringVar()
        self.VY_Var = tk.StringVar()
        self.VX = tk.Entry(self.subWindow, textvariable=self.VX_Var)
        self.VY = tk.Entry(self.subWindow, textvariable=self.VY_Var)
        self.VX.grid(row=13, column = 2, sticky="WE")
        self.VY.grid(row=13, column = 3, columnspan=2, sticky="WE")

        tk.Label(self.subWindow, text="Acceleration").grid(row=14, column=1,sticky="W")
        self.AX_Var = tk.StringVar()
        self.AY_Var = tk.StringVar()
        self.AX = tk.Entry(self.subWindow, textvariable=self.AX_Var)
        self.AY = tk.Entry(self.subWindow, textvariable=self.AY_Var)
        self.AX.grid(row=14, column = 2, sticky="WE")
        self.AY.grid(row=14, column = 3, columnspan=2, sticky="WE")

        tk.Label(self.subWindow, text="Couleur").grid(row=15, column=1,sticky="W")
        self.RC_Var = tk.StringVar()
        self.GC_Var = tk.StringVar()
        self.BC_Var = tk.StringVar()
        self.RC = tk.Entry(self.subWindow, textvariable=self.RC_Var)
        self.GC = tk.Entry(self.subWindow, textvariable=self.GC_Var)
        self.BC = tk.Entry(self.subWindow, textvariable=self.BC_Var)
        self.RC.grid(row=15, column = 2, sticky="WE")
        self.GC.grid(row=15, column = 3, sticky="WE")
        self.BC.grid(row=15, column = 4, sticky="WE")
        
        #CONFIGURATION COMMANDES
        self.savePlanetButton = tk.Button(self.subWindow, text="Sauvegarder planète", command=self.savePlanet)
        self.savePlanetButton.grid(row=16,column=0,sticky="NSWE")

        self.saveConfigButton = tk.Button(self.subWindow, text="Sauvegarder configuration", command=self.saveConfig)
        self.saveConfigButton.grid(row=16,column=1,sticky="NSWE")
        
        self.deleteConfButton = tk.Button(self.subWindow, text="Supprimer configuration", command=self.deleteConfig)
        self.deleteConfButton.grid(row=16,column=2,sticky="NSWE")

        self.launchConfigButton = tk.Button(self.subWindow, text="Lancer simulation", command=self.launchConfig)
        self.launchConfigButton.grid(row=16,column=4,sticky="NSWE")
        
        self.subWindow.grid()

    def changePlanetSelection(self, evt):
        w = evt.widget
        idPlanet = int(w.curselection()[0])
        planet = self.sim.solarSystem[idPlanet]


        #Affiche les valeurs de la planète dans les champs
        self.NOM_PLANETE_Var.set(planet.nom)
        self.MASSE_Var.set(intToE(planet.masse))
        self.RAYON_Var.set(intToE(planet.rayon))
        self.X_Var.set(intToE(planet.position[0]))
        self.Y_Var.set(intToE(planet.position[1]))
        self.VX_Var.set(intToE(planet.vitesse[0]))
        self.VY_Var.set(intToE(planet.vitesse[1]))
        self.AX_Var.set(intToE(planet.acceleration[0]))
        self.AY_Var.set(intToE(planet.acceleration[1]))
        self.RC_Var.set(planet.couleur[0])
        self.GC_Var.set(planet.couleur[1])
        self.BC_Var.set(planet.couleur[2])
        
    def updSim(self):
        self.sim.nom = self.Nom_Simu_Var.get()
        self.sim.FPS = int(self.FPS_Var.get())
        self.sim.G = eToFloat(self.G_Var.get())
        self.sim.dt = eToFloat(self.dt_Var.get())
        self.sim.SPACE_X = eToFloat(self.SPACE_X_Var.get())
        self.sim.SPACE_Y = eToFloat(self.SPACE_Y_Var.get())
        self.sim.ECHELLE_RAYON = eToFloat(self.ECHELLE_RAYON_Var.get())
        self.sim.UNIVERSE_CENTER = (eToFloat(self.UNIVERSE_CENTER_0_Var.get()), eToFloat(self.UNIVERSE_CENTER_1_Var.get()))

    def savePlanet(self):
        idPlanet = self.Lb.curselection()[0]
        planet = self.sim.solarSystem[idPlanet]

        planet.nom = self.NOM_PLANETE_Var.get()
        planet.rayon = eToFloat(self.RAYON_Var.get())
        planet.position = [eToFloat(self.X_Var.get()), eToFloat(self.Y_Var.get())]
        planet.vitesse = [eToFloat(self.VX_Var.get()), eToFloat(self.VY_Var.get())]
        planet.acceleration = [eToFloat(self.AX_Var.get()), eToFloat(self.AY_Var.get())]
        planet.couleur = [int(self.RC_Var.get()), int(self.GC_Var.get()), int(self.BC_Var.get())]
        
    def deleteConfig(self):
        pass

    def saveConfig(self):
        self.updSim()
        jsonString = self.sim.simToJson()

        file = tk.filedialog.asksaveasfilename(filetypes=[("Fichier Simulation",".mj")])
        
        with open(file,"w",encoding="utf-8") as f:
            f.write(jsonString)
        
        self.subWindow.destroy()

    def launchConfig(self):
        self.updSim()
        #self.subWindow.destroy()
        self.sim.launch()
    
    def show(self):
        self.subWindow.transient(self.master)
        self.subWindow.grab_set()
        self.master.wait_window(self.subWindow)
        
        return self.sim


if __name__ == "__main__":
    app = Application()
    app.master.geometry("600x400")
    app.master.title("Système Solaire")
    app.mainloop()
