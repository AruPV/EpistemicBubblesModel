from position import Position

class Information:
    ''' allows us to use information as a class
    might be useful later if we want to have different kinds of information
    with different characterists

    Parameters:
        ID: ID
        origin: Position object that holds Where the Information originated from. position type
    '''
    # how are we doing information in the base case? since there is only one kind
    # of information right now, do we represent information as an integer value if
    # an agent has more than one 'information'
    # or do we have give a name to each piece of generated information and store
    # them seperately?
    #Constructor method

    information_generated = 0
    def __init__(self, origin: Position) -> None:
        Information.information_generated += 1
        self.origin = origin
        self.ID = Information.information_generated
        pass

    origin: Position

    pass