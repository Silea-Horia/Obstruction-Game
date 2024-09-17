from src.services.services import Services
from src.ai.ai import AI
import time
import random


class UI:
    def __init__(self, services: Services, ai: AI):
        self.__services = services
        self.__ai = ai

    def __display_board(self):
        board = self.__services.board
        rows = len(board)
        for i in range(rows):
            print(end="\n|")
            for cell in board[i]:
                print(cell.sign, end="|")
        print()

    def __create_board(self):
        while True:
            print("How big should the board be?")
            try:
                lines = int(input("Lines: "))
                columns = int(input("Columns: "))
                self.__services.create_board(lines, columns)
                break
            except ValueError as ve:
                print(str(ve))

    @staticmethod
    def __determine_starting_player():
        print("Would you like to start? y/n")
        while True:
            opt = input(">>")
            if opt.lower() == "y":
                return "X", "O", 1
            elif opt.lower() == "n":
                return "O", "X", -1
            else:
                print("Erroneous command!")

    @staticmethod
    def __robot_message() -> str:
        messages = ["Hmmm...", "Let me think...", "Let's see...", "I will... no, this... hmm, actually...",
                    "What should I do now?", "That was a good move!", "I sense I will win...",
                    "When did you get this good?"]
        return messages[random.randint(0, len(messages))-1]

    def start(self):
        thinking_delay = 1.5
        last_cell_line = -1
        last_cell_column = -1
        while True:
            self.__create_board()

            human_sign, ai_sign, player_type = self.__determine_starting_player()
            self.__ai.set_sign(ai_sign)

            while True:
                self.__display_board()

                # Human action
                if player_type == 1:
                    line = input("Line: ")
                    if line.lower() == "xxx":   # quit anytime
                        break
                    column = input("Column: ")
                    if column.lower() == "xxx":
                        break

                    try:
                        self.__services.mark_cell(line, column, human_sign)
                        player_type *= (-1)
                        last_cell_line = int(line) - 1
                        last_cell_column = int(column) - 1
                    except ValueError as ve:
                        print(str(ve))
                # Robot action
                else:
                    print(self.__robot_message())
                    time.sleep(thinking_delay)
                    self.__ai.take_action(last_cell_line, last_cell_column)
                    player_type *= (-1)
                # Check if game is over
                if not self.__services.empty_space():
                    self.__display_board()
                    if player_type == 1:    # values are inverted
                        print("AI wins!")
                    else:
                        print("Human wins!")
                    break
            # End options
            while True:
                print("Replay? Press r.")
                print("Exit? Press x.")
                option = input(">>")
                if option.lower() == "r" or option.lower() == "x":
                    break
                else:
                    print("Erroneous command!")
            if option == "x":
                break
