import agent
from typing import List
from position import Position
import random
from information import Information
from numpy import sign
import csv

#### this is just printing the dictionary bc it is just not working for me
def printDict(my_dictionary) -> str:
    string = ""
    for key in my_dictionary:

        print(f"{key}: {my_dictionary[key]}")

##################################################################################################################
class Cell:
    ''' might not need this class but it could make it easier
    allows us to use Cell as a data type and store agents inside of it
    '''
    #########################################################
    def __init__(self, row: int, col: int):
        self.position:  Position = Position(row, col)
        self.contents = []     # im representing an empty cell as an empty list
                                    # for now.
    #########################################################
    def moveOut(self, agent: agent.Agent) -> bool:

        try:
            self.contents.remove(agent)
        except ValueError:
            print(f"Failed to move agent out of cell: {agent}. Agent not in cell.")
            return False                                                            #Couldn't Remove
        
        
        return True                                                                 #Removed Successfully
    #########################################################
    def moveIn(self, agent: agent.Agent) -> bool:

        if agent in self.contents:
            print(f"Failed to add agent: {agent._ID}. Agent already in cell")
            return False                                                            #Couldn't Add
        
        self.contents.append(agent)
        return True                                                                 #Added Successfully
    #########################################################
    def __str__(self):
        ''' creates and returns a string representation of this cell
        Returns:
            a string identifying the cell's row, col, and cell contents
        '''
        if self.contents == []: contents = "EMPTY"
        else:
            contents = ""
            for a in self.contents:
                print(a._ID)
                contents += "Agent " + str(a._ID)
        return f"({self.position.row}, {self.position.col}): {contents} "
    
################################################################################################################## 
class Grid:
    ''' class representing a 2-D list of cell objects'''

    slots = ('_num_rows', '_num_cols', '_agents')

    #########################################################
    def __init__(self, rows: int = 10, cols: int = 10, prop_agents: float = 1):
        ''' initializer method for grid object
        Parameters:
            num_rows:       number of rows in the grid
            num_cols:       number of columns in the grid
            prop_agents:    proportion of cells that will contain an agent when
                            the grid is created
        '''
        self._num_rows = rows
        self._num_cols = cols
        self._agents = []

        # create a rows x cols 2D list of Cell objects
        self._grid: list[list[Cell]] = \
            [ [Cell(row = r,col = c) for c in range(cols)] for r in range(rows) ]

        g_copy = [cell for row in self._grid for cell in row]
        agents = random.sample(g_copy, k = round((rows * cols - 2) * prop_agents))

        for i in agents:
            #create agent with an id and store cell location inside of it
            # append that agent object to cell contents
            new_agent = agent.Agent(i)
            i.contents.append(new_agent)
            self._agents.append(new_agent)
    #########################################################
    def getCell(self, position: Position) -> Cell:
        '''Get the cell at given position

        Parameters:
            position: Position object where the cell is
        '''
        row = position.row
        col = position.col
        cell = self._grid[row][col]
        return cell
    #########################################################
    def __str__(self) -> None:
        ''' creates a str version of the grid that shows each cell and the
        (number? names) of agents inside '''
        maze_str = ""
        for row in self._grid:
            maze_str += "|" + "|".join([str(len(cell.contents)) for cell in row]) + "|\n"
        return maze_str[:-1]  # remove the final \n
    #########################################################
    def _moveByCell(self, agent: agent.Agent, target_cell: Cell) -> bool:
        '''Handles the logic of moving a single agent from one cell to another

        Parameters:
            agent: The agent to be moved
            target_cell: The cell to which it should be moved
        Returns:
            Boolean regarding whether or not the move was successful.

        '''
        origin_cell: Cell = agent.cell

        if (origin_cell.moveOut(agent = agent)) == False:            #Try move out
            print(f"Failure to move agent: {agent}. Moving out failed")
            return False
        
        if (target_cell.moveIn(agent =  agent)) == False:            #Try move in
            print(f"Failure to move agent: {agent}. Moving In failed.")
            return False
        
        agent.cell = target_cell                                    #Update cell in agent object

        return True
    #########################################################
    def _getMoveCell(self, moving_agent: agent.Agent, origin: Position) -> Cell:
        '''Gets the cell to which agent must move considering the origin of the information

        It is used to calculate the cell to which the agent is to move.
        
        Parameters:
            agent: The agent that is moving
            origin: the position from which the information originated

        Returns:
            A target cell
        '''

        start_position: Position = moving_agent.cell.position

        #Find difference between the origin and the agent position
        row_difference = origin.row - start_position.row
        col_difference = origin.col - start_position.col

        #Get new position from adding +1, 0, or -1 to start position in each field.
        target_row = start_position.row + sign(row_difference)
        target_col = start_position.col + sign(col_difference)
        target_position = Position(row = target_row, col = target_col)

        #Get the target cell from the target position
        target_cell = self.getCell(target_position)

        return target_cell
    #########################################################
    def _moveAgent(self, moving_agent: agent.Agent, origin: Position, debugging = True):
        ''' High level logic for movement

        Moves agent given a origin of information.

        Parameters:
            agent: The agent that is moving
            origin: the position from which the information originated
        '''
        if debugging: print(f"{moving_agent}, is attempting to move. The origin of information is {origin}")
        #Get cell to be moved to
        target_cell = self._getMoveCell(moving_agent, origin)

        if debugging: print(f"Target cell will be {target_cell}")
        #Move agent
        self._moveByCell(moving_agent, target_cell)

        return
    #########################################################
    def agentsInRange(self, origin_agent: agent.Agent) -> List:
        ''' method to return a list of all the agents in within the spread radius
        of the the inputted agent
        Parameters:
            origin_agent: the agent that is spreading new information
        Returns:
            a list of all the agents within the spread radius
        '''
        # Im going to work under the assumption that a spread radius of 0
            # means that the agent can only spread information to agents in the same cell
            # and a spread of 1 means cells 1 cell away (including diagonals)
            # can change this later
        agents = []
        
        origin_cell: Cell = origin_agent.cell 
        spread_radius = origin_agent.spread_radius

        #Get integer values for the start and end of range
        row_start = max(0, origin_cell.position.row - spread_radius)
        row_end = min(self._num_rows, origin_cell.position.row + spread_radius)
        col_start = max(0, origin_cell.position.col - spread_radius)
        col_end = min(self._num_cols, origin_cell.position.col + spread_radius)
        # loop through all the cells and append all their agents to the list
        for r in range(row_start, row_end):
            for c in range(col_start, col_end):
                for a in self._grid[r][c].contents:
                    if a == origin_agent:     # don't add origin agent to the list
                        continue
                    agents.append(a)
        return agents
    #########################################################  
    def _addAgent(self, position: Position) -> None:
        # do we need this one? not sure
        # also if we we're going to do this, might want to change it so that the
            # agent object itself can be directly inputted -- might be a challenge
            # with the way I have naming set up right now tho
        ''' method to add an agent to a given cell in the grid -- Note: different
        from move agent
        Parameters:
            the position on the grid where the agents should be added
        Returns:
            None
        '''
        new_agent = agent.Agent(position)
        self._agents.append(new_agent)
        self._grid[position.row][position.col].contents.append(new_agent)
    #########################################################   
    def _findAgent(self, ID):
        ''' method to find agent in object in grid using ID number
        '''
        return self._agents[ID] 
    #########################################################
    def _share(self, agent, information, debugging = True):
        '''Reshare information with neighbours of agent agent

        Parameters:
            agent: The agent sharing information will be attempted
            information: The information which will be tried to shared with neighbors
        '''
        if debugging: print(f"{agent} is attempting to share information to:")
        share_list = self.agentsInRange(agent)                                      #Get list of agents with whom info will be shared
        for target_agent in share_list:
            if debugging: print(f"attempted with: {target_agent}")
            self._tryShare(target_agent, information, debugging = debugging)                               #Try to share it with them
        return
    #########################################################
    def _tryShare(self, target_agent: agent.Agent, information: Information, debugging = True):
        '''

        First reshares, then moves. It calls the receiveInf method on the target agent, which
        returns two different values in a dictionary. Resharing happens first, and then moving is dealt with.
        Refer to documentation for more information on this decision and its ramifications for the results.

        Paremeters:
            target_agent: The agent on which sharing of information will be attempted
            information: The information which will be tried to share with the agent
        '''
        if debugging: print(f"Someone is attempting to share with {target_agent}")
        share_results = target_agent.receiveInf(information = information)      #Share information with target agent
        is_info_accepted = share_results["is_accepted"]
        is_info_reshared = share_results["is_reshared"]
        if debugging: print(f"It resulted in {share_results}")

        if is_info_reshared: self._share(target_agent, information, debugging = debugging)             #Reshare if it will reshare
        if is_info_accepted: self._moveAgent(target_agent, information.origin.position, debugging = debugging)                          #Move if it accepted
    #########################################################
    def _oneTurn(self, origin_agent: agent.Agent, debugging = True):
        '''Runs a single "Turn" of a round (of a simulation)

        Paremeters:
            origin_agent: The agent that attempts to make the information
        '''

        info_generated = origin_agent.isInfGen()                                        #Generate info if it will be generated
        if info_generated:
            if debugging: print("Info generated, attempting to share")
            self._share(origin_agent, info_generated, debugging = debugging)                    #If information will be generated, share

        if debugging: print(f"{origin_agent} turn ended")
        return
    #########################################################
    def _oneRound(self, debugging = False):
        '''Runs a single "round" of the simulation

        A round is divided in multiple different turns. This function
        generates a "turn" list and proceeds to call the _oneTurn function
        in the random order generated

        '''
        if debugging: print("In one round")
        agents_left = self._agents.copy()

        if debugging: print(len(agents_left))
        while len(agents_left) != 0:

            variate = random.random()
            num_remaining = len(agents_left) - 1
            next_index = round(variate * num_remaining)
            next_agent = agents_left[next_index]
            agents_left.remove(next_agent)
            self._oneTurn(next_agent, debugging = debugging)
        
        return
    #########################################################
    def run(self, num_rounds = 1, debugging = False):
        ''' Function to be called when the state of the simulation is to advance

        Parameters:
            num_rounds: The amount of rounds to move forward
        '''
        if debugging: print("In Run Rounds")
        for i in range(0,num_rounds):
            print(f"Running Round {i}")
            self._oneRound(debugging = debugging)
        return
    #########################################################
    def toCSV(self, filename, debugging = False):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)

            for row in self._grid:
                pop_list = []
                for cell in row:
                    pop_list.append(len(cell.contents))
                writer.writerow(pop_list)
        return 