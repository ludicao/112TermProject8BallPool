#############################
# Sockets Server Demo Modeled frm the 15-112 website
# https://drive.google.com/drive/folders/0B3Jab-H-9UIiZ2pXMExjdDV1dW8

# This file code sets up the hosts, ports, and backlogs for multiple threading 
# and connection. It receives all the clients' messages and sends the messages 
# to other clients.
#############################

import socket
import threading
from queue import Queue

HOST = '127.0.0.1' 
PORT = 50001
BACKLOG = 6

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

def handleClient(client, serverChannel, cID, clientele):
    client.setblocking(1)
    msg = ""
    command = ''
    while True:
        try:
            msg += client.recv(10).decode("UTF-8")
            command = msg.split("\n")
            while (len(command) > 1):
                readyMsg = command[0]
                msg = "\n".join(command[1:])
                serverChannel.put(str(cID) + " " + readyMsg)
                command = msg.split("\n")
        except:
            # we failed
            return

def serverThread(clientele, serverChannel):
    while True:
        global playerNum
        msg = serverChannel.get(True, None)
        #print("msg recv: ", msg)
        msgList = msg.split(" ")
        senderID = msgList[0]
        instruction = msgList[1]
        details = " ".join(msgList[2:])
        if (instruction != ""):
            # Remove player ids from startScreen and endScreen when game mode
            # is initialized
            if instruction == 'cue' and 'Player2Start' in clientele:
                clientele.pop('Player2Start')
            if instruction == 'cue' and 'Player1Start' in clientele:
                clientele.pop('Player1Start')
            if instruction == 'cue' and 'Player1End' in clientele:
                clientele.pop("Player1End")
            if instruction == 'cue' and 'Player2End' in clientele:
                clientele.pop('Player2End')
                
                
            # Reiterate to the starting id num when going to menu from endScreen
            if instruction == 'menu':
                playerNum = 0
            # Remove player ids from endScreen when startScreen is initialized
            if instruction == 'atStart' and 'Player1End' in clientele:
                clientele.pop('Player1End')
            if instruction == 'atStart' and 'Player2End' in clientele:
                clientele.pop('Player2End')
            
            
            # Reiterate to the startingid num when going to game mode
            # from endScreen    
            if instruction == 'play':
                playerNum = 2
            # Remove player ids from game mode when endScreen in initialized
            if instruction == 'atEnd' and 'Player2' in clientele :
                clientele.pop('Player2')
            if instruction == 'atEnd' and 'Player1' in clientele:
                clientele.pop('Player1')
            
            for cID in clientele:
                if cID != senderID:
                    sendMsg = instruction + ' ' + senderID + " " + \
                    details + "\n"
                    clientele[cID].send(sendMsg.encode())
                    #print("> sent to %s:" % cID, sendMsg[:-1])
      
        #print('')
    serverChannel.task_done()

clientele = dict()
playerNum = 0

serverChannel = Queue(100)
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()

names = ["Player1Start", "Player2Start", "Player1", "Player2", \
'Player1End', 'Player2End']

while True:
    client, address = server.accept()
    # myID is the key to the client in the clientele dictionary
    myID = names[playerNum]
    for cID in clientele:
        print (repr(cID), repr(playerNum))
        clientele[cID].send(("newPlayer %s\n" % myID).encode("UTF-8"))
        client.send(("newPlayer %s\n" % cID).encode())
    clientele[myID] = client
    client.send(("myIDis %s \n" % myID).encode())
    print("connection recieved from %s" % myID)
    threading.Thread(target = handleClient, args = 
    
                          (client ,serverChannel, myID, clientele)).start()
  
    playerNum += 1