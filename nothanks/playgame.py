from nothanks import NoThanksSession

num = int(input("How many players? "))
playernames = [f"Player {i}" for i in range(1, num+1)]
session = NoThanksSession(playernames)
if session.validGame == False:
    exit("Invalid game.")

player = session.curPlayer
card = session.topCard
while True:
    res = True if input(f"{session.getPlayerName(player)}'s turn, who has cards {session.banks[player]} and {session.chips[player]} chips.  Current card is a {card}.  Take it?  y/n: ").lower() == "y" else False
    player, card = session.turn(res)
    if player == None or card == None:
        break

scores = session.scoreGame()
print(scores)