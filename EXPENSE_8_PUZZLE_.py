import sys
from queue import Queue, PriorityQueue
from queue import LifoQueue
import numpy as np
# ________________________________________________________________________________________________________________________________________
#TO STORE THE RESULT MATRIX AS NUMPY ARRAYS WHICH IS THE DIFFERENCES OF THE PAIRWISE MATRIX SUBTRACTIONS FROM THE START STATE TO GOAL STATE
result = []

# ________________________________________________________________________________________________________________________________________
# A HEURISTIC FUNCTION TO CALCULATE MANHATTAN DISTANCE FOR ASTAR
def heuristic(state, goal_state):

    total_distance = 0
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] != 0:
                row, col = divmod(state[i][j] - 1, len(state))
                total_distance += abs(row - i) + abs(col - j)
    return total_distance
# ________________________________________________________________________________________________________________________________________

# TO FIND THE COST OF PATH FORM START STATE TO GOAL STATE
def findPathCost(path):

    matrices = path
    total_path_cost = 0

    for i in range(0, len(matrices)-1):
        result_matrix = [[matrices[i][j][k] - matrices[i+1][j][k]
                          for k in range(len(matrices[i][0]))] for j in range(len(matrices[i]))]

        result.append(np.array(result_matrix))
        
        positive_matrix = [[result_matrix[j][k] for k in range(len(
            result_matrix[0])) if result_matrix[j][k] > 0] for j in range(len(result_matrix))]

        #TO FIND THE PATH COST FROM START STATE TO GOAL STATE
        for row in positive_matrix:
            for elem in row:
                total_path_cost += elem

    return total_path_cost
# ________________________________________________________________________________________________________________________________________

# MOVEMENTS FOR TILE
def movementsNumberedTiles():

    for array in result:
        rows, cols = np.where(array < 0)
        for row, col in zip(rows, cols):
            neg_row, neg_col = row, col
            neg_val = array[row, col]
            pos_rows, pos_cols = np.where(array > 0)
            for pos_row, pos_col in zip(pos_rows, pos_cols):
                pos_val = array[pos_row, pos_col]
                if pos_row == neg_row and pos_col > neg_col:
                    print(f"move {abs(neg_val)} left")
                elif pos_row == neg_row and pos_col < neg_col:
                    print(f"move {abs(neg_val)} right")
                elif pos_col == neg_col and pos_row < neg_row:
                    print(f"move {abs(neg_val)} down")
                elif pos_col == neg_col and pos_row > neg_row:
                    print(f"move {abs(neg_val)} up")

# ________________________________________________________________________________________________________________________________________

# BFS READ STATE FILE FUNCTION
def read_state_file_BFS(filename):
    state = []
    with open(filename, 'r') as f:
        #LOOPING 3 ROWS FROM THE TEXT FILE BY OMITING THE LAST LINE "END OF THE FILE"
        for i in range(3):
            line = f.readline()
            state.append(list(line.split()))

    state = tuple(int(num) for sublist in state for num in sublist)
    return np.array(state)
# ________________________________________________________________________________________________________________________________________

# BFS GET NEXT STATES
def get_next_states(state):

    next_states = []
    empty_tile_pos = state.index(0)
    if empty_tile_pos not in [0, 1, 2]:
        next_states.append(
            ('up', swap(state, empty_tile_pos, empty_tile_pos - 3)))

    if empty_tile_pos not in [6, 7, 8]:
        next_states.append(
            ('down', swap(state, empty_tile_pos, empty_tile_pos + 3)))

    if empty_tile_pos not in [0, 3, 6]:
        next_states.append(
            ('left', swap(state, empty_tile_pos, empty_tile_pos - 1)))

    if empty_tile_pos not in [2, 5, 8]:
        next_states.append(
            ('right', swap(state, empty_tile_pos, empty_tile_pos + 1)))

    return next_states
# ________________________________________________________________________________________________________________________________________

# SWAP FOR BFS
def swap(state, i, j):

    new_state = list(state)
    new_state[i], new_state[j] = new_state[j], new_state[i]

    return tuple(new_state)
# ________________________________________________________________________________________________________________________________________

# Puzzle class
class Expense8Puzzle:

    # CLASS CONSTRUCTOR FOR START AND GOAL STATE
    def __init__(self, start_file, goal_file):
        self.start = self.read_state_file(start_file)
        self.goal = self.read_state_file(goal_file)
        self.dim = len(self.start)
        # actions: right, down, left, up
        self.actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # TO READ START AND GOAL FILE
    def read_state_file(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            lines.pop()
            return [[int(num) for num in line.split()] for line in lines]

    # FINDING THE ZERO IN THE 8 PUZZLE
    def get_empty_tile_position(self, state):
        for i in range(self.dim):
            for j in range(self.dim):
                if state[i][j] == 0:
                    return (i, j)

    # MOVEMENT OF THE TILE FOR GENEARATION OF NEXT STATE
    def move(self, state, action):
        empty_tile_position = self.get_empty_tile_position(state)
        next_pos = (empty_tile_position[0] + action[0],
                    empty_tile_position[1] + action[1])
        if 0 <= next_pos[0] < self.dim and 0 <= next_pos[1] < self.dim:
            # create a deep copy of the state
            next_state = [row[:] for row in state]
            next_state[empty_tile_position[0]][empty_tile_position[1]
                                               ] = state[next_pos[0]][next_pos[1]]
            next_state[next_pos[0]][next_pos[1]] = 0
            return next_state
        else:
            return None

    # GENEREATING SUCCESSORS OF A GIVEN STATE
    def get_successors(self, state):

        successors = []
        zero_row, zero_col = self.get_empty_tile_position(state)
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for move in moves:
            new_row = zero_row + move[0]
            new_col = zero_col + move[1]

            if 0 <= new_row < self.dim and 0 <= new_col < self.dim:
                new_state = [row[:] for row in state]
                new_state[zero_row][zero_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[zero_row][zero_col]
                cost = new_state[new_row][new_col]
                successors.append((new_state, cost))

        return successors
        
# ________________________________________________________________________________________________________________________________________
   
    # BREADTH FIRST SEARCH IMPLEMENTATION FOR EXPENSE_8_PUZZLE PROBLEM
    def breadthFirstSearch(self, start_state, goal_state):

        c = []
        fringe = Queue()
        visited = set()
        path = []
        nodes_popped = 0
        nodes_expanded = 0
        nodes_generated = 1
        max_fringe_size = 1
        cost = 0

        fringe.put((start_state, []))

        while not fringe.empty():

            current_state, path = fringe.get()
            nodes_popped += 1

            p = path

            c.append(current_state)

            if (current_state == goal_state):

                return {
                    'path': path,
                    'nodes_popped': nodes_popped,
                    'nodes_expanded': nodes_expanded,
                    'nodes_generated': nodes_generated,
                    'max_fringe_size': max_fringe_size,
                    'depth': len(path),
                    'visited': visited,
                    'fringe': fringe,
                    'path_cost': len(path),
                    'c': c,
                }

            visited.add(current_state)

            for move, next_state in get_next_states(current_state):

                nodes_expanded += 1
                nodes_generated += 1
                if next_state not in visited:
                    fringe.put((next_state, path + [move]))
                    visited.add(next_state)
                    max_fringe_size = max(max_fringe_size, fringe.qsize())

        return None
# ________________________________________________________________________________________________________________________________________
   
    # DPETH FIRST SEARCH IMPLEMENTATION FOR EXPENSE_8_PUZZLE PROBLEM
    def depthFirstSearch(self, flag):

        start = self.start
        fringe = []
        closed = set()
        path = []
        cost = 0
        nodes_popped = 0
        nodes_generated = 0
        nodes_expanded = 1
        max_fringe_size = 1

        path.append(self.start)
        fringe.append((self.start, path, cost))

        while fringe:
            state, path, cost = fringe.pop()
            nodes_popped += 1

            if state == self.goal:
                cost_of_path = findPathCost(path)

                print("Nodes popped: ", nodes_popped)
                print("Nodes expanded: ", nodes_expanded)
                print("Nodes generated: ", nodes_generated)
                print("Max Fringe Size: ", max_fringe_size)
                print("Solution Found at depth ", len(
                    path), "with cost of ", cost_of_path)
                print("steps: ")
                movementsNumberedTiles()

                if flag == "true":
                    with open('dump.txt', 'w') as f:
                        f.write(f"Nodes popped: {nodes_popped}\n")
                        f.write(f"Nodes expanded: {nodes_expanded}\n")
                        f.write(f"Nodes generated: {nodes_generated}\n")
                        f.write(f"Path cost: {cost_of_path}\n")
                        f.write(f'closed: {closed}\n')
                        f.write("Path:\n")
                        f.write(f':{start}\n')
                        for line in path:
                            f.write(" ".join(str(num) for num in line) + "\n")
                        f.write(f'Fringe: {fringe}\n')

                        f.close()
                return

            closed.add(tuple(map(tuple, state)))
            # add successors in reverse order to simulate DFS
            for successor, _ in self.get_successors(state)[::-1]:
                if tuple(map(tuple, successor)) not in closed:
                    nodes_generated += 1
                    nodes_expanded += 1
                    fringe.append((successor, path + [successor], cost + 1))
                    max_fringe_size = max(max_fringe_size, len(fringe))
        return None
# ________________________________________________________________________________________________________________________________________
   
    # DLS IMPLEMTATION FOR EXPENSE_8_PUZZLE PROBLEM
    def depthLimitedSearch(self, limit, flag):

        fringe = LifoQueue()
        closed = set()
        path = []
        cost = 0
        nodes_popped = 0
        nodes_generated = 0
        nodes_expanded = 1
        max_fringe_size = 1

        path.append(self.start)
        fringe.put((self.start, path, cost, 0))
        while not fringe.empty():

            state, path, cost, depth = fringe.get()
            nodes_popped += 1

            if state == self.goal:

                cost_of_path = findPathCost(path)
                movementsNumberedTiles()
                print("Nodes Popped: ", nodes_popped)
                print("Nodes Expanded: ", nodes_expanded)
                print("Nodes Generated: ", nodes_generated)
                print("Max Fringe Size: ", max_fringe_size)
                print("Solution Found at depth ", depth,
                      " with cost of", cost_of_path, ".")
                print("steps: \t")
                movementsNumberedTiles()

                if flag == 'true':
                    with open('dump.txt', 'w') as f:
                        f.write(f"Nodes popped: {nodes_popped}\n")
                        f.write(f"Nodes expanded: {nodes_expanded}\n")
                        f.write(f"Nodes generated: {nodes_generated}\n")
                        f.write(f'closed: {closed}\n')
                        f.write(f"Path cost: {cost}\n")
                        f.write("Path:\n")
                        for line in path:
                            f.write(" ".join(str(num) for num in line) + "\n")
                return

            if depth == limit:
                continue

            closed.add(tuple(map(tuple, state)))
            for successor, _ in self.get_successors(state):
                if tuple(map(tuple, successor)) not in closed:
                    nodes_generated += 1
                    nodes_expanded += 1
                    fringe.put(
                        (successor, path + [successor], cost + 1, depth + 1))
                    max_fringe_size = max(max_fringe_size, fringe.qsize())

# ________________________________________________________________________________________________________________________________________
   
   #ITERATIVE DEEPENING SEARCH USING DEPTH LIMITED SEARCH
    def iterativeDeepeningSearch(self, depth_limit, flag):
        for depth in range(depth_limit):
            if self.depthLimitedSearch(depth, flag):
                return True
        return False
# ________________________________________________________________________________________________________________________________________
   
    # UNIFORM COST SEARCH IMPLEMENTATION FOR EXPENSE_8_PUZZLE PROBLEM
    def uniformCostSearch(self, flag):

        start = self.start
        fringe = PriorityQueue()
        closed = set()
        path = []
        cost = 0
        nodes_popped = 0
        nodes_generated = 0
        max_fringe_size = 1
        nodes_expanded = 1

        path.append(self.start)
        fringe.put((cost, self.start, path))
        while not fringe.empty():
            cost, state, path = fringe.get()
            nodes_popped += 1
            nodes_generated += 1

            if state == self.goal:

                cost_of_path = findPathCost(path)

                print("Nodes popped: ", nodes_popped)
                print("Nodes expanded: ", nodes_expanded)
                print("Nodes generated: ", nodes_generated)
                print("Max Fringe Size: ", max_fringe_size)
                print("Solution Found at depth ", len(
                    path), "with cost of ", cost_of_path)
                print("steps: ")
                movementsNumberedTiles()

                if flag == "true":
                    with open('dump.txt', 'w') as f:
                        f.write(f"Nodes popped: {nodes_popped}\n")
                        f.write(f"Nodes expanded: {nodes_expanded}\n")
                        f.write(f"Nodes generated: {nodes_generated}\n")
                        f.write(f"Path cost: {cost_of_path}\n")
                        f.write(f'closed: {closed}\n')
                        f.write("Path:\n")
                        f.write(f':{start}\n')
                        for line in path:
                            f.write(" ".join(str(num) for num in line) + "\n")
                        f.write(f'Fringe: {fringe}\n')
                        f.close()
                return

            closed.add(tuple(map(tuple, state)))
            for successor, action_cost in self.get_successors(state):
                if tuple(map(tuple, successor)) not in closed:
                    nodes_generated += 1
                    nodes_expanded += 1
                    fringe.put(
                        (cost + action_cost, successor, path + [successor]))
                    max_fringe_size = max(max_fringe_size, fringe.qsize())


# ________________________________________________________________________________________________________________________________________
   
    # ASTAR SEARCH IMPLEMENTATION FOR EXPENSE_8_PUZZLE PROBLEM
    def aStar(self, start_state, goal_state, flag):

        fringe = PriorityQueue()
        closed = set()
        path = []
        cost = 0
        nodes_popped = 0
        nodes_generated = 0
        nodes_expanded = 1
        max_fringe_size = 1
        depth = 0

        path.append(self.start)
        h = heuristic(self.start, self.goal)
        fringe.put((h, self.start, path, cost))

        while not fringe.empty():

            max_fringe_size = max(max_fringe_size, fringe.qsize())
            _, state, path, cost = fringe.get()
            nodes_popped += 1

            if state == self.goal:
                cost_of_path = findPathCost(path)

                depth = cost
                break

            closed.add(tuple(map(tuple, state)))

            for successor, _ in self.get_successors(state):

                if tuple(map(tuple, successor)) not in closed:
                    nodes_generated += 1
                    nodes_expanded += 1
                    new_cost = cost + 1
                    h = heuristic(successor, self.goal)
                    fringe.put((new_cost + h, successor,
                               path + [successor], new_cost))
                    max_fringe_size = max(max_fringe_size, fringe.qsize())

        print("Nodes Popped: ", nodes_popped)
        print("Nodes Expanded: ", nodes_expanded)
        print("Nodes Generated: ", nodes_generated)
        print("Max Fringe Size: ", max_fringe_size)
        print("Solution Found at depth ", depth,
              " with cost of", cost_of_path, ".")
        print("steps: \t")
        movementsNumberedTiles()

        with open('dump.txt', 'w') as f:
            if flag == 'true':
                f.write(f'Nodes generated: {nodes_generated}\n')
                f.write(f'Nodes popped: {nodes_popped}\n')
                f.write(f'Nodes expanded: {nodes_expanded}\n')
                f.write(f'Max_Fringe_size: {max_fringe_size}\n')
                f.write(f'Path:{path}\n')
                f.write(f'cost of path : {cost_of_path} \n')
                f.write(f"Solution result at depth:{depth}\n")
                f.write(f'Closed: {closed}\n')
                f.close()

        return None
# ________________________________________________________________________________________________________________________________________

#DRIVER CODE 
def main():

    start_file = sys.argv[1]
    goal_file = sys.argv[2]
    method = sys.argv[3]
    flag = sys.argv[4]

    classObj = Expense8Puzzle(start_file, goal_file)

    start_state = classObj.read_state_file(start_file)
    goal_state = classObj.read_state_file(goal_file)

    if method == "bfs":

        sS = read_state_file_BFS(start_file)
        gS = read_state_file_BFS(goal_file)

        result = classObj.breadthFirstSearch(tuple(sS), tuple(gS))

        if result:

            print("Nodes Popped:", result["nodes_popped"])
            print("Nodes Expanded:", result["nodes_expanded"])
            print("Nodes Generated:", result["nodes_generated"])
            print("Max Fringe Size:", result["max_fringe_size"])
            print("Solution Found at depth:",
                  result["depth"], "with cost of ", result["path_cost"])

            for i in result["path"]:
                print("    ", "move 0 ", i)

            with open('dump.txt', 'w') as f:

                if flag == 'true':
                    f.write(f'Path: {result["path"]}\n')
                    f.write(f'Nodes Popped: {result["nodes_popped"]}\n')
                    f.write(f'Nodes Expanded: {result["nodes_expanded"]}\n')
                    f.write(f'Nodes Generted: {result["nodes_generated"]}\n')
                    f.write(f'Max Fringe Size: {result["max_fringe_size"]}\n')
                    f.write(f'Solution found at depth: {result["depth"]}\n')
                    f.write(f'steps: \n')

                    for i in result["path"]:
                        f.write(f'    move 0 {i} \n')

                    f.write(f'path_cost: {result["path_cost"]}\n')
                    f.write(f'visited: {result["visited"]}\n')
                    f.write(f'current states: {result["c"]} \n')
                    f.close()
                else:
                    f.write('flag is false hence no dump details')
        else:
            print('No solution found.')

    if method == "dfs":
        result = classObj.depthFirstSearch(flag)

    if method == "ucs":
        result = classObj.uniformCostSearch(flag)

    if method == "dls":
        print("enter depth limit: ")
        limit = int(input())
        result = classObj.depthLimitedSearch(limit, flag)

    if method == "ids":
        print("Enter depth limit: ")
        depth_limit = int(input())
        result = classObj.iterativeDeepeningSearch(depth_limit, flag)

    if method == "a*" or method == None or method == 'none':
        classObj.aStar(start_state, goal_state, flag)

    if method == "greedy":
        result = classObj.greedy(start_state, goal_state, flag)
# ________________________________________________________________________________________________________________________________________
#MINVOKING MAIN METHOD 
if __name__ == '__main__':
    main()
