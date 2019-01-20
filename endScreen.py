#############################
# This file runs the end screen of the game. It responds to user interaction 
# through detecting whenter the user has clicked on a button, and switches to 
# different splash screens accordingly. It also displays different messages 
# depending on the different end game situations for the users.
#############################



import pygame
import positions
import graphics
import pool
import startScreen
import text

import socket
import threading
from queue import Queue

class endScreen():
    
    # Init function 
    def init(self):
        
        # Initialize button values                                  
        self.buttonColor1 = (51, 153, 255)
        self.buttonColor2 = (51, 153, 255)
        self.buttonColor3 = (51, 153, 255)   
        self.buttonColor4 = (255, 76, 76)     
        self.buttonWidth = 100
        self.buttonHeight = 40
        
        # Check type of winning/losing condition and current player in control
        if self.currDisplay:
            self.player = 'Player 1'
        else:
            self.player ='Player 2'
        
        # Set up coordinate range of button positions    
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
        
        self.x3Min = self.xMin
        self.x3Max = self.xMax
        self.y3Min = self.y2Min + self.buttonHeight + 20
        self.y3Max = self.y2Max + self.buttonHeight + 20
            
            
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
                      
        #Range coordinates of high score box
        self.xStartB = self.width/2 - self.buttonWidth/2
        self.yStartB = self.y3Max + 10
        
        # Values for exit button of high score board
        self.exitH = 15
        self.exitW = 30        
        self.exitX = self.width*0.35 + self.width*0.3 - self.exitW - 2
        self.exitY = (self.height-self.margin)*0.2 + 2
        
        # Bool indentifying whether high score board is drawn
        self.highScoreAppears = False

        # Add number of wins to winning player/add new player to winning board
        if self.win:
            if self.player == "Player 1":
                updateScore = text.updateScore(self.player1, 'highScore.txt')
                text.writeFile('highScore.txt', updateScore)
            else:
                updateScore = text.updateScore(self.player2, 'highScore.txt')
                text.writeFile('highScore.txt', updateScore)
                
        
        msg = 'atEnd\n'
        self.server.send(msg.encode())
            
            
    # init values of the Pygame class
    def __init__(self, currDisplay, bool, win, width=1000, \
    height=640, fps=50, title="112 Pool Game"):
        self.width = width
        self.height = height
        self.margin = 40
        self.fps = fps
        self.title = title
        self.bgColor = (230, 230, 250)    # Lavendar
        self.currDisplay = currDisplay
        self.bool = bool
        self.win = win
        pygame.init()
        
    # Draw the endScreen text
    def drawText(self, screen):
        self.font = pygame.font.Font('cmunti.ttf', 30)
        # "I" win
        if self.win:
            # "I" am player 1, reg win
            if self.player == 'Player 1' and self.currPlayerWins:
                text = self.font.render('Congrats %s! You Win!' % \
                self.player1.title(), True, (0, 0, 0))
                screen.blit(text, (self.width/2 - text.get_rect().width/2, \
                self.height/3 - text.get_rect().height/2))
            

            # "I" am player 1, opponent fouls
            elif self.player == 'Player 1' and not self.currPlayerWins:
                text = self.font.render('Opponent Fouls!', True, (0, 0, 0))
                text2 = self.font.render('Congrats %s! You Win!' % \
                self.player1.title(), True, (0, 0, 0))
                screen.blit(text, (self.width/2 - text.get_rect().width/2, \
                self.height/3 - text.get_rect().height/2))
                screen.blit(text2, (self.width/2 - text2.get_rect().width/2, \
                self.height/3 + text2.get_rect().height))
            
            # "I" am player 2, reg win
            elif self.player == 'Player 2' and not self.currPlayerWins:
                text = self.font.render('Opponent Fouls!', True, (0, 0, 0))
                text2 = self.font.render('Congrats %s, You Win!' % \
                self.player2.title(), True, (0, 0, 0))
                screen.blit(text, (self.width/2 - text.get_rect().width/2, \
                self.height/3 - text.get_rect().height/2))
                screen.blit(text2, (self.width/2 - text2.get_rect().width/2, \
                self.height/3 + text2.get_rect().height))


            # "I" am player 2, opponent fouls            
            elif self.player == 'Player 2' and self.currPlayerWins:
                text = self.font.render('Congrats %s! You Win' % \
                self.player2.title(), True, (0, 0, 0))
                screen.blit(text, (self.width/2 - text.get_rect().width/2, \
                self.height/3 - text.get_rect().height/2))
                
        # "I" lose        
        else:
            # "I" am player 1, reg lose
            if self.player == 'Player 1' and self.currPlayerWins:
                text = self.font.render('Sorry %s you lose!' % \
                self.player1.title(), True, (0, 0, 0))
                screen.blit(text, (self.width/2 - text.get_rect().width/2, \
                self.height/3 - text.get_rect().height/2))

            # "I" am player 1, I fouled
            elif self.player == 'Player 1' and not self.currPlayerWins:
                text = self.font.render('Uh oh! 8-Ball Striken', True, (0,0,0))
                text2 = self.font.render('Sorry %s You Lose, %s Wins!' % \
                (self.player1.title(), self.player2.title()), True, (0, 0, 0))
                screen.blit(text, (self.width/2 - text.get_rect().width/2, \
                self.height/3 - text.get_rect().height/2))
                screen.blit(text2, (self.width/2 - text2.get_rect().width/2, \
                self.height/3 + text2.get_rect().height))
            
            # "I" am player 2, I fouled
            elif self.player == 'Player 2' and not self.currPlayerWins:
                text = self.font.render('Uh oh! 8-Ball Striken', True, (0,0,0))
                text2 = self.font.render('Sorry %s You Lose, %s Wins!' % \
                (self.player2.title(), self.player1.title()), True, (0, 0, 0))
                screen.blit(text, (self.width/2 - text.get_rect().width/2, \
                self.height/3 - text.get_rect().height/2))
                screen.blit(text2, (self.width/2 - text2.get_rect().width/2, \
                self.height/3 + text2.get_rect().height))
            
            # "I" am player 2, reg lose
            elif self.player == 'Player 2' and self.currPlayerWins:
                text = self.font.render('Sorry %s! you lose' % \
                self.player2.title(), True, (0, 0, 0))
                screen.blit(text, (self.width/2 - text.get_rect().width/2, \
                self.height/3 - text.get_rect().height/2))
            
     
    
    # Draw the endScreen buttons 'back' and 'play again'    
    def drawButtons(self, screen):
        pygame.draw.rect(screen, self.buttonColor1,
        (self.xMin, self.yMin, self.buttonWidth, self.buttonHeight))
        
        pygame.draw.rect(screen, self.buttonColor2, 
        (self.x2Min, self.y2Min, self.buttonWidth, self.buttonHeight))
        
        pygame.draw.rect(screen, self.buttonColor3, 
        (self.x3Min, self.y3Min, self.buttonWidth, self.buttonHeight))

        
        self.font = pygame.font.Font('cmunti.ttf', 15)
        text = self.font.render('Back', True, (0, 0, 0))
        yDist = self.yMax - self.yMin
        yPos = self.yMax - yDist/2 - text.get_rect().height/2
        screen.blit(text, (self.width/2 - text.get_rect().width/2, yPos))
        
        text2 = self.font.render('Play Again!', True, (0,0,0))
        yPosNew = self.y2Max - yDist/2 - text2.get_rect().height/2
        screen.blit(text2, (self.width/2 - text2.get_rect().width/2, yPosNew))
        
        text3 = self.font.render('New Scores!', True, (0,0,0))
        yPosNew2 = self.y3Max - yDist/2 - text3.get_rect().height/2
        screen.blit(text3, (self.width/2 - text3.get_rect().width/2, yPosNew2))
    
    
        
    # Draw the high score box    
    def highScoreBox(self, screen):
        
        xStart = self.width*0.35
        yStart = (self.height-self.margin)*0.2
        width = self.width*0.3
        height = (self.height - self.margin)*0.6
        
        pygame.draw.rect(screen, (255,228,196), (xStart, yStart, \
        width, height), 0)
        
        wordSpace = 15
        
        pygame.draw.rect(screen, self.buttonColor4, (self.exitX, \
        self.exitY, self.exitW, self.exitH), 0)
        
        font = pygame.font.Font('cmunti.ttf', 10)
        exitText = font.render('Exit', True, (0, 0, 0))
        xText = xStart+width-2-self.exitW/2 - exitText.get_rect().width/2 
        yText = yStart+2+self.exitH/2 - exitText.get_rect().height/2
        screen.blit(exitText, (xText, yText))
        
        
        font = pygame.font.Font('cmunti.ttf', 30)
        title = font.render('High Score Board', True, (0, 0, 0))
        screen.blit(title, (self.width/2 - title.get_rect().width/2, \
            yStart + self.exitH + 10))
            
        titleH = title.get_rect().height
        
        font2 = pygame.font.Font('cmunti.ttf', 20)
        testSize = font2.render('High Score Board', True, (0, 0, 0))
        lineH = testSize.get_rect().height
        
        # Read the names from the highScore text file and display them
        listNames = text.readScores('highScore.txt')
        y = yStart + 10 + titleH + wordSpace
        x = xStart + 5
        if listNames != ['']:
            for i in range(len(listNames)):
                yEach = y + i*(lineH + wordSpace)
                nameScore = listNames[i].split()
                lineMsg = font2.render(nameScore[0] + ' ' + nameScore[1], \
                True, (0,0,0))
                screen.blit(lineMsg, (x, yEach))
    
    
    # Draw objects on screen    
    def redrawAll(self, screen):
        self.gameboard.draw(screen)
        self.border.draw(screen)
        self.holeGroup.draw(screen)
        self.drawText(screen)
        self.drawButtons(screen)
        if self.highScoreAppears:
            self.highScoreBox(screen)
            
        
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
            
        # New Scores button
        if cursorX > self.x3Min and cursorX < self.x3Max and \
        cursorY < self.y3Max and cursorY> self.y3Min:
            self.buttonColor3= (204, 229, 255)
        else:
            self.buttonColor3 = (51, 153, 255)
        
        # Exit button on high score board    
        if self.highScoreAppears:
            if cursorX > self.exitX and cursorX < self.exitX+self.exitW and \
            cursorY > self.exitY and cursorY < self.exitY+self.exitH:
                self.buttonColor4 = (255, 128, 128)
            else:
                self.buttonColor4 = (255, 76, 76)
    
    # If mouse if pressed on button, continue to start mode or play mode        
    def mousePressed(self):
        cursorX = pygame.mouse.get_pos()[0]
        cursorY = pygame.mouse.get_pos()[1]
        
        # Return to start mode
        if cursorX > self.xMin and cursorX < self.xMax and \
        cursorY < self.yMax and cursorY > self.yMin:
            msg = 'menu\n'
            self.server.send(msg.encode())
            startScreen.main()
        
        # Return to play mode    
        if cursorX > self.x2Min and cursorX < self.x2Max and \
        cursorY < self.y2Max and cursorY> self.y2Min:
            
            if self.player == 'Player 1':
                msg = 'play byPlay1\n'
                self.server.send(msg.encode())
                pool.main(self.player1, self.player2, True)
                
            elif self.player == 'Player 2':
                msg = 'play byPlay2\n'
                self.server.send(msg.encode())
                pool.main(self.player1, self.player2, False)
                
        # Pop up high score board
        if cursorX > self.x3Min and cursorX < self.x3Max and \
        cursorY < self.y3Max and cursorY> self.y3Min:
            self.highScoreAppears = True
        
        # Exit from high score board    
        if self.highScoreAppears:
            if cursorX > self.exitX and cursorX < self.exitX+self.exitW and \
            cursorY > self.exitY and cursorY < self.exitY+self.exitH:
                self.highScoreAppears = False
            
            
    # Run function         
    def run(self, player1, player2, serverMsg=None, server=None):
    
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
    
        # stores all the keys currently being held down
        self._keys = dict()
    
        # call game-specific initialization
        self.serverMsg = serverMsg
        self.server = server
        self.player1 = player1
        self.player2 = player2
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
                    
            # Update current board state in accordance with the other player
            while (self.serverMsg.qsize() > 0):
                msg = self.serverMsg.get(False)
                print("received: ", msg, "\n")
                msg = msg.split()
                command = msg[0]     # Instruction
                
                if command == 'menu':
                    startScreen.main()
                    
                elif command == 'play':
                    if msg[2] == 'byPlay2':
                        pool.main(self.player1, self.player2, True)
                    else:
                        pool.main(self.player1, self.player2, False)
                    
                    
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()   
            
        pygame.quit()

   
        
# Set up for socket module        
def main(name1, name2, currDisplay, bool, win):
    
    def handleServerMsg(server, serverMsg):
        server.setblocking(1)
        msg = ""
        command = ""
        while True:
            msg += server.recv(10).decode()
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
        

    threading.Thread(target = handleServerMsg, args = \
    (server, serverMsg)).start()
    endScreen(currDisplay, bool, win).run(name1, name2, serverMsg, server)
            
            