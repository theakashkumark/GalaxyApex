import time
import pygame
from obstacles import *
from spaceships import *
from utils import *
from blaze import *
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

        self.bg_image = pygame.transform.scale(pygame.image.load("images/background.jpg"), (self.world_width, self.world_height))

        #TO DO: Define player
        self.G_apex = GalaxyApex(self.world_width,self.world_height,walls_1)

        self.background_color = (181,101,29) 
        self.wall_color = (1,50,32)
        self.border_color = (255,0,0)

        self.annocement_font = pygame.font.SysFont(None,100)

        self.blazers = []
        self.drone = []

        self.multi_blaze_count = 10
        self.drone_top_speed = 5
        self.G_apex_score = 5
        self.level_goal = 5
        self.max_drone_count = 5
        self.level = 1
        self.sound = sound
        self.out_of_ammo_messaged_displayed = False
    
    def fill_background(self,camera_x,camera_y):
        self.screen.blit(self.bg_image,(0-camera_x,0-camera_y))

        level_surface = self.font.render(f"Level : {self.level}", True, (0,0,0))
        self.screen.blit(level_surface, (10,60))


    #firing mode or blazing mode
    def fire_single_blaze(self):
        blaze = SingleBlaze(self.G_apex.x,self.G_apex.y,self.G_apex.direction)
        self.blazers.append(blaze)

        #TODO : add sound
        
    def fire_multi_blaze(self):
        if self.multi_blaze_count>0:
            directions = [
                (self.G_apex.direction,0),
                (self.G_apex.direction,10),
                (self.G_apex.direction,-10)
            ]

            for direction,angle_offset in directions:
                blaze=MultiBlaze(self.G_apex.x,self.G_apex.y,direction,angle_offset)
                self.blazers.append(blaze)

            self.multi_blaze_count-=1
            self.out_of_ammo_messaged_displayed=False

            print('!bam bam bam')

            #TODO : add sound

        else:
            print("out of multi blaze ammo")
            self.out_of_ammo_messaged_displayed=True



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

        #TODO : walking sound

        new_G_apex_x = self.G_apex.x

        if keys[pygame.K_a]:
            new_G_apex_x-=self.G_apex.speed
            self.G_apex.direction = 'left'
        elif keys[pygame.K_d]:
            new_G_apex_x+=self.G_apex.speed
            self.G_apex.direction = 'right' 

        G_apex_rect = pygame.Rect(new_G_apex_x,self.G_apex.y,self.G_apex.size,self.G_apex.size)

        collision = check_collision(G_apex_rect,walls_1)

        if not collision and self.G_apex.x != new_G_apex_x and 0<=new_G_apex_x<=self.world_width-self.G_apex.size :
            self.G_apex.x = new_G_apex_x

        self.G_apex.rect = pygame.Rect(self.G_apex.x, self.G_apex.y, self.G_apex.size, self.G_apex.size)

        collision = False

        camera_x = self.G_apex.x - self.window_width // 2
        camera_y = self.G_apex.y - self.window_height // 2

        camera_x = max(0, min(camera_x, self.world_width - self.window_width))
        camera_y = max(0, min(camera_y, self.world_height - self.window_height))

        self.temp_drone=[]

        for dron in self.drone:
            if check_collision(dron.rect,self.blazers):
                blazer = get_collision(dron.rect,self.blazers)
                self.blazers.remove(blazer)

            elif check_collision(dron.rect,[self.G_apex]):
                self.G_apex_score-=1
            
            else:
                self.temp_drone.append(dron)

        self.drone=self.temp_drone

        for dron in self.drone:
            dron.move_towards_player(self.G_apex.x,self.G_apex.y,self.walls)


        print("Playing game....")

        self.fill_background(camera_x,camera_y)

        self.G_apex.draw(self.screen,camera_x,camera_y)

        #TODO : bullet logic
        for blaze in self.blazers:
            blaze.move()
            blaze.draw(self.screen,camera_x,camera_y)

            if check_collision(blaze.rect,walls_1):
                self.blazers.remove(blaze)

        for drone in self.drone:
            drone.draw(self.screen,camera_x,camera_y)
            

        #TODO : drone logic

        pygame.display.flip()

        self.clock.tick(self.fps)


        