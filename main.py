import pygame
import math
import constants as c
import objects as o
import gui

pygame.init()

WIN = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption("Planet Simulation")

class PlanetSimulation():
    def __init__(self) -> None:
        run = True
        clock = pygame.time.Clock()
        font1 = pygame.font.SysFont('Arial', 35, True)
        font2 = pygame.font.SysFont('Arial', 30)
        self.scale = c.SCALE
        
        # required, to not make the zooming out rapidly "speed up"
        self.scale_exp = 0

        buttons = []
        gui.Button(WIN,x=1100,y=730,width=150,height=50,colors=("#ffffff","#777777","#333333"),list=buttons,font=font1,text="Zoom in",command=self.zoom_in,multiclick=True)
        gui.Button(WIN,x=1100,y=800,width=150,height=50,colors=("#ffffff","#777777","#333333"),list=buttons,font=font1,text="Zoom out",command=self.zoom_out,multiclick=True)

        self.bodies = []
        sun = o.Celestial_Body(x=0, y=0, radius=30, color=(255,255,0), mass=c.MASS_SUN, is_center=True, is_sun=True, list=self.bodies, scale=self.scale, name="Sun")
        mercury = o.Celestial_Body(x=-0.39*c.AU, y=0, radius=8, color=(93,93,93), mass=c.MASS_MERCURY, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Mercury")
        venus = o.Celestial_Body(x=-0.72*c.AU, y=0, radius=14, color=(153,102,0), mass=c.MASS_VENUS, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Venus")
        earth = o.Celestial_Body(x=-1*c.AU, y=0, radius=15, color=(0,0,255), mass=c.MASS_EARTH, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Earth")
        mars = o.Celestial_Body(x=-1.52*c.AU, y=0, radius=10, color=(250,30,30), mass=c.MASS_MARS, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Mars")
        jupiter = o.Celestial_Body(x=-5.2*c.AU, y=0, radius=20, color=(165,42,42), mass=c.MASS_JUPITER, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Jupiter")
        saturn = o.Celestial_Body(x=-9.54*c.AU, y=0, radius=18, color=(200,101,0), mass=c.MASS_SATURN, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Saturn")
        uranus = o.Celestial_Body(x=-19.2*c.AU, y=0, radius=15, color=(46,139,87), mass=c.MASS_URANUS, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Uranus")
        neptune = o.Celestial_Body(x=-30.06*c.AU, y=0, radius=16, color=(0,0,120), mass=c.MASS_NEPTUNE, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Neptune")

        # since all objects are placed on the y-axis at the start, their x-axis_velocity is equal to 0,
        # so their initial (and constant) velocity is just the y-axis_velocity 
        mercury.vel_y = mercury.initial_velocity(self.bodies)
        venus.vel_y = venus.initial_velocity(self.bodies)
        earth.vel_y = earth.initial_velocity(self.bodies)
        mars.vel_y = mars.initial_velocity(self.bodies)
        jupiter.vel_y = jupiter.initial_velocity(self.bodies)
        saturn.vel_y = saturn.initial_velocity(self.bodies)
        uranus.vel_y = uranus.initial_velocity(self.bodies)
        neptune.vel_y = neptune.initial_velocity(self.bodies)

        stats = []
        for i,body in enumerate(self.bodies[1:-3]):
            gui.PlanetStats(WIN, 5, 8+i*158, body.radius, body.color, stats, font2, body.name, -body.x)
        for i,body in enumerate(self.bodies[6:]+self.bodies[0:-8]):
            gui.PlanetStats(WIN, 1005, 8+i*158, body.radius, body.color, stats, font2, body.name, -body.x)
        
        
        #gui.PlanetStats(WIN, 5, 5, 8, (93,93,93), buttons, font2, "Mercury", 0.39*c.AU)

        while run:
            clock.tick(60) 
            WIN.fill((0,0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            for body in self.bodies:
                if not body.is_center:
                    body.move(self.bodies)
                body.show(WIN)
            
            pygame.draw.rect(WIN, (20,20,20), (0,0,200,800))
            pygame.draw.rect(WIN, (20,20,20), (1000,0,200,800))

            for button in buttons:
                button.process()
            for stat in stats:
                stat.process()
            
            pygame.display.update()

        pygame.quit()

    def zoom_in(self):
            self.scale += math.exp(self.scale_exp) / c.AU
            # 42 is the answer to everything
            self.scale_exp += 0.0042
            for body in self.bodies:
                body.scale = self.scale
    def zoom_out(self):
        if self.scale > 0:
            self.scale -= math.exp(self.scale_exp) / c.AU
            self.scale_exp -= 0.0042
            for body in self.bodies:
                body.scale = self.scale

if __name__ == "__main__":
    PlanetSimulation()