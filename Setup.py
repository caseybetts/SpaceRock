# This file contains the Game_Setup class

import pygame
import random

from config import *
from Enemy import *
from SpaceRock import *
from RadarPoint import *

class Game_Setup():
    """Provides functions needed to set up the game"""

    def print_sprite(self, sprite):
        """Prints the attributes of the sprite"""
        print("id=", sprite.id,
                "\nmass=", sprite.mass)

    def enemy_generator(self, enemy_specs):
        """ Produces a group of enemies of the given specs. The enemy_specs argument
        should be a list of lists like [[quantity, mass, size], ...]"""

        sprite_group = pygame.sprite.Group()

        i = 1001

        for group in enemy_specs:
            for j in range(group[0]):
                sprite_group.add(self.make_enemy(i, group[1], group[2]))
                i += 1

        return sprite_group

    def make_enemy(self, id, mass, size, position = None, velocity = None):
        """ Returns an enemy sprite """

        if position == None:
            position = [int(random.gauss(500,1000)),
                        int(random.gauss(500,1000))]

        if velocity == None:
            velocity = [random.randint(-1,1),
                        random.randint(-1,1)]

        return Enemy(id, mass, size, position, velocity)

    def rock_generator(self, rock_specs, color, rock_id):
        """Produces a group of rocks of the specified sizes.
        The rock_specs argument should be a list of lists like [ [quantity, rock size],...]
        color should be "Brown" or "Grey"
        rock_id should be the highest id currently in existance"""

        # Create a sprite group to contain the rocks
        sprite_group = pygame.sprite.Group()

        i = rock_id + 1

        for size_group in rock_specs:
            for j in range(size_group[0]):
                sprite_group.add(self.make_random_rock(i, color, size_group[1]))
                i+=1
        print("Returning rock group", color)
        return sprite_group

    def make_rock(self, id, mass, color, position = None, velocity = None):
        """Returns one SpaceRock object
        If random is True, then provide the range """

        if position == None:
            position = [int(random.gauss(ROCK_LOWER_GAUSS_X, ROCK_UPPER_GAUSS_X)),
                        int(random.randint(-4*location[0], location[1]))]

        if velocity == None:
            velocity = [random.randint(ROCK_START_VELOCITY[0],ROCK_START_VELOCITY[1]),
                        random.randint(ROCK_START_VELOCITY[0],ROCK_START_VELOCITY[1])]

        return SpaceRock( id, mass, color, position[0], position[1], velocity[0], velocity[1])

    def make_random_rock(self, id, color, mass = None):
        """ returns a space rock of random mass and position.
            The range controling the position is set in the config file """

        # If a mass is not given then choose a random mass from the list
        if mass == None:
            mass = random.choice(MASSES)

        x_position = random.randint(ROCK_LOWER_GAUSS_X, ROCK_UPPER_GAUSS_X)
        y_position = random.randint(ROCK_LOWER_GAUSS_Y, ROCK_UPPER_GAUSS_Y)
        x_velocity = random.randint(ROCK_START_VELOCITY[0],ROCK_START_VELOCITY[1])
        y_velocity = random.randint(ROCK_START_VELOCITY[0],ROCK_START_VELOCITY[1])

        return SpaceRock( id, mass, color, x_position, y_position, x_velocity, y_velocity)

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


if __name__ == "__main__":

    setup = Game_Setup()
    my_sprites = setup.rock_generator([[500,3], [200,10], [100, 20]], "Grey")

    for sprite in my_sprites:
        setup.print_sprite(sprite)
