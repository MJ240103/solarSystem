import pygame

class Bouton:
    def __init__(self, x, y, width, height, text, text_color, bouton_color, hover_color, font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.bouton_color = bouton_color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, font_size)
        self.is_paused = False  # Pour suivre l'état pause ou non

    def draw(self, surface): #Permet d'afficher le bouton
        mouse_pos = pygame.mouse.get_pos() #Récupère la position de la souris sur l'écran
        if self.rect.collidepoint(mouse_pos): #Vérifie si la position de la souris se trouve à l'intérieur du rectangle
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.bouton_color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color) # caractère => image
        text_rect = text_surface.get_rect(center=self.rect.center) #Centre le texte
        surface.blit(text_surface, text_rect) #Place l'image à une position donnée

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos): #Vérifie si la position de la souris lors du clic se trouve à l'intérieur du rectangle
                return True
        return False

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.text = "lancer" if self.is_paused else "pause"