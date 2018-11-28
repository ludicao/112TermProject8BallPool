import pygame
import positions
import graphics
import pool
import text
import string


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
        
        # Initialize name box
        self.name1 = ''
        self.name2 = ''
        self.player1 = text.nameBox('Player 1', self.yMax + 10, \
                        self.width, False, self.name1, False)
        self.player2 = text.nameBox('Player 2', self.yMax + 70, \
                        self.width, False, self.name2, False)
        
        # Range coordianates of name box
        self.xMinBox1 = self.player1.x
        self.yMinBox1 = self.player1.startYBox()
        self.xMaxBox1 = self.player1.width + self.xMinBox1
        self.yMaxBox1 = self.player1.heightTextBox() + self.yMinBox1
        
        self.xMinBox2 = self.player2.x
        self.yMinBox2 = self.player2.startYBox()
        self.xMaxBox2 = self.player2.width + self.xMinBox2
        self.yMaxBox2 = self.player2.heightTextBox() + self.yMinBox2
        
        # Bool values indicating whether the name box is clicked on
        self.text1 = False
        self.text2 = False
        
        # Dictionary indicating whether both names are entered
        self.namesEntered = dict()

        
            
            
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
        self.player1.draw(screen)
        self.player2.draw(screen)
  
    
    # If cursor is above button, button changes color    
    def mouseMotion(self):
        cursorX = pygame.mouse.get_pos()[0]
        cursorY = pygame.mouse.get_pos()[1]
        if cursorX > self.xMin and cursorX < self.xMax and \
        cursorY < self.yMax and cursorY > self.yMin:
            self.buttonColor = (204, 229, 255)
        else:
            self.buttonColor = (51, 153, 255)
 

 
    
    # Mouse press functions   
    def mousePressed(self):
        cursorX = pygame.mouse.get_pos()[0]
        cursorY = pygame.mouse.get_pos()[1]
        
        # Mouse is pressed on start button 
        if cursorX > self.xMin and cursorX < self.xMax and \
        cursorY < self.yMax and cursorY > self.yMin:
            
            # If both players are entered, continue to start mode
            if (self.namesEntered == {'Player 1': True, "Player 2": True} \
            or self.namesEntered == {'Player 1': True, "Player 2": False}) and \
            self.player1.textName:
                player1 = self.player1.textName
                player2 = self.player2.textName
                pool.Pygame().run(player1.title(), player2.title())
        
        # Mouse is pressed on player 1 name entry box    
        elif cursorX > self.xMinBox1 and cursorX < self.xMaxBox1 and \
        cursorY < self.yMaxBox1 and cursorY > self.yMinBox1:
            
            # If player 1 name box is entered before pressing 'return' on 
            # player 2, automatically presses return for player 2
            if self.text2:
                self.player2 = text.nameBox('Player 2', self.yMax + 70, \
                                self.width, True, self.name2, False)
                self.text1 = False
                self.namesEntered["Player 2"] = True
                    
            
            # Enter 'pressed' condition into dictionary
            if 'Player 1' not in self.namesEntered:
                self.namesEntered["Player 1"] = False
            self.namesEntered["Player 1"] = False
            self.text1 = True 
            self.player1 = text.nameBox('Player 1', self.yMax + 10, \
                            self.width, True, self.name1, True)
        
        # Mouse is pressed on player 2 name entry box                            
        elif cursorX > self.xMinBox2 and cursorX < self.xMaxBox2 and \
        cursorY < self.yMaxBox2 and cursorY > self.yMinBox2:
            
            # If player 1 name box is entered before pressing 'return' on 
            # player 2, automatically presses return for player 2
            if self.text1:
                self.player1 = text.nameBox('Player 1', self.yMax + 10, \
                                self.width, True, self.name1, False)
                self.text1 = False
                self.namesEntered["Player 1"] = True
            
            # Enter 'pressed' condition into dictionary        
            if 'Player 2' not in self.namesEntered:
                self.namesEntered["Player 2"] = False
            self.namesEntered["Player 2"] = False
            self.text2 = True 
            self.player2 = text.nameBox('Player 2', self.yMax + 70, \
                            self.width, True, self.name2, True)
        
        # Mouse is pressed out of bounds
        else:
            self.text1 = False
            self.text2 = False
            
            
            
    
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
                
                # If player 1 entry box has been clicked on
                if self.text1:
                    if event.type == pygame.KEYDOWN:
                        # Enter player 1 name
                        letter = pygame.key.name(event.key)
                        if letter in string.ascii_letters:
                            self.name1 += letter
                            self.player1 = text.nameBox('Player 1', \
                            self.yMax + 10, self.width, True, self.name1, True)
                        elif letter == 'backspace':
                            self.name1 = self.name1[:-1]
                            self.player1 = text.nameBox('Player 1', \
                            self.yMax + 10, self.width, True, self.name1, True)
                        # Finished entering name when 'return' is pressed
                        elif letter == 'return':
                            self.namesEntered['Player 1'] = True
                            self.text1 = False
                            self.player1 = text.nameBox('Player 1', self.yMax \
                            + 10, self.width, True, self.name1, False)

                # If player 2 entry box has been clicked on
                elif self.text2:
                    if event.type == pygame.KEYDOWN:
                        # Enter player 2 name
                        letter = pygame.key.name(event.key)
                        if letter in string.ascii_letters:
                            self.name2 += letter
                            self.player2 = text.nameBox('Player 2', \
                            self.yMax + 70, self.width, True, self.name2, True)
                        elif letter == 'backspace':
                            self.name20 = self.name1[:-1]
                            self.player2 = text.nameBox('Player 2', \
                            self.yMax + 10, self.width, True, self.name2, True)
                        # Finished entering name when 'return' is pressed
                        elif letter == 'return':
                            self.namesEntered['Player 2'] = True
                            self.text2 = False
                            self.player2 = text.nameBox('Player 2', self.yMax \
                            + 70, self.width, True, self.name2, False)
                            
                
       
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()   
            
        pygame.quit()
                    
# Run the game
def main():
    startMode = startScreen()
    startMode.run()

if __name__ == '__main__':
    main()
                               
        
    
    