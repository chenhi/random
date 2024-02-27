import socket
from threading import Thread
from colorama import Fore, init, Back
from nothanks import NoThanksSession

# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # port we want to use
separator_token = "|" # we will use this to separate the client name & message


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


# The key for us will be the address
sockets = set()
names = {}
colors = {}
addrs = set()


# Game data
gamesess = None
gameon = False

def startGame():
    gamesess = NoThanksSession(list(addrs))
    gameon = True
    sendToAll("The game is starting!\n\n")
    sendToAll(gamesess.getRules())



def sendToAll(msg, sender="SERVER"):                            # Sends a non-prompt to all
    if sender != "SERVER":
        msg = "print|" + msgFrom(msg, sender)
    for clsocket in sockets:
        clsocket.send(msg.encode())

def addPlayer(socket, addr):
    # add the new connected client to connected sockets
    sockets.add(socket)
    names[addr] = f"Player at {addr}"
    colors[addr] = colorbank.pop()
    addrs.add(addr)
    print(f"[+] {addr} connected.")
    msg = "prompt|What is your name? |name"
    socket.send(msg.encode())


def removePlayer(socket, addr) -> str:
    sockets.remove(socket)
    colorbank.append(colors.pop(addr))
    return names.pop(addr)


def updateName(addr: str, newname: str) -> str:
    if newname == None:
        newname = f"Player at {addr}"
    names[addr] = newname
    return newname

def msgFrom(msg, addr):
    return f"{colors[addr]}{names[addr]}: {msg}{Fore.RESET}"



def listen_for_client(cs, addr):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # Player no longer connected, remove
            who = removePlayer(cs, addr)
            print(f"[!] {e}")
            sendToAll(f"Left the game. ([!] {e})")
        else:
            # If we received a message, split it into parts
            print(f"[#] Received message from {addr}: {msg}")
            parts = msg.split("|")
            
            # If it was an empty message, ignore it
            if len(parts) == 0:
                continue

            # Otherwise, find the command
            if parts[0] == "name":
                newname = updateName(addr, None if len(parts) < 2 else parts[1])
                print(f"[%] Updated name at {addr} to {newname}.")
                sendToAll(f"{newname} joined the game.", addr)
            elif parts[0] == "act" and len(parts) >= 2:
                # TODO determine if it's their turn?
                if parts[1] == "no":
                    sendToAll("No thanks!", addr)
                elif parts[1] == "yes":
                    sendToAll("I'll take it.", addr)
            
        # iterate over all connected sockets
        

while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    addPlayer(client_socket, client_address)

    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket, client_address))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()