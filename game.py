import time
import pygame
from obstacles import *

class AlienShooter():

    def __init__(self,window_width,window_height,world_width,world_height,fps,sound=False):
        
        self.window_width = window_width
        self.window_height = window_height
        self.world_width = world_width
        self.world_height = world_height

        self.chest = None
        self.energy_drop = None
        
        self.paused = False
        
        self.blaze_type = 'single'
        self.fire_mode = 'single'

        pygame.init()
        self.screen = pygame.display.set_mode((window_width,window_height))

        pygame.display.set_caption("Galaxy Apex")

        self.font = pygame.font.SysFont(None,36)

        self.clock = pygame.time.Clock()
        self.fps=fps

        self.walls = walls_1

        #TO DO: Define player

        self.background_color = (181,101,29) 
        self.wall_color = (1,50,32)
        self.border_color = (255,0,0)

        self.annocement_font = pygame.font.SysFont(None,100)

        self.blazers = []
        self.aliens = []

        self.alien_top_speed = 5
        self.level_goal = 5
        self.max_alien_count = 5
        self.level = 1
        self.sound = sound
    
    def fill_background(self):

        self.screen.fill(self.background_color)

        level_surface = self.font.render(f"Level : {self.level}", True, (0,0,0))
        self.screen.blit(level_surface, (10,60))

        pygame.display.flip()
        

    def step(self):

        print("Playing game....")
        self.fill_background()
        self.clock.tick(self.fps)
        