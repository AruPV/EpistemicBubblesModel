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
        _prob_repeat_inf: Probability that the agent will repeat
            information after getting accepted
        _spread_radius: Radius at which the agent will spread information
    '''
    def __init__(self, ID, location):
        self._ID = ID 
        self._position = location
        self._information = None
        # things we can change later -- should add rates later
        self._prob_gen_inf = .05
        self._prob_accept_inf = .4
        self._prob_repeat_inf = .1 
        self._spread_radius = 2 


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