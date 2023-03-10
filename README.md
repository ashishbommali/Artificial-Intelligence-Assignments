# Artificial-Intelligence-Assignments
EXPENSE 8 PUZZLE PROBLEM 


Assignment 1
Uninformed & Informed Search

The task is to build an agent to solve a modifed version of the 8 puzzle problem (called the Expense 8 puzzle problem). The task is still to take a 3X3 grid on which 8 tiles have been placed, where you can only move one tile at a time to an adjacent location (as long as it is blank) and figure out the order in which to move the tiles to get it to a desired configuration. However now the number on the tile now also represents the cot of moving that tile (moving the tile marked 6 costs 6).

Our program should be called expense_8_puzzle and the command line invocation should follow the following format:

expense_8_puzzle.py <start-file> <goal-file> <method> <dump-flag>
<start-file> and <goal-file> are required.
<method> can be
bfs - Breadth First Search
ucs - Uniform Cost Search
dfs - Depth First Search
dls - Depth Limited Search (Note: Depth Limit will be obtained as a Console Input)
ids - Iterative Deepening Search 
greedy - Greedy Seach
a* - A* Search (Note: if no <method> is given, this should be the default option)
If <dump-flag>  is given as true, search trace is dumped for analysis in trace-<date>-<time>.txt (Note: if <dump-flag> is not given, assume it is false)
search trace contains: fringe and closed set contents per loop of search(and per iteration for IDS), counts of nodes expanded and nodes
Both start file and goal file need to follow the format as shown here:
Sample Start file
Sample Goal file
Your output needs to follow the format given in the example here:

For:
expense_8_puzzle.py start.txt goal.txt a* true

The output should appear as follows:

Nodes Popped: 97
Nodes Expanded: 64
Nodes Generated: 173
Max Fringe Size: 77
Solution Found at depth 12 with cost of 63.
Steps:
Move 7 Left
Move 5 Up
Move 8 Right
Move 7 Down
Move 5 Left
Move 6 Down
Move 3 Right
Move 2 Right
Move 1 Up
Move 4 Up
Move 7 Left
Move 8 Left

Note: for both greedy and A* search you need to come up with a acceptable heuristic (Hint: Consider a modified version of h2)

____________________________________________________________________________________________________________________________________________________________

Programming Language		:  Python

Structure of the code: 		-->	The code strats from calling main() which instantiates class Expense8Puzzle with a constructor for taking start and goal files and here I 
					have implemented search algorithms such as DFS, BFS, DLS, IDS, UCS, A*, GREEDY ARE IMPLEMENTED along with few helper fucntion to read 
					files(start and goal text files), getting empty tile position, movements, generating successors, and in  addition to these I have implemented 
					few other methods as helpers (heuristic, finding path cost along the path from start to goal, movements for tile being moved with respect to 
					zero tile), (swap, getting next states, read start and goal file state) for BFS alone.

			     	-->	Implemented the code in different function to get a clear understanding at a first glance.

				-->	The different files used are: start.txt, goal.txt, dump.txt, EXPENSE_8_PUZZLE.py, 

EXPENSE_8_PUZZLE.py:		-->	This contains the entire code main method, helper functions, and search methods to solve the puzzle

How to run the code?		-->	Uninformed & Informed Search

The command line arguments should follow format like in the below
PythonFilename.py <start-file> <goal-file> <method> <dump-flag>

•	<start-file> and <goal-file> are required.
•	<method> can be
o	bfs - Breadth First Search
o	ucs - Uniform Cost Search
o	dfs - Depth First Search
o	dls - Depth Limited Search (Note: Depth Limit will be obtained as a Console Input) you will be promted for an input depth limit
o	ids - Iterative Deepening Search 
o	greedy - Greedy Seach
o	a* - 
•	If <dump-flag>  either ‘true’ or ‘false’
command line syntax ex: python3 EXPENSE_8_PUZZLE.py start.txt goal.txt a* true

versions: 
python version : 3.11.2 (supports 64 bit system, may work on 32 bit too)
pip version : 22.3.1
numpy version : 1.24.2

modules to be installed and imported: 
import sys
from queue import Queue, PriorityQueue
from queue import LifoQueue
import numpy as np

Note: 
The input files which are given in the command line arguments should be located in the same folder where the code is stored.
Dump file must be closed and opened every time after excecuting one search method for new data to be shown in the file.
DLS and IDS both prompt for depth limit before running the algorithm.
Sometime the terminal will not be able t show the entire out as few algorithms might use more buffer space.
tab space and exact format of output may vary but details are entailed as the way they are.
						
