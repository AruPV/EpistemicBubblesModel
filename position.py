from typing import NamedTuple

class Position(NamedTuple):
    ''' just allows us to use .row and .col rather than the less-easy-to-read
        [0] and [1] for accessing values
        yoinked this from the last class i had with Barry
    '''
    row: int
    col: int