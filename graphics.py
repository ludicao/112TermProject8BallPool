import pygame
import math

# Gameboard class
class Gameboard(object):
    
    
    
    # Initialize values for gameboard
    def __init__(self, x, y, width, height):        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.friction = 0.8
        self.color = (33, 137, 88)
    
        
    # Draw the game board
    def draw(self, screen):      
        pygame.draw.rect(screen, self.color, \
        (self.x, self.y, self.width, self.height), 0)
        
        
# Hole Class
class Hole(pygame.sprite.Sprite):
    
    radius = 25   # Constant for all holes
    color = (0, 0, 0)    # All holes are black
    
    # Init values:
    def __init__(self, x, y):
        super().__init__()
                
        # diameter of circle, also width and height of surface
        side = 2*Hole.radius 
        
        self.image = pygame.Surface((side, side))
        self.image.fill((33, 137, 88))
        self.image.set_colorkey((33, 137, 88))
        pygame.draw.circle(self.image, Hole.color,(Hole.radius, Hole.radius), \
                           Hole.radius, 0)
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        
# Cue class        
class Cue(pygame.sprite.Sprite):

    # Constant
    color = (176, 101, 34)
    length = 200
    distanceFromWhite = 30
    thickness = 4
    
    # Initialize values
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
     
    # Draw function
    def draw(self, screen):
        pygame.draw.lines(screen, Cue.color, False, \
        [(self.x1, self.y1), (self.x2, self.y2)], self.thickness)
        
        
# Class for guiding lines for cue stick to strike        
class GuideLines():
    
    gap = 20
    length = 40
    color = (255, 255, 255)
    extendingDist = 800
    thickness = 2
    
    def __init__(self, xStart, yStart, extendAngle):
        self.xStart = xStart
        self.yStart = yStart
        self.extendAngle = extendAngle

       
    def draw(self, screen):
        drawNum = self.extendingDist // (self.gap + self.length) + 1
        for i in range(drawNum):
            x1 = self.xStart - \
                 i*(self.length+self.gap)*math.cos(self.extendAngle)
            y1 = self.yStart + \
                 i*(self.length+self.gap)*math.sin(self.extendAngle)
            x2 = x1 + GuideLines.length*math.cos(self.extendAngle)
            y2 = y1 - GuideLines.length*math.sin(self.extendAngle)
            
            pygame.draw.lines(screen, self.color, False, \
                              [(x1, y1), (x2, y2)], self.thickness)
        
        
