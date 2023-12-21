________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
CODE STRUCTURE:
	The code is written in python 3.11.3
	Code starts with main driver code which calls the class BayesNets.
	BayesNets class contains methods such as __init__(), calculate_probabilities(), calculateJPD()
	
	__init__()  --> contructor takes dataset as argument and initialises the objects 
	
	calculate_probabilities() --> to learn the conditonal probabilty tables for the bayesian network from the training data and to calculate the probability metrices/tables over the training data for Task 1
	
	calculateJPD() -->  to calculate any value in the JPD for this domain using the conditional probabilty distributions calculated in Task 1 for Task2
	
________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
HOW TO RUN THE CODE:
	Before running the code make sure your in the same directory where the src code(bnet.py) and text file(training_data.txt) are in.
	Please follow the commandline below invokations with case sensitiveness.
	to compile and the run the code follow the invokations below

	for task 1 -->  python bnet.py <training_data>
			python filename.py training_data.txt
			ex: python bnet.py training_data.txt

	for task 2 -->  please enter the excatly 4 variables
			python bnet.py <training_data> <Bt/Bf> <Gt/Gf> <Ct/Cf> <Ft/Ff>
			python filename.py training_data.txt Bt Gf Ct Ff
		        ex: python bnet.py training_data.txt Bt Gf Ct Ff
			ex: python bnet.py training_data.txt Bt Gf Ct Ft
			ex: python bnet.py training_data.txt Bt Gf Cf Ff
			ex: python bnet.py training_data.txt Bt Gt Cf Ff
			ex: python bnet.py training_data.txt Bf Gf Ct Ff
________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
OUTPUT:
	you can find the outputs in terminal or stdout.
________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
REQUIRED INSTALLATIONS AND VERSIONS USED AND IMPORTS:
	Make sure to install python version-> 3.11.3 64bit 
	pip version-> 23.1.2
	install and import numpy
	import sys

________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
