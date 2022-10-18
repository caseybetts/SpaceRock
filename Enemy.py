# This file contains the Enemy class

import pygame

from Calculations import find_force
from config import *

from ThrustSprite import ThrustSprite

class Enemy(pygame.sprite.Sprite):
    """This is the enemy sprite"""
    def __init__(self, mass, x_size, y_size):
        super(Player,self).__init__()

        # Mass, Position and Velocity parameters initialized
        self.mass = mass
        self.velocity = [0,0]
        self.size = [x_size, y_size]
        self.id = 1000

        # Create pygame Surface
        self.surface = pygame.image.load("Graphics/GreenBlob.png")
        self.surface = pygame.transform.scale(self.surface, self.size)
        self.surface.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surface.get_rect( center = (1000,1000) )

        # Thrust sound and group
        self.thrust_sound = pygame.mixer.Sound(thrust_sound_location)
        self.thrust_sound.set_volume(.25)
        self.thrust_group = pygame.sprite.Group()
        self.percent_ejection = .002

        # Collision Sound
        self.collision_sound = pygame.mixer.Sound(gulp_sound_location)
        self.collision_sound.set_volume(.15)

        # Create radar point parameters
        self.radar_point_position = [0,0]
        self.radar_point_color = 'Yellow'
        self.radar_point_size = 2

    def thrust(self, direction):

        # Create a new thrust sprite and add it to the group
        ejected = ThrustSprite(self.rect.centerx,self.rect.centery,self.mass,direction)
        self.thrust_group.add(ejected)

        # Update the mass
        self.mass *= 1-self.percent_ejection

        # Play a sound
        self.thrust_sound.play()

        # Calculate and return the amount of force
        return self.mass*self.percent_ejection*thrust_acc

    def display(self, screen, screen_col, screen_row, win_width, win_height):

        # Blit the enemy to the screen
        screen.blit(self.surface,[
                        self.rect.left + (-screen_col*win_width),
                        self.rect.top + (-screen_row*win_height)])

        # Blit the radar point to the screen
        pygame.draw.rect(
                        screen,
                        self.radar_point_color,
                        (self.radar_point_position[0],
                          self.radar_point_position[1],
                          self.radar_point_size,
                          self.radar_point_size))

        # Blit the thrust group to the screen
        for sprite in self.thrust_group:
            sprite.display(
                            screen,
                            screen_col,



                            screen_row,
                            win_width,
                            win_height)

    # Move the sprite based on AI logic
    def update(self, all_sprites, key_down_flag, pressed_keys, screen, screen_col, screen_row, win_width, win_height, map_rect, radar_rect):

        x_thrust = 0
        y_thrust = 0

        # Calculate force on object
        force = find_force(all_sprites, self.rect[0], self.rect[1], self.mass, self.id)

        # Update acceleration
        acceleration_x = (force[0]+x_thrust)/(self.mass*framerate*framerate)
        acceleration_y = (force[1]+y_thrust)/(self.mass*framerate*framerate)

        # Update object's velocity
        self.velocity[0] += acceleration_x
        self.velocity[1] += acceleration_y

        # Find the displacement in position
        self.rect.move_ip(self.velocity[0],self.velocity[1])

        # Update the radar point
        self.radar_point_position = radar_coord_conversion(
                                                            self.rect.left,
                                                            self.rect.top,
                                                            RADAR_REDUCTION,
                                                            radar_rect,
                                                            map_rect)

        # Update thrust group
        self.thrust_group.update(
                                screen,
                                screen_col,
                                screen_row,
                                win_width,
                                win_height)


        self.display(screen, screen_col, screen_row, win_width, win_height)