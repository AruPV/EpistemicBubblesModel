from typing import List, NamedTuple, Optional
import random


class Agent:
    ''' class for each of the individual agents in the simulation
    allows us to store information about each agent inside the object
    '''
    def __init__(self, ID, location):
        self._ID = ID         # probably can just be a number
        self._location = location   # row col position of the cell the agent is in
        self._information = None

        # things we can change later -- should add rates later
        self._new_info_rate = None  # the chance each agent has of generating
                                        # new information
        self._spread_radius = None  # the radius outside the cell information
                                        # can spread
        self._acceptance_rate = None # how likely an agent is to accept new
                                        # information

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

    slots = ('_num_rows', '_num_cols')

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

        # create a rows x cols 2D list of Cell objects
        self._grid: list[list[Cell]] = \
            [ [Cell(r,c) for c in range(cols)] for r in range(rows) ]

        g_copy = [cell for row in self._grid for cell in row]
        agents = random.sample(g_copy, k = round((rows * cols - 2) * prop_agents))
        id_names = 0    # can't think of a better way to do this in my brain state
                        # want to give each agent a name
        for i in agents:
            #create agent with an id and store cell location inside of it
            # append that agent object to cell contents
            new_agent = Agent(id_names, i._position)
            i._contents.append(new_agent)
            id_names += 1

    def __str__(self) -> None:
        ''' creates a str version of the grid that shows each cell and the
        (number? names) of agents inside '''
        maze_str = ""
        for row in self._grid:  # row : List[Cell]
            maze_str += "|" + "|".join([str(len(cell._contents)) for cell in row]) + "|\n"
        return maze_str[:-1]  # remove the final \n

def main():
    g = Grid()
    print(g)



main()
