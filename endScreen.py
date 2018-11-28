import pygame
import positions
import graphics
import pool
import startScreen

class endScreen():
    
    # Init function 
    def init(self):
        
        # Initialize button values                                  
        self.buttonColor1 = (51, 153, 255)
        self.buttonColor2 = (51, 153, 255)
        self.buttonWidth = 100
        self.buttonHeight = 40
        
        if self.currDisplay:
            self.player = 'Player 1'
        else:
            self.player ='Player 2'
            
        if self.bool:
            self.currPlayerWins = True
            self.xMin = self.width/2 - self.buttonWidth/2
            self.xMax = self.width/2 + self.buttonWidth/2
            self.yMin = self.height*0.45 - self.buttonHeight/2
            self.yMax = self.height*0.45 + self.buttonHeight/2
        else:
            self.currPlayerWins = False
            self.xMin = self.width/2 - self.buttonWidth/2
            self.xMax = self.width/2 + self.buttonWidth/2
            self.yMin = self.height*0.5 - self.buttonHeight/2
            self.yMax = self.height*0.5 + self.buttonHeight/2
 
        self.x2Min = self.xMin
        self.x2Max = self.xMax
        self.y2Min = self.yMin + self.buttonHeight + 20
        self.y2Max = self.yMax + self.buttonHeight + 20
            
            
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
        
        
            
            
    # init values of the Pygame class
    def __init__(self, currDisplay, bool, width=1000, \
    height=640, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.margin = 40
        self.fps = fps
        self.title = title
        self.bgColor = (230, 230, 250)    # Lavendar
        self.currDisplay = currDisplay
        self.bool = bool
        pygame.init()
        
    # Draw the endScreen text
    def drawText(self, screen):
        self.font = pygame.font.Font('cmunti.ttf', 30)
        if self.player == 'Player 1' and self.currPlayerWins:
            text = self.font.render('Congrats! %s Wins' % \
            self.player1.title(), True, (0, 0, 0))
            screen.blit(text, (self.width/2 - text.get_rect().width/2, \
            self.height/3 - text.get_rect().height/2))

        elif self.player == 'Player 1' and not self.currPlayerWins:
            text = self.font.render('Uh oh! 8-Ball Striken', True, (0, 0, 0))
            text2 = self.font.render('%s Wins!' % self.player2.title(), True, (0, 0, 0))
            screen.blit(text, (self.width/2 - text.get_rect().width/2, \
            self.height/3 - text.get_rect().height/2))
            screen.blit(text2, (self.width/2 - text2.get_rect().width/2, \
            self.height/3 + text2.get_rect().height))
            
        elif self.player == 'Player 2' and not self.currPlayerWins:
            text = self.font.render('Uh oh! 8-Ball Striken', True, (0, 0, 0))
            text2 = self.font.render('%s Wins!' % self.player1.title(), True, (0, 0, 0))
            screen.blit(text, (self.width/2 - text.get_rect().width/2, \
            self.height/3 - text.get_rect().height/2))
            screen.blit(text2, (self.width/2 - text2.get_rect().width/2, \
            self.height/3 + text2.get_rect().height))
            
        elif self.player == 'Player 2' and self.currPlayerWins:
            text = self.font.render('Congrats! % Wins' % self.player2.title(), True, (0, 0, 0))
            screen.blit(text, (self.width/2 - text.get_rect().width/2, \
            self.height/3 - text.get_rect().height/2))
     
    
    # Draw the endScreen buttons 'back' and 'play again'    
    def drawButtons(self, screen):
        pygame.draw.rect(screen, self.buttonColor1,
        (self.xMin, self.yMin, self.buttonWidth, self.buttonHeight))
        
        pygame.draw.rect(screen, self.buttonColor2, 
        (self.x2Min, self.y2Min, self.buttonWidth, self.buttonHeight))

        
        self.font = pygame.font.Font('cmunti.ttf', 15)
        text = self.font.render('Back', True, (0, 0, 0))
        yDist = self.yMax - self.yMin
        yPos = self.yMax - yDist/2 - text.get_rect().height/2
        screen.blit(text, (self.width/2 - text.get_rect().width/2, yPos))
        
        text2 = self.font.render('Play Again!', True, (0,0,0))
        yPosNew = self.y2Max - yDist/2 - text2.get_rect().height/2
        screen.blit(text2, (self.width/2 - text2.get_rect().width/2, yPosNew))
    
    
    # Draw objects on screen    
    def redrawAll(self, screen):
        self.gameboard.draw(screen)
        self.border.draw(screen)
        self.holeGroup.draw(screen)
        self.drawText(screen)
        self.drawButtons(screen)
        
    # If cursor is above button, button changes color    
    def mouseMotion(self):
        # Back button
        cursorX = pygame.mouse.get_pos()[0]
        cursorY = pygame.mouse.get_pos()[1]
        if cursorX > self.xMin and cursorX < self.xMax and \
        cursorY < self.yMax and cursorY > self.yMin:
            self.buttonColor1 = (204, 229, 255)
        else:
            self.buttonColor1 = (51, 153, 255)
        
        # Play again button    
        if cursorX > self.x2Min and cursorX < self.x2Max and \
        cursorY < self.y2Max and cursorY> self.y2Min:
            self.buttonColor2 = (204, 229, 255)
        else:
            self.buttonColor2 = (51, 153, 255)
    
    # If mouse if pressed on button, continue to start mode or play mode        
    def mousePressed(self):
        cursorX = pygame.mouse.get_pos()[0]
        cursorY = pygame.mouse.get_pos()[1]
        
        # Return to start mode
        if cursorX > self.xMin and cursorX < self.xMax and \
        cursorY < self.yMax and cursorY > self.yMin:
            startScreen.startScreen().run()
        
        # Return to play mode    
        if cursorX > self.x2Min and cursorX < self.x2Max and \
        cursorY < self.y2Max and cursorY> self.y2Min:
            pool.Pygame().run()
            
    # Run function         
    def run(self, player1, player2):
    
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
    
        # stores all the keys currently being held down
        self._keys = dict()
    
        # call game-specific initialization
        self.init()
        self.player1 = player1
        self.player2 = player2
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
            
            