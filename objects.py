import pygame
import math
import constants as c

class Celestial_Body:
    def __init__(self, x, y, radius, color, mass, is_center, is_sun, list, scale, name, offset_x, offset_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.is_center = is_center
        self.is_sun = is_sun
        self.scale = scale
        self.name = name
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.coord_x = 0
        self.coord_y = 0

        self.orbit = []
        self.distance_to_sun = 0

        self.vel_x = 0
        self.vel_y = 0

        list.append(self)

    def show(self, window):
        scaled_points = []
        if len(self.orbit) >= 2:
            for point in self.orbit:
                x, y = point
                x = x * self.scale + c.WIDTH/2 + self.offset_x
                y = y * self.scale + c.HEIGHT/2 + self.offset_y
                scaled_points.append((x,y))

            pygame.draw.lines(window, (255,255,255), False, scaled_points, 1)

        self.coord_x = self.x * self.scale + c.WIDTH/2 + self.offset_x
        self.coord_y = self.y * self.scale + c.HEIGHT/2 + self.offset_y
        pygame.draw.circle(window, self.color, (self.coord_x, self.coord_y), self.radius)

    def distance(self, body):
        distance_x = body.x - self.x
        distance_y = body.y - self.y
        distance = math.sqrt(distance_x**2+distance_y**2)
        return distance_x, distance_y, distance
    
    def acceleration(self, body):
        distance_x, distance_y, distance = self.distance(body)
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
            if body.is_sun:
                _, _, self.distance_to_sun = self.distance(body)
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