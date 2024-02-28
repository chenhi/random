from nothanks import NoThanksSession
import torch
import torch.nn as nn

# Number of players
num = 3
playernames = [i for i in range(num)]

session = NoThanksSession(playernames)
if session.validGame == False:
    exit("Invalid game.")


class DQN(nn.Module):
    def __init__(self, num_states, num_actions):
        super(DQN, self).__init__






player = session.curPlayer
card = session.topCard
while True:
    res = True if input(f"{session.getPlayerName(player)}'s turn, who has cards {session.banks[player]} and {session.chips[player]} chips.  Current card is a {card}.  Take it?  y/n: ").lower() == "y" else False
    player, card = session.turn(res)
    if player == None or card == None:
        break

scores = session.scoreGame()
print(scores)