import time
import pygame
from obstacles import *
from spaceships import *
from utils import *
import sys
import random

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
        self.G_apex = GalaxyApex(self.world_width,self.world_height,walls_1)

        self.background_color = (181,101,29) 
        self.wall_color = (1,50,32)
        self.border_color = (255,0,0)

        self.annocement_font = pygame.font.SysFont(None,100)

        self.blazers = []
        self.drone = []

        self.drone_top_speed = 5
        self.level_goal = 5
        self.max_drone_count = 5
        self.level = 1
        self.sound = sound
    
    def fill_background(self):
        self.screen.fill(self.background_color)

        level_surface = self.font.render(f"Level : {self.level}", True, (0,0,0))
        self.screen.blit(level_surface, (10,60))

        pygame.display.flip()

    #firing mode or blazing mode
    def fire_single_blaze(self):
        print("!bam")
    
    def fire_multi_blaze(self):
        print('!bam bam bam')

    def toggle_pause(self):
        #complete toggle pass method
        pass
        

    def step(self):
        for event in pygame.event.get():
            
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_TAB:
                    self.blaze_type = 'single' if self.blaze_type=='multi' else 'multi'
                    print(f'swtiched to {self.blaze_type}')
                elif event.key==pygame.K_SPACE:
                    if self.blaze_type=='single':
                        self.fire_single_blaze()
                    else:
                        self.fire_multi_blaze()
                elif event.key==pygame.K_ESCAPE:
                    self.toggle_pause()
                
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if self.blaze_type=='single':
                    self.fire_single_blaze()
                else:
                    self.fire_multi_blaze()
            
        if self.paused:
            return
        
        player_moved = False

        if len(self.drone)<self.max_drone_count and random.randint(0,100)<3:
            self.drone.append(AlienDrone(self.world_width,self.world_height,size=80,speed=random.randint(1,self.drone_top_speed)))


        keys = pygame.key.get_pressed()

        new_G_apex_x = self.G_apex.x

        if keys[pygame.K_a]:
            new_G_apex_x-=self.G_apex.speed
            self.G_apex.direction = 'left'
        elif keys[pygame.K_d]:
            new_G_apex_x+=self.G_apex.speed
            self.G_apex.direction = 'right' 

        G_apex_rect = pygame.Rect(new_G_apex_x,self.G_apex.y,self.G_apex.size,self.G_apex.size)

        collision = check_collision(G_apex_rect,walls_1)

        if not collision and self.G_apex.x != new_G_apex_x and 0<=new_G_apex_x<=self.world_width-new_G_apex_x :
            self.G_apex.x = new_G_apex_x

            #TODO : walking sound

        new_G_apex_y = self.G_apex.y

        if keys[pygame.K_w]:
            new_G_apex_y -= self.G_apex.speed
            self.G_apex.direction = 'up'
        elif keys[pygame.K_s]:
            new_G_apex_y += self.G_apex.speed
            self.G_apex.direction = 'down'

        G_apex_rect = pygame.Rect(self.G_apex.x,new_G_apex_y,self.G_apex.size,self.G_apex.size)

        collision = check_collision(G_apex_rect,walls_1)

        if not collision and new_G_apex_y != self.G_apex.y and 0<=new_G_apex_y<=self.world_height-self.G_apex.size:
            self.G_apex.y=new_G_apex_y

        self.G_apex.rect = pygame.Rect(self.G_apex.x, self.G_apex.y, self.G_apex.size, self.G_apex.size)

        camera_x = self.G_apex.x - self.window_width // 2
        camera_y = self.G_apex.y - self.window_height // 2

        camera_x = max(0, min(camera_x, self.world_width - self.window_width))
        camera_y = max(0, min(camera_y, self.world_height - self.window_height))


        print("Playing game....")

        self.fill_background()
        self.G_apex.draw(self.screen,camera_x,camera_y)
        pygame.display.flip()
        self.clock.tick(self.fps)


        