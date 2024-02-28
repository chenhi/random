import socket
from threading import Thread
from colorama import Fore, init, Back
from nothanks import NoThanksSession
import random

# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # port we want to use
#separator_token = "|" # we will use this to separate the client name & message


colorbank = [Fore.BLUE, Fore.CYAN, Fore.GREEN, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.YELLOW
]

# initialize list/set of all connected client's sockets

# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


# Address is a pair (str, int)
sockets = {}            # Key: address; value: socket
names = {}              # Key: address; value: name
colors = {}             # Key: address; value: color
host = None

# Game data
gamesess = None
gameon = False



# TODO
# Host replacement



                                                                # TODO: HOW DO WE START THE GAME?  Need a "host", say the first player to join?  Need to track when they leave etc.
def startGame():
    gamesess = NoThanksSession(list(sockets))
    gameon = True
    #sendToAll("The game is starting!\n\n")
    sendToAll(gamesess.getRules())

#############################################################################
# MESSAGING
# Format: <MSG>action<SEP>information
mes = ">"
sep = "|"

def sendToAll(msg, sender="SERVER"):                            # Sends a non-prompt to all
    if sender != "SERVER":
        msg = mes + "print" + sep + msgFrom(msg, sender)
    else:
        msg = mes + "print" + sep + msg
    for _, clsocket in sockets.items():
        clsocket.send(msg.encode())

def sendToPlayer(msg, addr):                                    # Sends a non-prompt to a single player from the server
    msg = mes + "print" + sep + msg
    sockets[addr].send(msg.encode())

def promptPlayer(msg, addr, retcode):
    msg = mes + "prompt" + sep + msg + sep + retcode
    sockets[addr].send(msg.encode())


def addPlayer(socket, addr) -> bool:                            # Returns whether the player is the host or not
    # add the new connected client to connected sockets
    isHost = False
    if len(sockets) == 0:
        global host
        host = addr
        isHost = True
    sockets[addr] = socket
    names[addr] = f"Player at {addr}"
    colors[addr] = colorbank.pop()
    print(f"[+] {addr} connected{' as host' if isHost else ''}.")
    promptPlayer(f"{'You are the host.  That means you can start the game when there are 3 players.  ' if isHost else ''}What is your name? ", addr, "name")
    return isHost
    


def removePlayer(addr, isHost=False, error=""):
    sockets.pop(addr).close()
    who = names.pop(addr)
    colorbank.append(colors.pop(addr))
    print(f"[!] {who} ({addr}) disconnected{'.' if error == '' else ' with exception ' + error}")
    sendToAll(f"{who} ({addr}) left.  There are {len(sockets)} players.")
    # If the host left need to assign a new host
    if isHost:
        global host
        host = random.choice(list(sockets.keys()))
        sendToAll(f"The new host is {names[host]} ({host}).")
        if gameon == False:
            promptPlayer("Press return to start game. ", host, "start")



def updateName(addr: str, newname: str) -> str:
    if newname == None:
        newname = f"Player at {addr}"
    names[addr] = newname
    return newname

def msgFrom(msg, addr):
    return f"{colors[addr]}{names[addr]}: {msg}{Fore.RESET}"



def listen_for_client(cs, addr, isHost):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from `cs` socket
            data = cs.recv(1024)
            msg = data.decode()
        except Exception as e:
            # Player no longer connected, remove
            removePlayer(addr, isHost, e)
            break
        else:
            # If the player has left, exit the thread (detect if we get an empty message back; the client should never send an empty message)
            if addr not in sockets or data == b'':
                removePlayer(addr, isHost)
                break

            # If we received a message, split it into parts
            print(f"[#] Received message from {addr}: {msg}")
            parts = msg.split("|")
            
            # Find the command

            # Setting a name
            if parts[0] == "name":
                newname = updateName(addr, None if len(parts) < 2 else parts[1])
                print(f"[%] Updated name at {addr} to {newname}.")
                sendToAll(f"{newname} ({addr}) joined the game{' as host' if isHost else ''}.  There are {len(sockets)} players.", addr)
                sendToPlayer(NoThanksSession.getRules(), addr)

            elif parts[0] == "start":
                if len(sockets) < 3:
                    print("[!] Host tried to start game, too few players.")
                    sendToPlayer(f"We need at least 3 players and only have {len(sockets)}.", addr)
                elif len(sockets) > 7:
                    print("[!] Host tried to start game, too many players.")
                    sendToPlayer(f"We can have at most 7 players and have {len(sockets)}.", addr)
                else:
                    sendToAll(f"{names[addr]} ({addr}) has started the game!\n\n")
                    startGame()

            # Asking for information while in the waiting room
            elif len(parts) >= 2 and parts[0] == "query":
                if parts[1] == "rules":
                    sendToPlayer("TODO", addr)
                elif parts[1] == "quit":
                    sendToPlayer("disconnect", addr)

            # Performing an action, i.e. anything inside the game
            elif len(parts) >= 2 and parts[0] == "act":
                # This should only be called if the game is on.  Otherwise, ignore it.
                if gameon == False or (gamesess != None and gamesess.gameOver == True):
                    continue

                

                # If the player issueing an action is not the current player, warn them and don't do anything
                if gamesess.isCurrentPlayer(addr) == False:
                    sendToPlayer("I don't think it's your turn.", addr)
                    continue
                # TODO determine if it's their turn?
                if parts[1] == "no":
                    sendToAll("No thanks!", addr)
                elif parts[1] == "yes":
                    sendToAll("I'll take it.", addr)


            if gameon == False and isHost:
                promptPlayer("Press return to start game. ", addr, "start")

    
        

while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    isHost = addPlayer(client_socket, client_address)

    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket, client_address, isHost))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()