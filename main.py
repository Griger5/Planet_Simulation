import pygame
import constants as c
import objects as o

pygame.init()

WIN = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption("Planet Simulation")

class GUI():
    def __init__(self) -> None:
        run = True
        clock = pygame.time.Clock()

        sun = o.Celestial_Body(x=0, y=0, radius=30, color=(255,255,0), mass=c.MASS_SUN, is_center=False)
        mercury = o.Celestial_Body(x=-0.39*c.AU, y=0, radius=8, color=(93,93,93), mass=c.MASS_MERCURY, is_center=False)
        venus = o.Celestial_Body(x=-0.72*c.AU, y=0, radius=14, color=(153,102,0), mass=c.MASS_VENUS, is_center=False)
        earth = o.Celestial_Body(x=-1*c.AU, y=0, radius=15, color=(0,0,255), mass=c.MASS_EARTH, is_center=False)
        mars = o.Celestial_Body(x=-1.52*c.AU, y=0, radius=10, color=(250,30,30), mass=c.MASS_MARS, is_center=False)


        bodies = [sun, mercury, venus, earth, mars]

        pygame.display.update()

        # since all objects are placed on the y-axis at the start, their x-axis_velocity is equal to 0,
        # so their initial (and constant) velocity is just the y-axis_velocity 
        mercury.vel_y = mercury.initial_velocity(bodies)
        venus.vel_y = venus.initial_velocity(bodies)
        earth.vel_y = earth.initial_velocity(bodies)
        mars.vel_y = mars.initial_velocity(bodies)

        while run:
            clock.tick(60) 
            WIN.fill((0,0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            for body in bodies:
                if not body.is_center:
                    body.move(bodies)
                body.show(WIN)
            
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    GUI()