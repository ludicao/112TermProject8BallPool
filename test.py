                    '''
                        if self.display1 == True:
                            self.player1.ballList += [[ball.number,ball.color]]
                            text.Player.playerContinue = True

                        elif self.display1 == False:
                            self.player2.ballList += [[ball.number,ball.color]]
                            text.Player.playerContinue = True
                        
                        ball.kill()
                        
                    elif ball.color == (255, 255, 255):
                        self.whiteBall.holeViolation = True
                        self.xSpeed = 0
                        self.ySpeed =0
                        
                    else:
                        if self.display1 == True:
                            if self.player1.type == 'striped' and \
                            (type(ball) != ballClass.Ball):
                                self.player1.ballList += [[ball.number, ball.color]]
                            elif self.player1.type == 'solid' and \
                            (type(ball) == ballClass.Ball):
                                self.player1.ballList += [[ball.number, ball.color]]
                            text.Player.playerContinue = True

                        elif self.display1 == False:
                            if self.player2.type == 'striped' and \
                            (type(ball) != ballClass.Ball):
                                self.player2.ballList += [[ball.number, ball.color]]
                            elif self.player2.type == 'solid' and \
                            (type(ball) == ballClass.Ball):
                                self.player1.ballList += [[ball.number, ball.color]]
                            text.Player.playerContinue = True
                        ball.kill()
                    '''
import pool

print(pool.Pygame.width)
                        