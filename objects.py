import pygame
import math
import constants as c

class Celestial_Body:
    def __init__(self, x, y, radius, color, mass, is_center):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.is_center = is_center

        self.orbit = []
        self.distance_to_sun = 0

        self.vel_x = 0
        self.vel_y = 0

    def show(self, window):
        scaled_points = []
        if len(self.orbit) >= 2:
            for point in self.orbit:
                x, y = point
                x = x * c.scale + c.WIDTH/2
                y = y * c.scale + c.HEIGHT/2
                scaled_points.append((x,y))

            pygame.draw.lines(window, (255,255,255), False, scaled_points, 1)

        coord_x = self.x * c.scale + c.WIDTH/2
        coord_y = self.y * c.scale + c.HEIGHT/2
        pygame.draw.circle(window, self.color, (coord_x, coord_y), self.radius)

    def acceleration(self, body):
        distance_x = body.x - self.x
        distance_y = body.y - self.y
        distance = math.sqrt(distance_x**2+distance_y**2)
        angle = math.atan2(distance_y, distance_x)
        acc_x = math.cos(angle)*c.G*body.mass/distance**2
        acc_y = math.sin(angle)*c.G*body.mass/distance**2
        return acc_x, acc_y

    def move(self, bodies):
        total_acc_x = 0
        total_acc_y = 0
        for body in bodies:
            if self == body:
                continue
            acc_x, acc_y = self.acceleration(body)
            total_acc_x += acc_x
            total_acc_y += acc_y

        self.vel_x += c.TIMESCALE*total_acc_x
        self.vel_y += c.TIMESCALE*total_acc_y

        self.x += c.TIMESCALE * self.vel_x
        self.y += c.TIMESCALE * self.vel_y

        self.orbit.append((self.x, self.y))
    
    # needed, since we're starting from a still frame of a constant motion, not from the beginning of the motion
    def initial_velocity(self, bodies):
        vel = 0
        for body in bodies:
            if self == body:
                continue
            distance_x = body.x - self.x
            distance_y = body.y - self.y
            distance = math.sqrt(distance_x**2+distance_y**2)
            vel += math.sqrt(c.G * body.mass / distance)
        return vel
    
