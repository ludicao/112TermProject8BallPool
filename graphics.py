import pygame

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
    
    radius = 23    # Constant for all holes
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
    
    gap = 50
    length = 80
    color = (255, 255, 255)
    extendingDist = 800
    
    def __init__(self, x1, y1, extendAngle, relativePos):
        self.x1 = x1
        self.y1 = y1   
        self.extendAngle = extendAngle
        self.relativePos = relativePos
        
    #def posOfEndPoints(self, relativePos):
        
            
        
    def draw(self, screen):
        dist = distance(self.boardCornerx, self.boardCornery, self.x1, self.x2)
        drawNum = GuideLines.extendingDist // (GuideLines.gap + GuideLines.length) + 1
        
        
