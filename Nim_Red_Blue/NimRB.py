import sys
from copy import deepcopy
import math
import random
import argparse

alpha = -sys.maxsize #ALPHA VALUE TO NEGATIVE INFINITE(NEGATIVELY LARGE NUMBER)
beta = sys.maxsize #BETA VALUE TO POSITVE INFINITE(POSITIVELY LARGE NUMBER)

#A CLASS NIMRB CONTAINS ALL THE HELPER FUNCTIONS
class NimRB:

    #INITIALISING OBJECTS
    def __init__(self, red_numbers, blue_numbers, first_player, depth):
        self.red_numbers = red_numbers
        self.blue_numbers = blue_numbers
        self.score = {'human': 0, 'computer': 0}
        self.current_player = first_player
        self.depth = depth

    #SKORE IS SUM OF RED AND BLUE BALLS WITH THIER RESPECTIVE VALUES
    def skore(self):
        return abs(2* self.red_numbers + 3* self.blue_numbers)

    #EVALUATE FUNCTION
    def evaluate(self):
        # evaluate function returns the difference between the current score of the computer and human players
        return self.score['computer'] - self.score['human']

    #SWITCHING THE USER AFTER THEIR TURN
    def switchPlayer(self):
        if self.current_player == 'computer':
            self.current_player = 'human'
        else:
            self.current_player = 'computer'
        
        return self.current_player

    #RESULT MAKE BEST MOVE FOR COMPUTER TO TAKE
    def result(self, state, action):
        # Computes the next state given current state and action
        pile, count =state
        pile1, pile2 = state
        if pile == 0:
            new_state = (pile1 - count, pile2)
        else:
            new_state = (pile1, pile2 - count)
        return new_state

    #ACTIONS FUNCTION GENERATES ALL THE POSSIBLE STATES OF THE GAME
    def actions(self, state):
        # Generates legal actions for a given state
        pile1, pile2 = state
        actions_list = []
        for pile, count in enumerate(state):
            for i in range(1, count+1):
                actions_list.append((pile, i))
        return actions_list

    #UTILITY FUNCTION TO FOR TIE, AND WHO WINS THE GAME
    def utility(self, state):
        # Calculates the utility value of a terminal state
        pile1, pile2 = state
        if pile1 == 0 and pile2 == 0:
            return 0  # kind of a tie match
        elif pile1 == 0:
            return 1  # player 2 wins
        else:
            return -1  # player 1 wins

    #TERMINAL FUNCTION TO CHECK WHETHER THE STATE IS A END STATE OR NOT
    def terminal_test(self, state):
        # Determines if a state is terminal (i.e. the game is over)
        pile1, pile2 = state
        return pile1 == 0 and pile2 == 0
    
    #MAX_VALUE FUNCTION IS FOR COMPUTER TO PLAY AS MAX PLAYER
    def max_value(self, state, alpha, beta, depth_limit):
        # Calculates the max-value for a given state
        if self.terminal_test(state):
            return self.utility(state), None
        v = float('-inf')
        best_move = None
        for action in self.actions(state):
            new_state = self.result(state, action)
            if depth_limit == 0:
                return v, best_move
            min_val, _ = self.min_value(new_state, alpha, beta, depth_limit-1)
            if min_val > v:
                v = min_val
                best_move = action
            if v >= beta:
                return v, best_move
            alpha = max(alpha, v)
        return v, best_move

    #MIN_VALUE FUNCTION IS TO PLAY AGAINST HUMAN PLAYER WITH COMPUTER
    def min_value(self, state, alpha, beta, depth_limit):
        # Calculates the min-value for a given state
        if self.terminal_test(state):
            return self.utility(state), None
        v = float('inf')
        best_move = None
        for action in self.actions(state):
            new_state = self.result(state, action)
            if depth_limit == 0:
                return v, best_move
            max_val, _ = self.max_value(new_state, alpha, beta, depth_limit-1)
            if max_val < v:
                v = max_val
                best_move = action
            if v <= alpha:
                return v, best_move
            beta = min(beta, v)
        return v, best_move

    #MIN_MAX ALGORITHM WITH ALPHA BETA PRUNING 
    def alpha_beta_decision(self, state, depth_limit):
        # Computes the optimal action for a given state using alpha-beta pruning
        alpha = float('-inf')
        beta = float('inf')
        _, best_move = self.max_value(state, alpha, beta, depth_limit)
        return best_move

#HUMANTURN FUNCTION TO HUMAN PLAYER TO MAKE THE CHOICE AND MOVEMENT 
def humanTurn(two_player_game):
    
    while two_player_game.current_player == 'human':
        pile_color = input("Human turn Enter the pile to pick from {'Red', 'Blue'}: ")    
        if pile_color == 'Red'and two_player_game.red_numbers < 1:
            print("You win! with score:", two_player_game.skore())
            sys.exit()    
        elif pile_color == 'Red' and two_player_game.red_numbers >0:
            two_player_game.red_numbers -= 1          
            two_player_game.switchPlayer()
            print("human 1 tile moved and given control to computer")
            continue
        if pile_color == 'Blue' and two_player_game.blue_numbers < 1:
            print("You win! with score:", two_player_game.skore())
            sys.exit()
        elif pile_color == 'Blue' and two_player_game.blue_numbers >0:
            two_player_game.blue_numbers -= 1
            # two_player_game.current_player = 'computer' 
            two_player_game.switchPlayer() #SWITCH THE CURRENT PLAYER
            print("human 1 tile moved and given control to computer")
            continue
        break    
    return None

#COMPUTERTURN FUNCTION FOR COMPUTER TO PICK BEST POSSIBLE MOVE USING MINMAX ALPHA BETA PRUNING   
def computerTurn(two_player_game):

    # Simulates the computer's turn
    initial_state = (two_player_game.red_numbers, two_player_game.blue_numbers)
    state = initial_state
    action = two_player_game.alpha_beta_decision(state, two_player_game.depth)
    state = two_player_game.result(state, action)

    while two_player_game.current_player == 'computer':
        if(two_player_game.red_numbers>1 and two_player_game.blue_numbers>1):
            two_player_game.red_numbers -= 1 
            print("computer takes 1 red")
            # two_player_game.current_player = 'human'
            two_player_game.switchPlayer()
        elif (two_player_game.red_numbers>1 and two_player_game.blue_numbers>0):
            two_player_game.red_numbers -= 1 
            print("computer takes 1 red")
            # two_player_game.current_player = 'human'
            two_player_game.switchPlayer()
        elif (two_player_game.red_numbers>0 and two_player_game.blue_numbers>1):
            two_player_game.blue_numbers -= 1 
            print("computer takes 1 blue")
            # two_player_game.current_player = 'human'
            two_player_game.switchPlayer()
        elif (two_player_game.red_numbers>0 and two_player_game.blue_numbers>0):
            two_player_game.blue_numbers -= 1 
            print("computer takes 1 blue")
            # two_player_game.current_player = 'human'
            two_player_game.switchPlayer()
        elif ((two_player_game.red_numbers == 0) and (two_player_game.blue_numbers == 0)):
            print("computer wins with score: ", two_player_game.skore())
            sys.exit(0)
        elif ((two_player_game.red_numbers == 0) or (two_player_game.blue_numbers == 0)):
            print("computer wins with score: ", two_player_game.skore())
            sys.exit(0)

    return None

#MAIN DRIVER FUNCTION TO START OUR CODE 
if __name__ == "__main__":

    first_player = 'computer'
    depth = None

    red_numbers = int(sys.argv[1]) #FIRST ARGUMENT FORM COMMAND LINE -> NUMBER OF RED BALLS
    blue_numbers = int(sys.argv[2]) #SECOND ARGUMENT FROM COMMAND LINE -> NUMBER OF BLUE BALLS

    if sys.argv[3] is None or sys.argv[3] == 'computer': #THIRD ARGUMENT FROM COMMAND LINE -> WHO IS PLAYER FIRST TURN
        first_player = 'computer'
    first_player = 'computer' if len(sys.argv) < 4 or sys.argv[3] == 'computer' else 'human' 

    depth = int(sys.argv[4]) #FOURTH ARGUMENT FORM COMMAND LINE -> WHICH IS DEPTH_LIMIT

    two_player_game = NimRB(red_numbers, blue_numbers, first_player, depth) #CREATING OBJECT TO NIMRB CLASS
    
    while True:
        print("red balls count:", two_player_game.red_numbers, "blue balls count:",  two_player_game.blue_numbers)
        if two_player_game.current_player == 'human': #HUMAN TURN
            humanTurn(two_player_game) #HUMANTURN INVOKING
        else: #COMPUTER TURN
            computerTurn(two_player_game) #COMPUTERTURN INVOKING