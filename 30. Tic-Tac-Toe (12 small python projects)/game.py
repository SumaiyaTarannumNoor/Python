# this file is used in no. 30.

from player import HumanPlayer, RandomComputerPlayer
import time


class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(16)] # we will use a single list to rep a 3x3 board
        self.current_winner = None #keep track of winner!
        
    def print_board(self):
        #tis is just getting the rows
        for row in [self.board[i*4:(i+1)*4] for i in range(4)]:
                print('|__ ' + ' _|_ '.join(row) + ' __|')
                 
    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2 etc (tells us what number correporends tp what box)
        number_board = [[str(i) for i in range (j*4, (j+1)*4)] for j in range(4)] 
        for row in number_board:
            print('|__ ' + ' _|_ '.join(row) + ' __|')
             
            
            
    def available_moves(self):
        return [i for i,spot in enumerate(self.board) if spot == ' ']  
     
    def empty_squares(self):
         return ' ' in self.board
    
    def num_empty_squares(self):
        return self.board.counts(' ') 
    
    def make_move(self, square, letter):
        #if valid move, then make the move (assign square to the letter)
        #then return true. If invalif, return false
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square, letter):
        #check row 
        row_ind = square // 4
        row = self.board[row_ind*4 : (row_ind + 1) *4]
        if all([spot == letter for spot in row]):
            return True
        
        #check column
        col_ind = square % 4
        column = [self.board[col_ind+i*4] for i in range(4)]
        if all([spot == letter for spot in column]):
            return True
        
        #check for diagonal
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 5, 10, 15]] #left to right diagona
            if all([spot == letter for spot in diagonal1]):
                return True
            
            diagonal2 = [self.board[i] for i in [3, 6, 9, 12]] #right to left diagona
            if all([spot == letter for spot in diagonal2]):
                return True
            
        return False   
     
def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()
        
           
        
    letter = 'X' #starting letter
    #iterate while the game still has empty squares
    #(we don't have to worry about winner because we'll jut return the
    # which breaks the loop )
    while game.empty_squares():
        #get the move from the appropriate player
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        #define a function to make a move!
        
        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square}')
                game.print_board()
                print('') #just empty line
            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                    return letter 
                
            letter = 'O' if letter == 'X' else 'X' #switches players       
        #tiny break
        time.sleep(1)   
    if print_game:
            print('It\'s a tie.')    

if __name__ == '__main__':
    x_player = HumanPlayer('X')
    o_player = RandomComputerPlayer('O')   
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)     
