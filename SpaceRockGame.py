# Game involving space rocks
# By Casey Betts

# mustard sun by Martin Cee (softmartin) (c) copyright 2022 Licensed under a Creative Commons Attribution Noncommercial  (3.0) license. http://dig.ccmixter.org/files/softmartin/65383 Ft: subliminal
import math
import pygame
import random

from Calculations import (
    find_force,
    radar_coord_conversion,
    momentum,
    display_coord_conversion
    )
from config import *
from SpaceRock import *
from Player import *
from RadarPoint import *
from pygame.locals import *
from sys import exit



if not pygame.get_init():
    pygame.init()

class _Setup():
    "Provides functions needed to set up the game"

    def make_random_rock(self, ID):
        # returns a space rock of random mass and position
        mass = random.choice(MASSES) #random.randint(5,10)*1000000000000000
        x_position = random.randint(outer_left,outer_right)
        y_position = random.randint(outer_top, outer_bottom) #[10-random.randint(1,2),10-random.randint(1,2)]
        x_velocity = random.randint(-1,1)
        y_velocity = random.randint(-1,1)
        rand_rock = SpaceRock( mass, x_position, y_position, x_velocity, y_velocity, ID )
        return rand_rock

    def make_random_rocks(self, num):
        # Create a sprite group to contain random space rocks
        sprite_group = pygame.sprite.Group()
        for i in range(num):
            sprite_group.add(self.make_random_rock(i+1))
        return sprite_group

    def make_radar_points(self, num):
        sprite_group = pygame.sprite.Group()
        for i in range(num):
            point = RadarPoint(i+1)
            sprite_group.add(point)
        return sprite_group

class Game():
    # Contains the loop for running the game
    def __init__(self):
        # Create a display window
        self.screen = pygame.display.set_mode((winWidth,winHeight))
        # Create a clock to control frames per second
        self.clock = pygame.time.Clock()
        # Font
        self.font = pygame.font.Font(pygame.font.get_default_font(), 40)
        # Create Radar screen surface
        self.radar_screen = pygame.Surface(((outer_right-outer_left)*radar_reduction,(outer_bottom-outer_top)*radar_reduction))
        self.radar_screen.fill((20,20,20))
        self.radar_screen.set_alpha(128)
        # Create variable to store the number of rocks remaining
        self.remaining_rocks = len(rocks.sprites())
        # Import background music
        self.bg_music = pygame.mixer.Sound("audio/background_music.wav")

        # Create a variable for the screen column and row
        self.screen_col = 0
        self.screen_row = 0

        # Key down flag
        self.key_down_flag = False

    def update_screen_position(self, player_x, player_y):
        """Given the player's position, this determines the column and row of the screen on the map."""

        # Determine screen column
        if player_x < -2*winWidth:
            self.screen_col = -3
        elif player_x < -winWidth:
            self.screen_col = -2
        elif player_x < 0:
            self.screen_col = -1
        elif player_x < winWidth:
            self.screen_col = 0
        elif player_x < 2*winWidth:
            self.screen_col = 1
        elif player_x < 3*winWidth:
            self.screen_col = 2
        else:
            self.screen_col = 3

        # Determine screen column
        if player_y < -2*winHeight:
            self.screen_row = -3
        elif player_y < -winHeight:
            self.screen_row = -2
        elif player_y < 0:
            self.screen_row = -1
        elif player_y < winHeight:
            self.screen_row = 0
        elif player_y < 2*winHeight:
            self.screen_row = 1
        elif player_y < 3*winHeight:
            self.screen_row = 2
        else:
            self.screen_row = 3

    def run(self):

        # Play background music
        if music_on:
            self.bg_music.play(loops = -1)

        # Contains the loop to render the game and exit on quit event
        while True:

            # Loop through all the current pygame events in the queue
            for event in pygame.event.get():

                # Check if a key is currently pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.cleanup()
                    else:
                        # Change the key down flag to True
                        self.key_down_flag = True

                elif event.type == pygame.KEYUP:
                    # Reset the key down flag
                    self.key_down_flag = False

                elif event.type == pygame.QUIT:
                    self.cleanup()

            # Get the set of keys pressed
            pressed_keys = pygame.key.get_pressed()

            # Reset the background
            self.screen.fill('Black')

            # Check if any space rocks have collided with eachother
            for rock in rocks:
                rock_collision = pygame.sprite.spritecollideany(rock, rocks)
                if rock_collision.id != rock.id:
                    if abs(rock_collision.velocity[0] - rock.velocity[0]) < 1 and abs(rock_collision.velocity[1] - rock.velocity[1]) < 1:
                        if rock_collision.mass > rock.mass:
                            rock_collision.mass += rock.mass
                            rock_collision.change_size()
                            for point in point_group:
                                if point.id == rock_collision.id:
                                    point.change_size(rock_collision.mass)
                                if point.id == rock.id:
                                    point.kill()
                            rock.kill()

                        else:
                            rock.mass += rock_collision.mass
                            for point in point_group:
                                if point.id == rock_collision.id:
                                    point.kill()
                            rock_collision.kill()
                        self.remaining_rocks = len(rocks.sprites())
                    else:
                        rock_collision.velocity[0] *= collision_slow_percent
                        rock_collision.velocity[1] *= collision_slow_percent
                        rock.velocity[0] *= collision_slow_percent
                        rock.velocity[1] *= collision_slow_percent

            # Check if any space rocks have collided with the player
            collision_rock = pygame.sprite.spritecollide(blob,rocks, True)

            if collision_rock:
                # If so, then kill the space rock and add the rock's mass to the player mass
                print( collision_rock[0].mass )
                blob.mass += collision_rock[0].mass
                blob.velocity = [momentum(blob.mass,blob.velocity[0], collision_rock[0].mass, collision_rock[0].velocity[0])/2,
                                momentum(blob.mass,blob.velocity[1], collision_rock[0].mass, collision_rock[0].velocity[1])/2]
                for point in point_group:
                    if point.id == collision_rock[0].id:
                        point.kill()
                self.remaining_rocks = len(rocks.sprites())

            # Update player position and thrust group
            self.screen.blit(blob.surface, blob.update(all_sprites, self.key_down_flag, pressed_keys, self.screen_col, self.screen_row))

            # Update screen position
            self.update_screen_position(blob.rect.left,blob.rect.top)

            # Update space rock positions
            for entity in rocks:
                self.screen.blit(entity.surface, entity.update(all_sprites, self.screen_col, self.screen_row))

            # Update the radar point positions
            point_group.update(rocks, blob.rect.left, blob.rect.top)

            # Update thrust group
            blob.thrust_group.update()

            for sprite in blob.thrust_group:
                # Change coordinates based on the screen position
                thr_x = sprite.rect.left + (-self.screen_col*winWidth)
                thr_y = sprite.rect.top + (-self.screen_row*winHeight)

                # Blit the thrust sprite on the screen
                self.screen.blit(sprite.surface,(thr_x,thr_y))

            # Blit the radar screen on the window
            self.screen.blit(self.radar_screen,(radar_left,radar_top))

            screen_position = radar_coord_conversion( self.screen_col*winWidth,
                                        self.screen_row*winHeight,
                                        radar_reduction,
                                        radar_left,
                                        radar_top,
                                        outer_left,
                                        outer_top
                                        )
            pygame.draw.rect(
                            self.screen,
                            (40,40,40),
                            (   screen_position[0],
                                screen_position[1],
                                winWidth*radar_reduction,
                                winHeight*radar_reduction)
                            )

            # Draw the radar points on the screen
            for entity in point_group:
                self.screen.blit(entity.surface, entity.rect)

            # End the game when all space rocks are gone
            if not rocks.sprites():
                print("You Win!")
                self.cleanup()

            # Display the current mass of the player
            mass_text_surf = self.font.render(
                f'Current Mass: {math.trunc(blob.mass)} kg              Space Rocks Remaining: {self.remaining_rocks}',
                False, (64,64,64))
            self.screen.blit(mass_text_surf,(10,10))

            self.clock.tick(framerate)

            pygame.display.flip()

    def cleanup(self):
        pygame.quit()
        exit()
        print("cleanup complete")

if __name__ == "__main__":
    # Create the rocks and add them to a sprite group
    setup = _Setup()
    rocks = setup.make_random_rocks(number_of_rocks)
    # Create radar points and add them to a sprite group
    point_group = setup.make_radar_points(number_of_rocks)
    # Create radar point for the player
    player_point = RadarPoint(0)
    point_group.add(player_point)
    # Create the player sprite
    blob = Player(
                player_start_mass,
                player_start_pos_x,
                player_start_pos_y,
                player_start_velocity_x,
                player_start_velocity_y,
                player_start_size_x,
                player_start_size_y
                )
    # Sprite group for all sprites
    all_sprites = pygame.sprite.Group()
    for rock in rocks:
        all_sprites.add(rock)
    all_sprites.add(blob)
    # Sprite group just for the player
    player_group = pygame.sprite.Group()
    player_group.add(blob)

    # Create game object and run
    game = Game()
    game.run()
