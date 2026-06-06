import pygame 
import math

class SingleBlaze():

    def __init__(self, x, y, direction):
        
        self.x = x
        self.y = y
        self.direction = direction

        print(f"single blaze launched in direction {self.direction}")

        self.rect = pygame.Rect(self.x,self.y,10,10)

        self.blaze_speed = 10

        self.blaze_color = (192,192,192)

    def move(self):

        if self.direction == 'right':
            self.x += self.blaze_speed
        elif self.direction == 'left':
            self.x-=self.blaze_speed
        elif self.direction == 'up':
            self.y-=self.blaze_speed
        elif self.direction == 'down':
            self.y += self.blaze_speed

        self.rect.topleft=(self.x,self.y)

    def draw(self,screen,camera_x,camera_y):
        pygame.draw.rect(screen,self.blaze_color,(self.rect.x-camera_x,self.rect.y-camera_y, 10 , 10))

class MultiBlaze():

    def __init__(self, x, y, direction, angle_offset):

        self.x = x
        self.y = y
        self.direction = direction
        self.angle_offset = angle_offset

        print(f"multi blaze launched at direction {self.direction} with angle offset {self.angle_offset}")

        self.rect = pygame.Rect(self.x,self.y,10,10)
        self.blaze_speed = 10
        self.blaze_color = (192,192,192)

        self.dx, self.dy = self.get_movement_vector(self.direction, self.angle_offset)

    def get_movement_vector(self, direction, angle_offset):
        
        direction_angles ={
            'up': -math.pi/2,
            'down': math.pi/2,
            'left':math.pi,
            'right':0
        }

        base_angle = direction_angles[direction]
        final_angle = base_angle+angle_offset

        dx=math.cos(final_angle)*self.blaze_speed
        dy=math.sin(final_angle)*self.blaze_speed

        if abs(angle_offset)==10:
            dx=-dx
            dy=-dy
        
        return dx,dy
    
    def move(self):

        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (self.x,self.y)

    def draw(self,screen,camera_x,camera_y):
        pygame.draw.rect(screen,self.blaze_color,(self.rect.x-camera_x,self.rect.y-camera_y,10,10))
