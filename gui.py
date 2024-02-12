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


class PlanetStats():
    def __init__(self, window, x, y, radius, color, list, name, distance, name_font, distance_font):
        self.window = window
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.list = list
        self.distance = distance
        self.distance_font = distance_font
        self.alreadyPressed = False

        self.width, self.height = 190, 150

        self.containerColors = {
            "normal":(35,35,35),
            "hover":(60,60,60),
            "pressed":(90,90,90),
        }

        self.statSurface = pygame.Surface((self.width, self.height))
        self.statSurface.fill((20,20,20))
        self.statRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.planetName = name_font.render(name, True, (180, 180, 180))

        self.distanceText = self.distance_font.render("", True, (180, 180, 180))

        list.append(self)
    
    def process(self, bodies):
        self.statSurface.fill((20,20,20))
        pygame.draw.rect(self.statSurface, self.containerColors["normal"], (0, 0, self.width, self.height), 0, 10)

        pygame.draw.circle(self.statSurface, self.color, (self.width/2, self.height/2), self.radius)
        if self.distance != 0:
            self.distanceText = self.distance_font.render(str(self.distance/1000)+" Km", True, (180, 180, 180))
        
        self.statSurface.blit(self.planetName, [
            self.width/2 - self.planetName.get_rect().width/2,
            self.height/6 - self.planetName.get_rect().height/2
        ])
        self.statSurface.blit(self.distanceText, [
            self.width/2 - self.distanceText.get_rect().width/2,
            self.height/1.1 - self.distanceText.get_rect().height/1.1
        ])
        
        self.window.blit(self.statSurface, self.statRect)