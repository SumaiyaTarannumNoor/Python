import random

def play():
    user = input("What's your choice?\n 'r' for rock, 'p' for paper, 's' for scissor!: \n")
    computer = random.choice(['r', 'p', 's'])

    if user == computer:
        return "It's a tie!"

    if is_win(user, computer):
        return "You won!!"

    return "You lost!"


def is_win(player, opponent):
    #return true if player wins
    #r>s, s>p, p>r

    if(player == 'r' and opponent == 's') or (player == 's' and opponent == 'p') or (player == 'p' and opponet == 'r'):
        return True

print (play())


        
