'''
Author: Dylan Fox 12-1-21
ASCII/Console based TicTacToe game that implements the MiniMax algorithm for 1 player game mode
'''

import random
import os

# GLOBAL CONSOLE COLOR VARIABLES
from colorama import init
init()

W  = '\033[0m'  # white (default)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple

# GLOBAL GAME BOARD VARIABLE
board = [' ']*10

# TEST BOARD STATES FOR AI
#board = [ 0    1    2    3    4    5    6    7    8    9]

#board = [' ', 'X', 'O', 'O', 'X', 'O', 'X', 'O', ' ', ' '] # AI WIN next move
#board = [' ', ' ', 'X', ' ', 'O', 'X', ' ', ' ', ' ', ' '] # Move on 3 and player wins next move
#board = [' ', 'X', 'O', ' ', 'X', 'O', 'O', ' ', 'X', ' '] # garunteed tie
#board = [' ', 'O', 'X', 'O', 'O', 'X', 'X', 'X', ' ', 'O'] # AI must choose to tie game

def check_draw(board): # CHECK FOR DRAW
    for i in range(1,10):
        if check_space(board, i):
            return False
    return True

def check_win(board, marker): # CHECKS FOR WIN CONDITION AFTER EACH TURN
    return ((board[7] == board[8] == board[9] == marker) or # TOP ROW
        (board[4] == board[5] == board[6] == marker) or # MIDDLE ROW
        (board[1] == board[2] == board[3] == marker) or # BOTTOM ROW
        (board[7] == board[4] == board[1] == marker) or # LEFT COLUMN
        (board[8] == board[5] == board[2] == marker) or # MIDDLE COLUMN
        (board[9] == board[6] == board[3] == marker) or # RIGHT COLUMN
        (board[7] == board[5] == board[3] == marker) or # BACKSLASH DIAG
        (board[1] == board[5] == board[9] == marker))   # FORWARDSLASH DIAG

def player_move(board, marker): # GETS AND PROCESSES PLAYER MOVE
    while True:
        playerChoice = input('Player {} make your move! '.format(marker))
        
        if playerChoice.isdigit() and int(playerChoice) in range(1,10):
            playerChoice = int(playerChoice) # CONVERTS INPUT TO INT
            
            if check_space(board, playerChoice):
                board[playerChoice] = marker
                return board
            else:
                print(R + 'That space is already occupied.\n' + W)
        else:
            print(R +'Enter a valid digit 1-9.\n' + W)

def check_space(board, pos): # CHECK TO VALIDATE SPACE IS OPEN
    return board[pos] == ' '

def marker_choice(): # ASKS AND ASSIGNS PLAYER SYMBOL
    while True:
        playerInput = input('Player 1: play as X or O? ').upper()
    
        if playerInput == 'X':
            return 'X', 'O'
        elif playerInput == 'O':
            return 'O', 'X'
        else:
            print(R + 'Please choose either X or O.\n' + W)
        
def draw_board(board): # DRAWS GAME BOARD   
    # PRINTS CURRENT GAME BOARD
    #os.system('cls') # CLEAR CONSOLE IN WINDOWS
    print('\n')
    print('\t {} | {} | {} '.format(board[7], board[8], board[9]))
    print('\t-----------')
    print('\t {} | {} | {} '.format(board[4], board[5], board[6]))
    print('\t-----------')
    print('\t {} | {} | {} '.format(board[1], board[2], board[3]))
    print('\n')

def evaluate(board, computer_marker, player_marker): # CHECKS FOR WIN CONDITIONS AND RETURNS VALUE TO minimax() | USED IN 1 PLAYER ONLY
    if check_win(board, computer_marker):
        return 10
    elif check_win(board, player_marker):
        return -10
    else:
        return 0

def minimax(board, depth, is_max_player, computer_marker='O', player_marker='X'):
    score = evaluate(board, computer_marker, player_marker)
    if score == 10: # Maximizer win
        return (score - depth)
    elif score == -10: # Minimizer win
        return (score + depth)

    if is_max_player:
        max_value = -1000
        for i in range(len(board)):
            if check_space(board, i):
                board[i] = computer_marker
                max_value = max(max_value, minimax(board, depth + 1, False))
                board[i] = ' '
        return max_value
    
    else:
        min_value = 1000
        for i in range(len(board)):
            if check_space(board, i):
                board[i] = player_marker
                min_value = min(min_value, minimax(board, depth + 1, True))
                board[i] = ' '
        return min_value

# Keeps track of the current best move - used to start the minimax algorithm
def find_best_move(board, computer_marker='O'):
    best_score = -1000 # placeholder values
    best_move = -1     # ^^              ^^

    for i in range(1, 10):
        if check_space(board, i):
            board[i] = computer_marker # Makes move
            move_value = minimax(board, 0, False)
            board[i] = ' ' # Undoes move
            if move_value > best_score:
                best_score = move_value
                best_move = i
    return best_move

def introduction(board): # GAME INTO AND CHECKS IF 1 OR 2 PLAYERS
    
    # BANNER INTRO
    print(O + ".___________. __    ______    .___________.    ___       ______    .___________.  ______    _______ ")
    print(    "|           ||  |  /      |   |           |   /   \     /      |   |           | /  __  \  |   ____|")
    print(    "`---|  |----`|  | |  ,----'   `---|  |----`  /  ^  \   |  ,----'   `---|  |----`|  |  |  | |  |__   ")
    print(    "    |  |     |  | |  |            |  |      /  /_\  \  |  |            |  |     |  |  |  | |   __|  ")
    print(    "    |  |     |  | |  `----.       |  |     /  _____  \ |  `----.       |  |     |  `--'  | |  |____ ")
    print(    "    |__|     |__|  \______|       |__|    /__/     \__\ \______|       |__|      \______/  |_______|" + W)
    print(G+'\nWelcome to my Tic Tac Toe game! The game board positions are in the same layout as your numpad.' + W)

    # Input validation & gate for 1 - 2 player game choice
    while True: 
        try:
            num_of_players = int(input('Will you be playing 1 or 2 player: '))

            if num_of_players in range(1, 3):
                break
            else:
                print(R + 'Enter a value of 1 or 2.\n' + W)
        except:
            print(R + 'Enter a value of 1 or 2.\n' + W)

    # STARTS GAME
    if num_of_players == 1:
        while True:
            first_choice = input('Press 1 if you want to go first or 2 for the AI: ')
            if first_choice.isdigit() and int(first_choice) in range(1,3):
                game_logic_1_player(board, int(first_choice))
            else:
                print(R + 'Enter a valid option.\n' + W)

    elif num_of_players == 2:
        game_logic_2_player(board) 

def game_logic_1_player(board, turn): # MAIN LOGIC CONTROLLER - for 1 player game
    # VARIABLES 
    player_marker, computer_marker = 'X', 'O'
    tick = 0 # Tracks number of turns played

    draw_board(board) # Draws inital game board
    while True:

        # Players turn
        if turn == 1:
            # Proccess player move & updates board
            player_move(board, player_marker)
            draw_board(board)
            
            # Checks for win/draw after 5th move
            if tick >= 4:
                if check_win(board, player_marker):
                    print('You Win!')
                    game_over(board)
                elif check_draw(board):
                    print("It's a draw!")
                    game_over(board)
            # Passes turn to computer
            tick += 1
            turn = 2 

        # Computers turn
        elif turn == 2:
            if tick == 8: # If 8 moves have been played without a win AI will play only empty spot
                for i in range(len(board)):
                    if check_space(board, i):
                        board[i] = computer_marker    
            else: # If there are > 1 open space will use minimax to determine best move
                move = find_best_move(board)
                board[move] = computer_marker
                
            draw_board(board)
            # Checks for win/draw
            if tick >= 4:
                if check_win(board, computer_marker):
                    print('You Lose!')
                    game_over(board)
                elif check_draw(board):
                    print("It's a draw!")
                    game_over(board)

            # Passes turn to player
            tick += 1
            turn = 1


def game_logic_2_player(board): # MAIN LOGIC CONTROLLER - for 2 player game
    # VARIABLES
    turn = random.randint(1,2) # CONTROLS PLAYER TURN 1, 2 FOR PLAYERS RESPECTIVELY | RANDOM START PLAYER
    tick = 0 # Tracks number of turns played
    
    # PLAYER MARKER CHOICE
    player_1_marker, player_2_marker = marker_choice()
    
    # DRAW INITIAL BOARD
    draw_board(board)

    print(O+'  Player {} will go first{}'.format(turn, W))
    
    while True: # GAME WHILE LOOP           
        
        if turn == 1: # PLAYER 1
        # ASK TO CHOOSE MOVE > CHECK SPACE > COMMIT CHANGE
            player_move(board, player_1_marker) 
            draw_board(board) # DRAWS BOARD AFTER MOVE           
        
        # Checks for win/draw after 5th move
            if tick >= 4:
                if check_win(board, player_1_marker):
                    print('Player 1 is the winner!')
                    game_over(board)
                elif check_draw(board):
                    print("It's a draw!")
                    game_over(board)

            ## PASSES TURN TO PLAYER 2
            tick += 1
            turn = 2
        
        elif turn == 2: # PLAYER 2
        # ASK TO CHOOSE MOVE > CHECK SPACE > COMMIT CHANGE
            player_move(board, player_2_marker)
            draw_board(board) # DRAWS BOARD AFTER MOVE 

            # Checks for win/draw after 5th move
            if tick >= 4:
                if check_win(board, player_2_marker):
                    print('Player 2 is the winner!')
                    game_over(board)
                elif check_draw(board):
                    print("It's a draw!")
                    game_over(board)

            ## PASSES TURN TO PLAYER 1
            tick += 1
            turn = 1

def game_over(board):
    while True:
        keepPlaying = input('Would you like to keep playing? Yes or No: ').lower()
        if keepPlaying == 'yes' or keepPlaying == 'y':
            board = [' ']*10 # Resets game board
            introduction(board)
        elif keepPlaying == 'no' or keepPlaying == 'n':
            exit()
        else:
            print('Please enter yes or no')

def main():
    introduction(board)        

if __name__ == "__main__":
    main()
