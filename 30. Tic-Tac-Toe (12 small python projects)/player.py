# this file is used in no. 30
import math
import random

class Player:
    def __init__(self, letter):
        #letter in x or o
        self.letter = letter
        
    # we wasnt all player to get their next move given a game
    def get_move(self, game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self, game):
        #get a random valid spot for our next move
        square = random.choice(game.available_moves())
        return square
    
class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square =  input(self.letter + '\'s turn. Input move (0-16):')
            # we are goint to check that this is a correct value by trying to cast
            #it to an integer, and if it's not, then we say its invalid
            # if that spot is not available on the board, we also say its invalid
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True # if these are successful, then yay!
            except ValueError:
                print('Invalid square. Try again')
        
        return val                            
