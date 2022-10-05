# This file contains the Game_Setup class

import pygame
import random

from config import *
from SpaceRock import *
from RadarPoint import *

class Game_Setup():
    "Provides functions needed to set up the game"

    def make_random_rock(self, ID, x_bound, y_bound):
        # returns a space rock of random mass and position
        mass = random.choice(MASSES) #random.randint(5,10)*1000000000000000
        x_position = random.randint(x_bound[0], x_bound[1])
        y_position = random.randint(y_bound[0], y_bound[1]) #[10-random.randint(1,2),10-random.randint(1,2)]
        x_velocity = random.randint(rock_start_velocity[0],rock_start_velocity[1])
        y_velocity = random.randint(rock_start_velocity[0],rock_start_velocity[1])
        rand_rock = SpaceRock( mass, x_position, y_position, x_velocity, y_velocity, ID )
        return rand_rock

    def make_random_rocks(self, num, x_bound, y_bound):
        # Create a sprite group to contain random space rocks
        sprite_group = pygame.sprite.Group()
        for i in range(num):
            sprite_group.add(self.make_random_rock(i+1, x_bound, y_bound))
        return sprite_group

    def make_radar_points(self, num):
        sprite_group = pygame.sprite.Group()
        for i in range(num):
            point = RadarPoint(i+1)
            sprite_group.add(point)
        return sprite_group
