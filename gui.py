import pygame

class Button():
    def __init__(self, window, x, y, width, height, colors, list, font, text="", command=None, multiclick=False):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.command = command
        self.multiclick = multiclick
        self.alreadyPressed = False

        self.activeColors = {
            "normal":colors[0],
            "hover":colors[1],
            "pressed":colors[2],
        }

        self.position_x = x - width/2
        self.position_y = y - width/2

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.position_x, self.position_y, self.width, self.height)

        self.buttonText = font.render(text, True, (20, 20, 20))

        list.append(self)
    
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.activeColors['normal'])
        
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.activeColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.activeColors['pressed'])
                if not self.multiclick:
                    if not self.alreadyPressed:
                        self.command()
                        self.alreadyPressed = True
                else:
                    self.command()
            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonText, [
            self.buttonRect.width/2 - self.buttonText.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonText.get_rect().height/2
        ])
        
        self.window.blit(self.buttonSurface, self.buttonRect)