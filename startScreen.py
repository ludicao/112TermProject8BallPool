import pygame
import positions
import graphics
import pool


# Start Screen Class
class startScreen():
    
    startMode = True
    
    # Init function 
    def init(self):
        
        # Initialize gameboard and sprite groups
        self.boardWidth = self.width-2*self.margin
        self.boardHeight = self.height-3*self.margin
        self.gameboard = graphics.Gameboard(self.margin, self.margin, \
                                   self.boardWidth, self.boardHeight)
        self.ballGroup = pygame.sprite.Group() 
        self.holeGroup = pygame.sprite.Group()
        
        
        # Add holes to sprite group
        listPos = positions.holePositions(self.margin, \
        graphics.Border.innerMargin, self.boardWidth, self.boardHeight) 
                                          
        for pos in listPos:
            self.holeGroup.add(graphics.Hole(pos[0], pos[1]))
            
        # Initialize borders
        self.border = graphics.Border(self.width, \
                      self.height, self.margin, self.boardHeight)
        
        # Initialize button values                                  
        self.buttonColor = (51, 153, 255)
        self.buttonWidth = 100
        self.buttonHeight = 50
        self.xMin = self.width/2 - self.buttonWidth/2
        self.xMax = self.width/2 + self.buttonWidth/2
        self.yMin = self.height*0.45 - self.buttonHeight/2
        self.yMax = self.height*0.45 + self.buttonHeight/2
            
            
    # init values of the Pygame class
    def __init__(self, width=1000, height=640, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.margin = 40
        self.fps = fps
        self.title = title
        self.bgColor = 	(230, 230, 250)    # Lavendar
        pygame.init()
     
    # Draw the welcome text
    def drawText(self, screen):
        self.font = pygame.font.Font('cmunti.ttf', 30)
        text = self.font.render('Welcome to the Game of Pool!', True, (0, 0, 0))
        screen.blit(text, (self.width/2 - text.get_rect().width/2, \
        self.height/3 - text.get_rect().height/2))
    
    # Draw the start button    
    def drawButtons(self, screen):
        pygame.draw.rect(screen, self.buttonColor,
        (self.xMin, self.yMin, self.buttonWidth, self.buttonHeight))
        self.font = pygame.font.Font('cmunti.ttf', 15)
        text = self.font.render('Press to Start!', True, (0, 0, 0))
        
        yDist = self.yMax - self.yMin
        yPos = self.yMax - yDist/2 - text.get_rect().height/2
        screen.blit(text, (self.width/2 - text.get_rect().width/2, yPos))
        
    # Display the drawings    
    def redrawAll(self, screen):
        self.gameboard.draw(screen)
        self.border.draw(screen)
        self.holeGroup.draw(screen)
        self.drawText(screen)
        self.drawButtons(screen)
    
    # If cursor is above button, button changes color    
    def mouseMotion(self):
        cursorX = pygame.mouse.get_pos()[0]
        cursorY = pygame.mouse.get_pos()[1]
        if cursorX > self.xMin and cursorX < self.xMax and \
        cursorY < self.yMax and cursorY > self.yMin:
            self.buttonColor = (204, 229, 255)
        else:
            self.buttonColor = (51, 153, 255)
    
    # If mouse if pressed on button, continue to start mode         
    def mousePressed(self):
        cursorX = pygame.mouse.get_pos()[0]
        cursorY = pygame.mouse.get_pos()[1]
        
        if cursorX > self.xMin and cursorX < self.xMax and \
        cursorY < self.yMax and cursorY > self.yMin:
            pool.Pygame().run()
    
    # Run function         
    def run(self):
    
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
    
        # stores all the keys currently being held down
        self._keys = dict()
    
        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed()
                elif (event.type == pygame.MOUSEMOTION and \
                event.buttons == (0, 0, 0)):
                    self.mouseMotion()
                elif event.type == pygame.QUIT:
                    playing = False
                    
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()   
            
        pygame.quit()
                    
                            
        
    
    