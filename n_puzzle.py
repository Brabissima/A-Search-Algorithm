import numpy as np
from state import State


class NPuzzleInstance:

    def __init__(self, m=3, n=None, initial_state=None, goal_state=None):
        '''
        Creates a new instance of the N-Puzzle game, where m is the
        number of rows and n is the number of columns. If n is not provided,
        n will be equals to m. The user can provide an initial_state and a
        goal_state, if they're not provided, the goal_state state will be
        the default and initial_state will be random
        '''
        self.m = m
        self.n = n if n else m  # if n is None, set n = m
        self.neighbors_indexes = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        # If user wanna pass an especific goal_state
        if goal_state:
            self.goal_state = goal_state
        else:
            self.goal_state = self.__build_goal_state()

        # If user wanna pass an especific initial_state
        if initial_state:
            matrix = np.asarray(initial_state)
            self.initial_state = State(matrix)
            self.initial_state.heuristic_value = self.heuristic(self.initial_state)
        else:
            self.initial_state = self.__build_initial_state()
            self.initial_state.heuristic_value = self.heuristic(self.initial_state)

        self.current_state = self.initial_state

    def __build_initial_state(self):
        '''
        Generates a random matrix m x n.Called when the user does not provide
        an initial_state. The values of this matrix belongs [0, m*n)
        * 0 represents the empty place
        '''
        c_state = np.arange(self.m * self.n)
        np.random.shuffle(c_state)
        c_state = np.asarray(c_state).reshape((self.m, self.n))

        return State(c_state)

    def __build_goal_state(self):
        '''
        Generates the default matrix m x n to be the goal_state.
        The default goal_state is:
        |    1    ,     2    , ...,   n |
        |   n+1   ,    n+2   , ..., 2*n |
        |  2*n+1  ,   2*n+2  , ..., 3*n |
                           .
                           .
                           .
        |(m-1)*n+1, (m-1)*n+2, ...,   0 |
        * 0 represents the empty place
        '''
        g_state = np.arange(self.m * self.n).reshape((self.m, self.n))
        g_state = np.roll(g_state, -1)
        # The line above shifts the 0 (empty space) to the last position
        # Ex.: np.roll([0, 1, 2, ..., m*n-1], -1) --> [1, 2, ..., m*n-1, 0]
        return State(g_state)

    def heuristic(self, some_state=None):
        '''
        Calculates the number of steps required for each cell out of place to be
        in place compared to his position in goal_state. The possible movements
        are UP, DOWN, LEFT and RIGHT.
        '''
        # If some_state is None, set it to self.current_state
        some_state = some_state if some_state is not None else self.current_state

        total_distance = 0

        for i in range(self.m):
            for j in range(self.n):
                if some_state[i, j] != self.goal_state[i, j]:

                    g_i, g_j = self.goal_state.get_indexes(some_state[i, j])

                    dx = abs(i - g_i)
                    dy = abs(j - g_j)

                    total_distance += dx + dy

        return total_distance

    def is_solved(self):
        '''
        Check if the current_state is equals to the goal_state
        '''
        return self.current_state == self.goal_state

    def neighbors(self):
        '''
        Iterates over all possible neighbors of current_state, considering the possible
        movements and the size of the grid (matrix).
        '''
        x, y = self.current_state.get_indexes(0)

        for (i, j) in self.neighbors_indexes:
            if 0 <= x + i < self.m and 0 <= y + j < self.n:
                    neigh = State(self.current_state.matrix)
                    neigh[x + i, y + j], neigh[x, y] = neigh[x, y], neigh[x + i, y + j]

                    neigh.greedy_value = self.current_state.greedy_value + 1
                    neigh.heuristic_value = self.heuristic(neigh)

                    yield neigh

    def __str__(self):

        return 'Dimensions: {}\nInitial State:\n{}\n{}\n\nGoal State:\n{}\n{}\n'.format(
            self.goal_state.shape,
            self.initial_state, self.initial_state.get_func_values_as_str(),
            self.goal_state, self.goal_state.get_func_values_as_str()
        )