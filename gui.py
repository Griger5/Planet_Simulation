import pygame
import json
from pathlib import Path

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
    def __init__(self, window, x, y, radius, color, list, name, distance, name_font, distance_font, info_font, info_font2, index):
        self.window = window
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.list = list
        self.distance = distance
        self.distance_font = distance_font
        self.info_font = info_font
        self.info_font2 = info_font2
        self.index = index

        self.alreadyPressed = False
        self.showInfoPanel = False

        self.width, self.height = 190, 150

        self.containerColors = {
            "normal":(35,35,35),
            "hover":(60,60,60),
            "pressed":(90,90,90),
        }
        
        root_dir = Path(__file__).resolve().parent
        with open(str(root_dir)+"\planet_info.json") as file:
            self.information = json.load(file)["details"][self.index]

        self.statSurface = pygame.Surface((self.width, self.height))
        self.statSurface.fill((20,20,20))
        self.statRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.planetName = name_font.render(name, True, (180, 180, 180))

        self.distanceText = self.distance_font.render("", True, (180, 180, 180))

        self.list.append(self)

    def showInfo(self):
        width = 200
        height = 400
        infoSurface = pygame.Surface((width, height))
        infoSurface.set_alpha(220)
        pygame.draw.rect(infoSurface, (35,35,35), (0, 0, width, height), 0, 10)
        stat = self.list[self.index]
        if stat.x < 600:
            x = 200
        else:
            x = 800
        if stat.y < height:
            # it looks a bit nicer with -5 in my opinion
            y = stat.y - 5
        else:
            y = 800 - height
        infoRect = pygame.Rect(x, y, width, height)

        type_name = self.info_font2.render("Name:", True, (180, 180, 180))
        name = self.info_font.render(self.information["name"], True, (180, 180, 180))
        type_diameter = self.info_font2.render("Diameter:", True, (180, 180, 180))
        diameter = self.info_font.render(self.information["diameter"], True, (180, 180, 180))
        type_mass = self.info_font2.render("Mass:", True, (180, 180, 180))
        mass = self.info_font.render(self.information["mass"], True, (180, 180, 180))
        type_daylength = self.info_font2.render("Spin time:", True, (180, 180, 180))
        daylength = self.info_font.render(self.information["dayLength"], True, (180, 180, 180))
        type_yearlength = self.info_font2.render("Orbit time:", True, (180, 180, 180))
        yearlength = self.info_font.render(self.information["yearLength"], True, (180, 180, 180))
        type_trivia = self.info_font2.render("Trivia:", True, (180, 180, 180))

        infoSurface.blit(type_name, [width/2 - type_name.get_rect().width/2, 10])
        infoSurface.blit(name, [width/2 - name.get_rect().width/2, 35])
        infoSurface.blit(type_diameter, [width/2 - type_diameter.get_rect().width/2, 65])
        infoSurface.blit(diameter, [width/2 - diameter.get_rect().width/2, 90])
        infoSurface.blit(type_mass, [width/2 - type_mass.get_rect().width/2, 120])
        infoSurface.blit(mass, [width/2 - mass.get_rect().width/2, 145])
        infoSurface.blit(type_daylength, [width/2 - type_daylength.get_rect().width/2, 175])
        infoSurface.blit(daylength, [width/2 - daylength.get_rect().width/2, 200])
        infoSurface.blit(type_yearlength, [width/2 - type_yearlength.get_rect().width/2, 230])
        infoSurface.blit(yearlength, [width/2 - yearlength.get_rect().width/2, 255])
        infoSurface.blit(type_trivia, [width/2 - type_trivia.get_rect().width/2, 285])

        # pygame doesn't support multiline texts, I used the most primitive idea to solve it, I may re-do it someday in a smarter way
        for i,item in enumerate(self.information["trivia"]):
            trivia = self.distance_font.render(self.information["trivia"][item], True, (180, 180, 180))
            infoSurface.blit(trivia, [10, 310+20*i])

        self.window.blit(infoSurface, infoRect)
    
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.statSurface.fill((20,20,20))
        
        if self.showInfoPanel:
            self.showInfo()

        if self.statRect.collidepoint(mousePos):
            pygame.draw.rect(self.statSurface, self.containerColors["hover"], (0, 0, self.width, self.height), 0, 10)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                pygame.draw.rect(self.statSurface, self.containerColors["pressed"], (0, 0, self.width, self.height), 0, 10)
                if not self.alreadyPressed:
                    if self.showInfoPanel:
                        self.showInfoPanel = False
                    else:
                        self.showInfoPanel = True
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        else:
            pygame.draw.rect(self.statSurface, self.containerColors["normal"], (0, 0, self.width, self.height), 0, 10)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.showInfoPanel = False

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