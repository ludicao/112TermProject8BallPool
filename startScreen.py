#############################
# This file runs the start screen of the game. It is also the main  client file
# of the program. It responds to user interaction through detecting whenter 
# the user has clicked on a button, and switches to different splash screens 
# accordingly. It also displays different messages depending on the different 
# end game situations for the users.
#############################


import pygame
import positions
import graphics
import pool
import text
import string

import socket
import threading
from queue import Queue



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
        self.buttonColor2 = (51, 153, 255)
        self.buttonColor3 = (255, 76, 76)
        self.buttonWidth = 100
        self.buttonHeight = 50
        self.xMin = self.width/2 - self.buttonWidth/2
        self.xMax = self.width/2 + self.buttonWidth/2
        self.yMin = self.height*0.4 - self.buttonHeight/2
        self.yMax = self.height*0.4 + self.buttonHeight/2
        
        # Initialize name box
        self.name1 = ''
        self.name2 = ''
        self.player1 = text.nameBox('Player 1', self.yMax + 10, \
                        self.width, False, self.name1, False)
        self.player2 = text.nameBox('Player 2', self.yMax + 70, \
                        self.width, False, self.name2, False)
        
        # Range coordinates of name box
        self.xMinBox1 = self.player1.x
        self.yMinBox1 = self.player1.startYBox()
        self.xMaxBox1 = self.player1.width + self.xMinBox1
        self.yMaxBox1 = self.player1.heightTextBox() + self.yMinBox1
        
        self.xMinBox2 = self.player2.x
        self.yMinBox2 = self.player2.startYBox()
        self.xMaxBox2 = self.player2.width + self.xMinBox2
        self.yMaxBox2 = self.player2.heightTextBox() + self.yMinBox2
        
        #Range coordinates of high score box
        self.xStartB = self.width/2 - self.buttonWidth/2
        self.yStartB = self.yMaxBox2 + 15
        
        # Bool values indicating whether the name box is clicked on
        self.text1 = False
        self.text2 = False
        
        # Dictionary indicating whether both names are entered
        self.namesEntered = dict()
        
        self.highScoreAppears = False

        # Values for exit button of high score board
        self.exitH = 15
        self.exitW = 30        
        self.exitX = self.width*0.35 + self.width*0.3 - self.exitW - 2
        self.exitY = (self.height-self.margin)*0.2 + 2
        
        # Bool values for preventing multi-player conflict controling of board 
        self.typed = None
        self.curr1 = True
        
        msg = 'atStart\n'
        self.server.send(msg.encode())
        
            
            
    # init values of the Pygame class
    def __init__(self, width=1000, height=640, fps=50, title="112 Pool Game"):
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
        self.height*0.3 - text.get_rect().height/2))



    
    # Draw the start button    
    def drawButtons(self, screen):
        pygame.draw.rect(screen, self.buttonColor,
        (self.xMin, self.yMin, self.buttonWidth, self.buttonHeight))
        self.font = pygame.font.Font('cmunti.ttf', 15)
        text = self.font.render('Press to Start!', True, (0, 0, 0))
        
        yDist = self.yMax - self.yMin
        yPos = self.yMax - yDist/2 - text.get_rect().height/2
        screen.blit(text, (self.width/2 - text.get_rect().width/2, yPos))
        
    # Draw the high score button
    def scoreButton(self, screen):
        pygame.draw.rect(screen, self.buttonColor2, (self.xStartB, self.yStartB, \
        self.buttonWidth, self.buttonHeight))
        
        font = pygame.font.Font('cmunti.ttf', 15)
        text = font.render('High Scores', True, (0, 0, 0))
        screen.blit(text, (self.width/2 - text.get_rect().width/2, \
        self.yStartB + self.buttonHeight/2 - text.get_rect().height/2))
        
    # Draw the high score board    
    def highScoreBox(self, screen):
        
        xStart = self.width*0.35
        yStart = (self.height-self.margin)*0.2
        width = self.width*0.3
        height = (self.height - self.margin)*0.6
        
        pygame.draw.rect(screen, (255,228,196), (xStart, yStart, \
        width, height), 0)
        
        pygame.draw.rect(screen, self.buttonColor3, (self.exitX, \
        self.exitY, self.exitW, self.exitH), 0)
        
        font = pygame.font.Font('cmunti.ttf', 10)
        exitText = font.render('Exit', True, (0, 0, 0))
        xText = xStart+width-2-self.exitW/2 - exitText.get_rect().width/2 
        yText = yStart+2+self.exitH/2 - exitText.get_rect().height/2
        screen.blit(exitText, (xText, yText))
        
        wordSpace = 15
        
        
        font = pygame.font.Font('cmunti.ttf', 30)
        title = font.render('High Score Board', True, (0, 0, 0))
        screen.blit(title, (self.width/2 - title.get_rect().width/2, \
            yStart + self.exitH + 10))
            
        titleH = title.get_rect().height
        
        font2 = pygame.font.Font('cmunti.ttf', 20)
        testSize = font2.render('High Score Board', True, (0, 0, 0))
        lineH = testSize.get_rect().height
        
        # Read highScore text and display them on high score board
        listNames = text.readScores('highScore.txt')
        y = yStart + 10 + titleH + wordSpace
        x = xStart + 5
        if listNames != ['']:
            for i in range(len(listNames)):
                yEach = y + i*(lineH + wordSpace)
                nameScore = listNames[i].split()
                lineMsg = font2.render(nameScore[0].title() + ' ' + \
                nameScore[1], True, (0,0,0))
                screen.blit(lineMsg, (x, yEach))


    # Display the drawings    
    def redrawAll(self, screen):
        self.gameboard.draw(screen)
        self.border.draw(screen)
        self.holeGroup.draw(screen)
        self.drawText(screen)
        self.drawButtons(screen)
        self.player1.draw(screen)
        self.player2.draw(screen)
        self.scoreButton(screen)
        if self.highScoreAppears:
            self.highScoreBox(screen)
  
    
    # If cursor is above button, button changes color    
    def mouseMotion(self):
        cursorX = pygame.mouse.get_pos()[0]
        cursorY = pygame.mouse.get_pos()[1]
        if cursorX > self.xMin and cursorX < self.xMax and \
        cursorY < self.yMax and cursorY > self.yMin:
            self.buttonColor = (204, 229, 255)
        else:
            self.buttonColor = (51, 153, 255)
        if cursorX > self.xStartB and cursorX < self.xStartB + self.buttonWidth\
        and cursorY < self.yStartB + self.buttonHeight and \
        cursorY > self.yStartB:
            self.buttonColor2 = (204, 229, 255)
        else:
            self.buttonColor2 = (51, 153, 255)
            
        if self.highScoreAppears:
            if cursorX > self.exitX and cursorX < self.exitX+self.exitW and \
            cursorY > self.exitY and cursorY < self.exitY+self.exitH:
                self.buttonColor3 = (255, 178, 178)
            else:
                self.buttonColor3 = (255, 76, 76)
            
            
    # Mouse press functions   
    def mousePressed(self):
        cursorX = pygame.mouse.get_pos()[0]
        cursorY = pygame.mouse.get_pos()[1]
        
        # Mouse is pressed on start button 
        if cursorX > self.xMin and cursorX < self.xMax and \
        cursorY < self.yMax and cursorY > self.yMin:
            
            # If both players are entered, continue to start mode
            if self.namesEntered == {'Player 1': True, "Player 2": True}:
                player1 = self.player1.textName
                player2 = self.player2.textName

                # Player 1 presses the start button
                if self.curr1:            
                    msg ='gameStarts byPlay1\n'
                    self.server.send(msg.encode())
                    pool.main(player1.title(), player2.title(), True)
                else:
                    msg ='gameStarts byPlay2\n'
                    self.server.send(msg.encode())
                    pool.main(player1.title(), player2.title(), False)
                    
                    
            

                
        
        # Mouse is pressed on player 1 name entry box    
        elif cursorX > self.xMinBox1 and cursorX < self.xMaxBox1 and \
        cursorY < self.yMaxBox1 and cursorY > self.yMinBox1 and self.curr1:
                   
            
            # Enter 'pressed' condition into dictionary
            if 'Player 1' not in self.namesEntered:
                self.namesEntered["Player 1"] = False
            self.namesEntered["Player 1"] = False
            self.text1 = True 
            self.player1 = text.nameBox('Player 1', self.yMax + 10, \
                            self.width, True, self.name1, True)
        
        # Mouse is pressed on player 2 name entry box                            
        elif cursorX > self.xMinBox2 and cursorX < self.xMaxBox2 and \
        cursorY < self.yMaxBox2 and cursorY > self.yMinBox2 and not self.curr1:
 
            # Enter 'pressed' condition into dictionary        
            if 'Player 2' not in self.namesEntered:
                self.namesEntered["Player 2"] = False
            self.namesEntered["Player 2"] = False
            self.text2 = True 
            self.player2 = text.nameBox('Player 2', self.yMax + 70, \
                            self.width, True, self.name2, True)
                            
        # Mouse presses on high score box                    
        elif cursorX > self.xStartB and cursorX < self.xStartB + self.buttonWidth\
        and cursorY < self.yStartB + self.buttonHeight and \
        cursorY > self.yStartB:
            self.highScoreAppears = True
        
        # Exit high score board    
        if self.highScoreAppears:
            if cursorX > self.exitX and cursorX < self.exitX+self.exitW and \
            cursorY > self.exitY and cursorY < self.exitY+self.exitH:
                self.highScoreAppears = False
    
        
    
    # Run function         
    def run(self, serverMsg, server):
    
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
    
        # stores all the keys currently being held down
        self._keys = dict()
    
        self.serverMsg = serverMsg
        self.server = server
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
                            self.typed = 'keyword'
                        elif letter == 'backspace':
                            self.name1 = self.name1[:-1]
                            self.player1 = text.nameBox('Player 1', \
                            self.yMax + 10, self.width, True, self.name1, True)
                            self.typed = 'keyword'
                            
                        # Finished entering name when 'return' is pressed
                        elif letter == 'return':
                            self.namesEntered['Player 1'] = True
                            self.text1 = False
                            self.player1 = text.nameBox('Player 1', self.yMax \
                            + 10, self.width, True, self.name1, False)
                            self.typed = 'return'
                            
                        if self.typed == 'keyword':
                            msg = 'player1Typed %s\n' % self.name1
                            self.server.send(msg.encode())
                            
                        elif self.typed == 'return':
                            msg = 'player1Entered %s\n' % self.name1
                            self.server.send(msg.encode())
                            
                    self.typed = None

                # If player 2 entry box has been clicked on
                elif self.text2:
                    if event.type == pygame.KEYDOWN:
                        # Enter player 2 name
                        letter = pygame.key.name(event.key)
                        if letter in string.ascii_letters:
                            self.name2 += letter
                            self.player2 = text.nameBox('Player 2', \
                            self.yMax + 70, self.width, True, self.name2, True)
                            self.typed = 'keyword'
                            
                        elif letter == 'backspace':
                            self.name2 = self.name2[:-1]
                            self.player2 = text.nameBox('Player 2', \
                            self.yMax + 70, self.width, True, self.name2, True)
                            self.typed = 'keyword'
                        # Finished entering name when 'return' is pressed
                        elif letter == 'return':
                            self.namesEntered['Player 2'] = True
                            self.text2 = False
                            self.player2 = text.nameBox('Player 2', self.yMax \
                            + 70, self.width, True, self.name2, False)
                            self.typed = 'return'
                            print(self.typed)
                            
                        if self.typed == 'keyword':
                            msg = 'player2Typed %s\n' % self.name2
                            self.server.send(msg.encode())
                            
                        elif self.typed == 'return':
                            print('sfadfdddfsa', self.typed)
                            msg = 'player2Entered %s\n' % self.name2
                            self.server.send(msg.encode())
                            
                    self.typed = None
                            
                
            # Update board state in accordance with other player    
            while (self.serverMsg.qsize() > 0):
                msg = self.serverMsg.get(False)
                print("received: ", msg, "\n")
                msg = msg.split()
                command = msg[0]
                    
                if command == "gameStarts":
                    player1 = self.player1.textName
                    player2 = self.player2.textName 
                    if msg[2] == 'byPlay2':
                        # "I" am player 1
                        pool.main(player1.title(), player2.title(), True)
                    else:
                        pool.main(player1.title(), player2.title(), False)                        


                elif command == 'player1Typed':
                    if len(msg) > 2:
                        name1 = msg[2]
                    else:
                        name1 = ''
                    self.player1 = text.nameBox('Player 1', \
                    self.yMax + 10, self.width, True, name1, True)
                    self.curr1 = False    # Player 2 cannot change player 1 name
                    
                elif command == 'player1Entered':
                    if len(msg) > 2:
                        name1 = msg[2]
                    else:
                        name1 = ''
                    self.namesEntered['Player 1'] = True
                    self.text1 = False
                    self.player1 = text.nameBox('Player 1', self.yMax \
                    + 10, self.width, True, name1, False)
                    
                elif command == 'player2Typed':
                    if len(msg) > 2:
                        name2 = msg[2]
                    else:
                        name2 = ''
                    self.player2 = text.nameBox('Player 2', \
                    self.yMax + 70, self.width, True, name2, True)
                    self.curr1 = True
                    
                elif command == 'player2Entered':
                    if len(msg) > 2:
                        name2 = msg[2]
                    else:
                        name2 = ''
                    self.namesEntered['Player 2'] = True
                    self.text2 = False
                    self.player2 = text.nameBox('Player 2', self.yMax \
                    + 70, self.width, True, name2, False)
         
                serverMsg.task_done()
                  
                        
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip() 
            
        pygame.quit()
         

# Socket server message set up
def main():
    def handleServerMsg(server, serverMsg):
        server.setblocking(1)
        msg = ""
        command = ""
        while True:
            msg += server.recv(10).decode("UTF-8")
            command = msg.split("\n")
            while (len(command) > 1):
                readyMsg = command[0]
                msg = "\n".join(command[1:])
                serverMsg.put(readyMsg)
                command = msg.split("\n")
    HOST = '127.0.0.1'
    PORT = 50001
        
        
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    server.connect((HOST,PORT))
    
    print("connected to server")
    serverMsg = Queue(100)
        
    threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
    startScreen().run(serverMsg, server)


if __name__ == '__main__':
    main()



    
        

                            
        
    
    