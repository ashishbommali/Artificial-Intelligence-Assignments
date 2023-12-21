PROGRAMMING LANGUAGE USED: PYTHON (VERSION - 3.10.11 64-BIT), PIP VERSION(23.0.1)
STRUCTURE OF CODE: Our code starts with driver code followed by taking cmd inputs, and passing the values to functions defined for humanTurn and computerTurn
		Public Functions: computerTurn()-> computer picks best move and makes it using min_max algorithm with alpha_beta_pruning and required function calls in Class NimRB, humanTurn()
				-> human turn prompts for pile and makes a move in that pile.
		Classes: NimRB, 
			Class Methods: __init__()-> initialises the parameters,skore()-> return the score after game over, evaluate()-> evaluate function to check the score of individuals, switchPlayer()
				->switches the current player, result()-> computer bestMove will be made, actions()-> return all the possible states for computer, utility()-> return utility value for computer,
				 terminal_test()->return whether piles are empty or not which is terminal state for game, max_value()-> computer as max player using minmax alpha beta, min_value(), alpha_beta_decision()
				->minimax algorithm with alpha beta pruning return best move for computer
			
HOW TO RUN THE CODE: 
		RUN FROM COMMAND LINE USING SYNTAX BELOW
		python3 File_name.py number_of_red_balls number_of_blue_balls player depth_limit
		ex: python3 NimRB.py 6 6 computer 5
		File_name.py-> str, number_of_red_balls-> int, number_of_blue_balls->int player->str depth_limit->int
		for player rgument you must enter either human/computer(case sensitive)
		when console shows: human turn it will prompt for input like 
			Human turn Enter the pile to pick from {'Red', 'Blue'}: choose pile with either Red or Blue(case sensitive inputs)
ACS Omega: not supported

