import copy
import random

from src.services.services import Services


class AI:
    """
    The AI class handles the robot's decision-making during the game
    """
    def __init__(self, services: Services):
        self.__services = services
        self.__sign = None

    def set_sign(self, sign: str):
        """
        Function that sets the robot's play sign as the given sign
        :param sign: The given sign
        :return: NoneType
        """
        self.__sign = sign

    def __default_strategy(self, lines: int, columns: int):
        """
        Function that marks a random cell on the board
        :param lines: Number of lines of the board
        :param columns: Number of columns of the board
        :return: NoneType
        """
        while True:
            try:
                self.__services.mark_cell(str(random.randint(1, lines)), str(random.randint(1, columns)), self.__sign)
                return
            except ValueError:
                pass

    def __odd_strategy(self, lines: int, columns: int, board, last_line: int, last_column: int):
        """
        Function that executes the winning odd-strategy, if the ai starts, by mirroring the human's actions
        :param lines: Number of lines of the board
        :param columns: Number of columns of the board
        :param board: Current state of the board
        :param last_line: Last line index of the human's move
        :param last_column: Last column index of the human's move
        :return: NoneType
        """
        # If first move, play the middle
        if self.__sign == "X":
            if board[lines//2][columns//2].state == 0:
                self.__services.mark_cell(str(lines//2+1), str(columns//2+1), self.__sign)
                return
        # Else mirror the last move of the human
        self.__services.mark_cell(str(abs(lines-last_line)), str(abs(columns-last_column)), self.__sign)

    def __recursive_decision(self, lines, columns, services, step) -> float:
        """
        Function that goes through each cell of the board and, for the open cells, starts a new branch by marking it and
        simulating all possible moves by the ai and the player and returns win rate of the branch
        :param lines: Number of lines in the board
        :param columns: Number of columns in the board
        :param services: The services object containing the current board state
        :param step: The number of steps it took to reach this state
        :return: The win rate of the branch
        """
        # end-case: board is empty -> we are at the end of a branch and have to figure out if we won or lost
        if not services.empty_space():
            # win
            if step % 2 == 1:
                return 1
            # lose
            else:
                return 0

        win_count = 0
        branch_count = 0
        # go through all cells
        for line in range(lines):
            for column in range(columns):
                # check if we have an open cell
                if services.board[line][column].state == 0:
                    # make a copy of the board and the services
                    new_board = copy.deepcopy(services.board)
                    service_copy = Services(new_board)

                    # mark the cell
                    service_copy.mark_cell(str(line+1), str(column+1), self.__sign)

                    # start a new branch and calculate the number of wins on it
                    win_count += self.__recursive_decision(lines, columns, service_copy, step+1)
                    branch_count += 1

        # return the win rate as number of wins over the number of total branches
        return win_count / branch_count

    def __brute_force(self, lines, columns):
        """
        Function that goes through each cell of the board and, for the open cells, simulates each possible outcome
        of different moves by the player and the AI to figure out what the move that will result in victory is,
        and does it.
        :param lines: Number of lines in the board
        :param columns: Number of columns in the board
        :return: NoneType
        """
        move_i = move_j = -1
        services = self.__services
        max_win_rate = -1

        # go through each cell
        for line in range(lines):
            for column in range(columns):
                # check if cell is open
                if services.board[line][column].state == 0:
                    # copy the board and the services
                    new_board = copy.deepcopy(services.board)
                    service_copy = Services(new_board)

                    # mark the cell
                    service_copy.mark_cell(str(line + 1), str(column + 1), self.__sign)

                    # start a new branch and calculate its win rate
                    branch_win_rate = self.__recursive_decision(lines, columns, service_copy, 1)
                    # if we have a more probable winning branch, save it
                    if branch_win_rate > max_win_rate:
                        max_win_rate = branch_win_rate
                        move_i = line
                        move_j = column

                    # make a backup of last open cell in case none of the branches are winnable
                    backup_i = line
                    backup_j = column

        # if the move index remains unchanged, then there are no winnable branches and we use the backup one
        if move_i == -1:
            move_i = backup_i
            move_j = backup_j

        # do the move that is most probable to lead to a win
        self.__services.mark_cell(str(move_i+1), str(move_j+1), self.__sign)

    def take_action(self, last_line: int, last_column: int):
        """
        Function that evaluates the current state of the board and marks a cell accordingly
        :return: NoneType
        """
        board = self.__services.board
        lines = len(board)
        columns = len(board[0])
        if lines % 2 == 1 and columns % 2 == 1 and self.__sign == "X":
            self.__odd_strategy(lines, columns, board, last_line, last_column)
        else:
            if self.__services.blank_spots() > 16:
                self.__default_strategy(lines, columns)
            else:
                self.__brute_force(lines, columns)
