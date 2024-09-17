class Cell:
    """
    The cell class represents a square on the board and has two properties:
    - the state, which can be 0 representing an open cell and 1 representing a blocked cell
    - the sign, which can be a space, O for a cell marked by the O player or X for a cell marked by the X player
    """
    def __init__(self, state: int = 0):
        if not isinstance(state, int):
            raise ValueError("State must be an int!")
        if state != 0 and state != 1:
            raise ValueError("State must be either 0 or 1!")
        self.__state = state
        self.__sign = " "

    def block(self):
        self.__state = 1
        self.__sign = "*"

    @property
    def state(self):
        return self.__state

    @property
    def sign(self):
        return self.__sign

    def set_sign(self, new_sign: str):
        if not isinstance(new_sign, str):
            raise ValueError("Sign must be a string!")
        if new_sign != "O" and new_sign != "X":
            raise ValueError("Sign must be either O or X!")
        self.__sign = new_sign
