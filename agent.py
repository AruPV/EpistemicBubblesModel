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