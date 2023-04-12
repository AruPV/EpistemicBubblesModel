import random
from information import Information
from grid import Grid

class Agent:
    ''' class for each of the individual agents in the simulation
    allows us to store information about each agent inside the object

    Parameters:
        ID: The ID of the agent
        _position: Holds the position of the cell the agent is in.
            It's a location object.
        _prob_gen_inf: Probability that the agent will generate
            information in a given loop
        _prob_accept_inf: Probability that the agent will accept
            information it
        _prob_reshare_inf: Probability that the agent will repeat
            information after getting accepted
        _information: the different information this agent has received
        _spread_radius: Radius at which the agent will spread information
        _grif: grid which the agent belongs to
    '''
    def __init__(self, ID, location, grid: Grid):
        self._ID = ID
        self._grid = grid
        self._position = location
        self._information = None
        # things we can change later -- should add rates later
        self._prob_gen_inf = .05
        self._prob_accept_inf = .4
        self._prob_reshare_inf = .1 
        self._spread_radius = 2


    def isInfGen(self, ) -> bool:
        ''' Check if information will be generated
        Returns:
            Bool, whether or not information is to be generated
        '''
        is_gen = False
        prob_roll = random()
        if self._prob_gen_inf > prob_roll:
            is_gen = True
        return is_gen
    
    def isInfAccept(self) -> bool:
        ''' Check if information will be accepted
        Returns:
            Bool, whether or not information is to be accepted
        '''
        is_accept = False
        prob_roll = random()
        if self._prob_accept_inf > prob_roll:
            is_accept = True
        return is_accept
    
    def isInfReshared(self) -> bool:
        ''' Check if information will be reshared
        Returns:
            Bool, whether or not information is to be reshared
        '''
        is_reshared = False
        prob_roll = random()
        if self._prob_repeat_inf > prob_roll:
            is_reshared = True
        return is_reshared

    def receiveInf(self, information: Information) -> None:
        ''' Receives information from other agents
        Parameters:
            information: the information shared by other agent
        Returns:
            Nothing
        '''
        return

    def shareInf(self) -> None:
        agents_in_range = self._grid.agentsInRange(origin = self)
        for agent in agents_in_range:
            agent.receiveInf()

        return

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