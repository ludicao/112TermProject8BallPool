import pygame

def checkType(boolIsFull, display1):
    if boolIsFull == False:
        if display1 == True:
            return ['striped', 'solid']
        else:
            return ['solid', 'striped']
    else:
        if display1 == True:
            return ['solid', 'striped']
        else:
            return ['striped', 'solid']
    


class Player():
    
    def __init__(self, type, num):
        self.type = type
        self.num = num
        
    def draw(self, screen, screenWidth, margin):
        self.font = pygame.font.Font('cmunti.ttf', 30)
        text = self.font.render('Player %s: %s' % (str(self.num), self.type), \
               True, (0, 0, 0))
               
        x = screenWidth/3
        y = 0
        
        screen.blit(text, (x,y))

    @ staticmethod
    def drawNone(screen, screenWidth, margin, bool):
        font = pygame.font.Font('cmunti.ttf', 30)
        if bool:
            text = font.render('Player 1', True, (0, 0, 0))
        else:
            text = font.render('Player 2', True, (0, 0, 0))
            
        x = screenWidth/5*2
        y = 0
        
        screen.blit(text, (x,y))

    
    
        

        
        
    