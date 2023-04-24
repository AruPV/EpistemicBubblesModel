import agent
from typing import List
from position import Position
import random
from information import Information

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

        if self.contents.find(agent) == -1:
            print(f"Failed to move agent out of cell: {agent._ID}. Agent not in cell.")
            return False        #Couldn't Remove
        
        self.contents.remove(agent)
        return True             #Removed Successfully
    #########################################################
    def moveIn(self, agent: agent.Agent) -> bool:

        if self.contents.find(agent) != -1:
            print(f"Failed to add agent: {agent._ID}. Agent already in cell")
            return False        #Couldn't Add
        
        self.contents.append(agent)
        return True             #Added Successfully
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

    def __init__(self, rows: int = 10, cols: int = 10, prop_agents: float = 0.3):
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
            print(i)
        print(self._agents)
    #########################################################
    def getCell(self, position: Position) -> Cell:
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

    def _moveAgent(self, agent: agent.Agent, target_cell: Cell) -> bool:
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
        row_end = min(10, origin_cell.position.row + spread_radius)
        col_start = max(0, origin_cell.position.col - spread_radius)
        col_end = min(10, origin_cell.position.col + spread_radius)
        # loop through all the cells and append all their agents to the list
        for r in range(row_start, row_end):
            for c in range(col_start, col_end):
                for a in self._grid[r][c].contents:
                    print(a)
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
        ''' method to add an agent to a given cell in the grid -- NOTE: different
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

    def _tryShare(self, target_agent: agent.Agent, information: Information):
        '''

        First reshares, then moves. It calls the receiveInf method on the target agent, which
        returns two different values in a dictionary. Resharing happens first, and then moving is dealt with.
        Refer to documentation for more information on this decision and its ramifications for the results.

        Paremeters:
            target_agent: The agent on which sharing of information will be attempted
            information: The information which will be tried to share with the agent
        '''
        target_agent.receiveInf(information = information)      #Share information with target agent

        self.move

    #########################################################

    def _oneTurn(self, origin_agent: agent.Agent):
        '''Runs a single "Turn" of a round (of a simulation)

        
        '''

        info_generated = origin_agent.isInfGen()                #Generate info if it will be generated
        if(info_generated == False): return                     #If information will not be generated, return
        
        #If it is generated, then:
        share_list = self.agentsInRange(origin_agent)           #Get list of agents with whom info will be shared
        for agent in share_list:
            self._tryShare(agent)                               #Try to share it with them
        return
    
    #########################################################

    def _oneRound(self):
        '''Runs a single "round" of the simulation

        A round is divided in multiple different turns. This function
        generates a "turn" list and proceeds to call the _oneTurn function
        in the random order generated

        '''
        return

    #########################################################


    def simulate(self, runs: int):
        ''' function to simulate the the spread of information
        runs: the number of times to cycle through the sim

        each run starts with a chance for all agents in the grid to generate
        information. then, for each of the agents that have generated new
        information, each agent within the spread radius has a chance of accepting
        the information
        '''
        # Call grid to generate a “turn” list
        g_copy = [cell for row in self._grid for cell in row]
        agents = []     # im going to store stuff as a tuple
        for c in g_copy:
            if c.isEmpty() == False:
                for a in c.contents:
                    if random.random() <= a._prob_gen_inf:
                        name = len(self._information) + 1
                        info = Information(a.position, name)
                        self._information[name] = info
                        a._information.append(info)
                        if random.random() <= a._prob_repeat_inf:   # share information
                            agents.append([a, info])
                            print(f"{a} shares the information")
                        else:
                            print(f"{a} doesn't share the information")

        # Agent action loop, for each agent in turn list
        # Check if information will be generated (.1)
        # If information is generated, then get list of agents in radius from grid
        while len(agents) > 0:
            print(f"Agents in radius of {agents[0][0]}:")
            in_range = self._agentsInRange(agents[0][0])
            info = agents[0][1]
            agents.pop(0)
            for r in in_range:
                if info not in r._information:  # check if the agents has the info
                    if random.random() <= r._prob_accept_inf:
                        print(f"{r} accepts the information")
                        r._information.append(info)
                        if random.random() <= r._prob_repeat_inf:
                            print("     decides to share")
                            agents.append([r, info])
                    else:
                        print(f"{r} rejects the information")


        # Call each agent in that list to see if they accept the information
            # Check that the agent has not received this information already, if they did, then next.
            # When agent receives information, add to their list of received information
            # If not accepted, then return
            # If accepted
                # Move closer to idea origin
                # If they don't spread it again, return (.1)
                # If they do
                # Call b.ii again
            # Next
