import pygame
import math
import constants as c
import objects as o
import gui

pygame.init()

WIN = pygame.display.set_mode((c.WIDTH, c.HEIGHT))

pygame.display.set_caption("Planet Simulation")

pygame.key.set_repeat(8)

class PlanetSimulation():
    def __init__(self) -> None:
        run = True
        clock = pygame.time.Clock()
        font1 = pygame.font.SysFont('Arial', 35, True)
        font2 = pygame.font.SysFont('Times new roman', 30)
        font3 = pygame.font.SysFont('Arial', 18)
        self.scale = c.SCALE
        
        # required, to not make the zooming out rapidly "speed up"
        self.scale_exp = 0

        buttons = []
        gui.Button(WIN,x=1100,y=730,width=150,height=50,colors=("#ffffff","#777777","#333333"),list=buttons,font=font1,text="Zoom in",command=self.zoom_in,multiclick=True)
        gui.Button(WIN,x=1100,y=800,width=150,height=50,colors=("#ffffff","#777777","#333333"),list=buttons,font=font1,text="Zoom out",command=self.zoom_out,multiclick=True)

        self.bodies = []
        mercury = o.Celestial_Body(x=-0.39*c.AU, y=0, radius=8, color=(93,93,93), mass=c.MASS_MERCURY, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Mercury", offset_x=0, offset_y=0)
        venus = o.Celestial_Body(x=-0.72*c.AU, y=0, radius=14, color=(153,102,0), mass=c.MASS_VENUS, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Venus", offset_x=0, offset_y=0)
        earth = o.Celestial_Body(x=-1*c.AU, y=0, radius=15, color=(0,0,255), mass=c.MASS_EARTH, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Earth", offset_x=0, offset_y=0)
        mars = o.Celestial_Body(x=-1.52*c.AU, y=0, radius=10, color=(250,30,30), mass=c.MASS_MARS, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Mars", offset_x=0, offset_y=0)
        jupiter = o.Celestial_Body(x=-5.2*c.AU, y=0, radius=20, color=(165,42,42), mass=c.MASS_JUPITER, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Jupiter", offset_x=0, offset_y=0)
        saturn = o.Celestial_Body(x=-9.54*c.AU, y=0, radius=18, color=(200,101,0), mass=c.MASS_SATURN, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Saturn", offset_x=0, offset_y=0)
        uranus = o.Celestial_Body(x=-19.2*c.AU, y=0, radius=15, color=(46,139,87), mass=c.MASS_URANUS, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Uranus", offset_x=0, offset_y=0)
        neptune = o.Celestial_Body(x=-30.06*c.AU, y=0, radius=16, color=(0,0,120), mass=c.MASS_NEPTUNE, is_center=False, is_sun=False, list=self.bodies, scale=self.scale, name="Neptune", offset_x=0, offset_y=0)
        sun = o.Celestial_Body(x=0, y=0, radius=30, color=(255,255,0), mass=c.MASS_SUN, is_center=True, is_sun=True, list=self.bodies, scale=self.scale, name="Sun", offset_x=0, offset_y=0)

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
        for i,body in enumerate(self.bodies[:-4]):
            gui.PlanetStats(WIN, 5, 8+i*158, body.radius, body.color, stats, body.name, body.x, font2, font3)
        for i,body in enumerate(self.bodies[5:]):
            gui.PlanetStats(WIN, 1005, 8+i*158, body.radius, body.color, stats, body.name, body.x, font2, font3)

        while run:
            clock.tick(60) 
            WIN.fill((0,0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.move_right()
                    elif event.key == pygame.K_LEFT:
                        self.move_left()
                    elif event.key == pygame.K_UP:
                        self.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.move_down()

            for i,body in enumerate(self.bodies):
                body.move(self.bodies)
                stats[i].distance = body.distance_to_sun
                body.show(WIN)
            
            pygame.draw.rect(WIN, (20,20,20), (0,0,200,800))
            pygame.draw.rect(WIN, (20,20,20), (1000,0,200,800))

            for button in buttons:
                button.process()

            for stat in stats:
                stat.process(self.bodies)
            
            pygame.display.update()

        pygame.quit()

    def zoom_in(self):
            self.scale += math.exp(self.scale_exp) / c.AU
            # 42 is the answer to everything
            self.scale_exp += 0.0042
            for body in self.bodies:
                body.scale = self.scale
                body.radius += math.exp(self.scale_exp)/20
    def zoom_out(self):
        if self.scale > 0:
            self.scale -= math.exp(self.scale_exp) / c.AU
            self.scale_exp -= 0.0042
            for body in self.bodies:
                body.scale = self.scale
                body.radius -= math.exp(self.scale_exp)/20
    def move_right(self):
        for body in self.bodies:
            body.offset_x += -1
    def move_left(self):
        for body in self.bodies:
            body.offset_x += 1
    def move_up(self):
        for body in self.bodies:
            body.offset_y += 1
    def move_down(self):
        for body in self.bodies:
            body.offset_y += -1

if __name__ == "__main__":
    PlanetSimulation()