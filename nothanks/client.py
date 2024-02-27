import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back


###############################################################################################

startChips = {3: 11, 4: 11, 5: 11, 6: 9, 7: 7}

def getRules(num):
    rules = "\n==========RULES==========\n"
    rules += f"The deck consists of 24 integer-valued cards drawn from the range [3, 35].\n"
    rules += f"There are currently {num} players, each starting with {startChips[num]} chips.\n"
    rules += f"On your turn, you can either take the card and chips on the table, or reject it by paying one chip if you have one.  The chips you take are playable, the card goes in your bank.\n"
    rules += f"When the cards are exhausted, the game ends, and you score as follows.\n"
    rules += f"For each run (consecutive sequence) in your bank, you add the score of the lowest card in the run.  You then subtract the number of chips.\n"
    rules += f"Lowest score wins.\n\n"
    return rules


################################################################################################
# init colors

init()

# set the available colors
# colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
#     Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
#     Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
#     Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
# ]

# choose a random color for the client
# client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
#separator_token = "|" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")

# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")



# prompt the client for a name
#name = input("Enter your name: ")
#to_send = f"name|{name}"
#s.send(to_send.encode())

#print("\n\nWelcome to the game 'No Thanks!'.  To quit, type 'quit'.  For the rules, type 'rules'.\n\n")

# How to process messages
def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        parts = message.split("|")
        if len(parts) == 0:
            continue
        elif parts[0] == "print" and len(parts) > 1:                                                                # Print format: "|print|text to print|ignore"
            print("\n" + parts[1])
        elif parts[0] == "prompt":                                                                                  # Prompt format: "|prompt|text of the prompt|heading of reply|ignore"
            res = input("You have been prompted: " if len(parts) == 1 else parts[1]).replace("|", "")               # Strip response of the special character
            res = ("response|" if len(parts) <= 2 else parts[2] + "|") + res
            s.send(res.encode())




# make a thread that listens for messages and prompts
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()


yourPlayerNumber = 0
numPlayers = 4
yourCards = []
yourChips = 3


while True:
    # Player can request things from the server at any time, or quit
    to_send =  input("\n Waiting for the server or other players... (commands: 'hand', 'rules', 'quit'). ")
    # a way to exit the program
    if to_send.lower() == 'quit':
        break
    elif to_send.lower() == 'rules':
        to_send = "query|rules"
    elif to_send.lower() == 'hand':
        to_send = "query|hand"
    # add the datetime, name & the color of the sender
    #date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    #to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    # finally, send the message
    s.send(to_send.encode())

# close the socket
s.close()