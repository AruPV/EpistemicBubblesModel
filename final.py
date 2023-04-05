from typing import List, NamedTuple, Optional
import random


class Agent:
    ''' class for each of the individual agents in the simulation
    allows us to store information about each agent inside the object
    '''
    def __init__(self, ID, location):
        self._ID = ID         # probably can just be a number
        self._position = location   # row col position of the cell the agent is in
        self._information = None

        # things we can change later -- should add rates later
        self._new_info_rate = None  # the chance each agent has of generating
                                        # new information
        self._spread_radius = 2  # the radius outside the cell information
                                        # can spread
        self._acceptance_rate = None # how likely an agent is to accept new
                                        # information

    def __eq__(self, other: 'Agent') -> bool:
        ''' Boolean method to indicate whether a given Agent is equal to this agent
        Returns:
            True if this agent and the other agent are the same, False o/w
        '''
        return self._position.row == other._position.row and \
               self._position.col == other._position.col and \
               self._ID == other._ID

    def __str__(self) -> None:
        ''' creates str version of agent object '''
        return f"Agent {str(self._ID)}, Location: ({self._position.row}, {self._position.col})"

class Information:
    ''' allows us to use information as a class
    might be useful later if we want to have different kinds of information
    with different characterists
    '''
    # how are we doing information in the base case? since there is only one kind
    # of information right now, do we represent information as an integer value if
    # an agent has more than one 'information'
    # or do we have give a name to each piece of generated information and store
    # them seperately?
    pass

class Position(NamedTuple):
    ''' just allows us to use .row and .col rather than the less-easy-to-read
        [0] and [1] for accessing values
        yoinked this from the last class i had with Barry
    '''
    row: int
    col: int

class Cell:
    ''' might not need this class but it could make it easier
    allows us to use Cell as a data type and store agents inside of it
    '''
    def __init__(self, row: int, col: int):
        self._position:  Position = Position(row, col)
        self._contents = []     # im representing an empty cell as an empty list
                                    # for now

    def __str__(self):
        ''' creates and returns a string representation of this cell
        Returns:
            a string identifying the cell's row, col, and cell contents
        '''
        if self._contents == []: contents = "EMPTY"
        else:
            contents = ""
            for a in self._contents:
                print(a._ID)
                contents += "Agent " + str(a._ID)
        return f"({self._position.row}, {self._position.col}): {contents} "


class Grid:
    ''' class representing a 2-D list of cell objects'''

    slots = ('_num_rows', '_num_cols', '_agents')

    def __init__(self, rows: int = 10, cols: int = 10, prop_agents: float = 0.3):
        ''' initializer method for grid object
        Parameters:
            rows:           number of rows in the grid
            cols:           number of columns in the grid
            prop_agents:    proportion of cells that will contain an agent when
                            the grid is created
        '''
        self._num_rows = rows
        self._num_cols = cols
        self._agents = {}

        # create a rows x cols 2D list of Cell objects
        self._grid: list[list[Cell]] = \
            [ [Cell(r,c) for c in range(cols)] for r in range(rows) ]

        g_copy = [cell for row in self._grid for cell in row]
        agents = random.sample(g_copy, k = round((rows * cols - 2) * prop_agents))

        for i in agents:
            #create agent with an id and store cell location inside of it
            # append that agent object to cell contents
            name = len(self._agents) + 1
            new_agent = Agent(name, i._position)
            i._contents.append(new_agent)
            self._agents[name] = new_agent
            print(i)
        printDict(self._agents)

    def __str__(self) -> None:
        ''' creates a str version of the grid that shows each cell and the
        (number? names) of agents inside '''
        maze_str = ""
        for row in self._grid:
            maze_str += "|" + "|".join([str(len(cell._contents)) for cell in row]) + "|\n"
        return maze_str[:-1]  # remove the final \n

    def _moveAgent(self):
        pass

    def _agentsInRange(self, origin: Agent) -> List:
        ''' method to return a list of all the agents in within the spread radius
        of the the inputted agent
        Parameters:
            origin: the agent that is spreading new information
        Returns:
            a list of all the agents within the spread radius
        '''
        # Im going to work under the assumption that a spread radius of 0
            # means that the agent can only spread information to agents in the same cell
            # and a spread of 1 means cells 1 cell away (including diagonals)
            # can change this later
        agents = []
        if origin._spread_radius == 0:
            for a in self._grid[origin._position.row][origin._position.col]._contents:
                if a != origin:
                    agents.append(a)
        else:
            # row_start
            if origin._position.row - origin._spread_radius < 0:
                row_start = 0
            else: row_start = origin._position.row - origin._spread_radius
            # row_end
            if origin._position.row + origin._spread_radius > self._num_rows:
                row_end = self._num_rows
            else: row_end = origin._position.row + origin._spread_radius + 1
            # col_start
            if origin._position.col - origin._spread_radius < 0:
                col_start = 0
            else: col_start = origin._position.col - origin._spread_radius
            # col_end
            if origin._position.col + origin._spread_radius > self._num_cols:
                col_end = self._num_cols
            else: col_end = origin._position.col + origin._spread_radius + 1

            # loop through all the cells and append all their agents to the list
            for r in range(row_start, row_end):
                for c in range(col_start, col_end):
                    for a in self._grid[r][c]._contents:
                        if a == origin:     # don't add origin agent to the list
                            continue
                        agents.append(a)
        return agents

    def _addAgent(self, position: Position) -> None:
        # do we need this one? not sure
        # also if we we're going to do this, might want to change it so that the
            # agent object itself can be directly inputted -- might be a challenge
            # with the way I have naming set up right now tho
        ''' method to add an agent to a given cell in the grid -- NOTE: different
        from move agent
        Parameters:
            the position on the grid where the agents should be added
        Returns:
            None
        '''
        new_agent = Agent(len(self._agents) + 1, position)
        self._agents[len(self._agents) + 1] = new_agent
        self._grid[position.row][position.col]._contents.append(new_agent)

    def _findAgent(self, ID):
        ''' method to find agent in object in grid using ID number
        '''
        return self._agents[ID]

#### this is just printing the dictionary bc it is just not working for me
def printDict(my_dictionary) -> str:
    string = ""
    for key in my_dictionary:

        print(f"{key}: {my_dictionary[key]}")

def main():
    random.seed(42)
    g = Grid()
    print(g)

    ################# testing addAgent
    p = Position(1,1)
    g._addAgent(p)
    print(len(g._agents))
    print(g)

    #agent30 = g._findAgent(30)
    #print(g._agentsInRange(agent30)[0])
    ############## testing agentInRange when spread radius is 1
    agent9 = g._findAgent(9)
    p2 = Position(1,3)
    g._addAgent(p2)
    #test = g._agentsInRange(agent9)
    #for a in test:
        #print(a)

    ############ testing agentInRange when spread radius is 2
    test = g._agentsInRange(agent9)
    for a in test:
        print(a)



main()
