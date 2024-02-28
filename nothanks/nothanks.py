import random

class NoThanksSession():
    startChips = {3: 11, 4: 11, 5: 11, 6: 9, 7: 7}

    def __init__(self, players: list):  
        if len(players) < 3 or len(players) > 7 or len(players) > len(set(players)):        # If the number of players is wrong or the player IDs are not unique, don't start the game.
            self.gameOver = True
            self.validGame = False
        else:
            self.validGame = True
            self.deck = random.sample(range(3, 36), 24)                             # Get a random shuffled subset of the deck
            self.players = players                                                  
            random.shuffle(players)                                                 # A list of strings; the index is the player number and the value is the unique "name" or "id"
            self.chips = [self.numChips(len(players))] * len(players)
            self.banks = [[] for x in players]
            self.curPlayer = 0
            self.chipPool = 0
            self.topCard = self.deck.pop()
            self.gameOver = False
            self.scores = {}
        

    def getRules(self=None):
        rules = "\n==========RULES==========\n"
        rules += f"The deck consists of 24 integer-valued cards drawn from the range [3, 35].\n"
        if self != None:
            num = len(self.players)
            rules += f"There are currently {num} players, each starting with {NoThanksSession.startChips[num]} chips.\n"
        rules += f"On your turn, you can either take the card and chips on the table, or reject it by paying one chip if you have one.  The chips you take are playable, the card goes in your bank.\n"
        rules += f"When the cards are exhausted, the game ends, and you score as follows.\n"
        rules += f"For each run (consecutive sequence) in your bank, you add the score of the lowest card in the run.  You then subtract the number of chips.\n"
        rules += f"Lowest score wins.\n"
        rules += f"==========RULES==========\n\n"
        return rules

    def numChips(self, numPlayers: int) -> int:
        if numPlayers in NoThanksSession.startChips:
            return NoThanksSession.startChips[numPlayers]
        else:
            return None

    def getPlayerName(self, id: int) -> str:                                    # Returns a string
        return str(self.players[id])
    
    def getPlayerId(self, id: int):                                             # Returns some undetermined data type
        return self.players[id]
    
    def isCurrentPlayer(self, id: str) -> bool:
        return self.players[self.curPlayer] == id

    def turn(self, response: bool) -> tuple[int,int]:                           # Returns the numeric ID of the next player and the next card
        if self.gameOver:                                                       # Don't do anything if the game is over and return None
            return None, None
        if response == False and self.chips[self.curPlayer] > 0:
            self.chips[self.curPlayer] -= 1                                     # Take a chip away
            self.chipPool += 1                                                  # Move the chip to the pool
        else:
            self.banks[self.curPlayer].append(self.topCard)                     # Give the card to the player
            self.chips[self.curPlayer] += self.chipPool                         # Give the chip pool to the player
            self.chipPool = 0                                                   # Empty the chip pool
            if len(self.deck) == 0:
                self.topCard = None
                self.gameOver = True
                return None, None
            else:
                self.topCard = self.deck.pop()                                  # Reveal the next card

        self.curPlayer = (self.curPlayer + 1) % len(self.players)               # Go to next player
        return self.curPlayer, self.topCard
    
    def scoreGame(self) -> dict:                                                # Scores the game then returns the scores
        for i, key in enumerate(self.players):
            score = 0
            score -= self.chips[i]
            self.banks[i].sort()
            prev = -1
            for n in self.banks[i]:
                if prev != n - 1:
                    score += n
                prev = n
            self.scores[key] = score
        return self.scores