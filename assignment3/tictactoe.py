# Task 6

class TictactoeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class Board:
    valid_moves = [
        "upper left",
        "upper center",
        "upper right",
        "middle left",
        "center",
        "middle right",
        "lower left",
        "lower center",
        "lower right",
    ]

    def __init__(self):
        self.board_array = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "],
        ]
        self.turn = "X"
        self.last_move = None

    def __str__(self):
        lines = []
        lines.append(
            f" {self.board_array[0][0]} | "
            f"{self.board_array[0][1]} | "
            f"{self.board_array[0][2]} \n"
        )
        lines.append("-----------\n")
        lines.append(
            f" {self.board_array[1][0]} | "
            f"{self.board_array[1][1]} | "
            f"{self.board_array[1][2]} \n"
        )
        lines.append("-----------\n")
        lines.append(
            f" {self.board_array[2][0]} | "
            f"{self.board_array[2][1]} | "
            f"{self.board_array[2][2]} \n"
        )
        return "".join(lines)

    def move(self, move_string):
        move_string = move_string.strip().lower()

        if move_string not in Board.valid_moves:
            raise TictactoeException(
                "That's not a valid move."
            )

        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3
        column = move_index % 3

        if self.board_array[row][column] != " ":
            raise TictactoeException(
                "That spot is taken."
            )

        self.board_array[row][column] = self.turn
        self.last_move = (row, column)

        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"

    def whats_next(self):
        winner = self._find_winner()

        if winner is not None:
            return True, f"{winner} has won"

        board_is_full = all(
            cell != " "
            for row in self.board_array
            for cell in row
        )

        if board_is_full:
            return True, "Cat's Game"

        return False, f"{self.turn}'s turn"

    def _find_winner(self):
        winning_lines = []

        # Rows
        winning_lines.extend(self.board_array)

        # Columns
        for column in range(3):
            winning_lines.append([
                self.board_array[0][column],
                self.board_array[1][column],
                self.board_array[2][column],
            ])

        # Diagonals
        winning_lines.append([
            self.board_array[0][0],
            self.board_array[1][1],
            self.board_array[2][2],
        ])

        winning_lines.append([
            self.board_array[0][2],
            self.board_array[1][1],
            self.board_array[2][0],
        ])

        for line in winning_lines:
            if (
                line[0] != " "
                and line[0] == line[1] == line[2]
            ):
                return line[0]

        return None


if __name__ == "__main__":
    board = Board()
    game_over = False

    print("Welcome to Tic-Tac-Toe!")
    print("Valid moves are:")

    for move_name in Board.valid_moves:
        print(f"- {move_name}")

    while not game_over:
        print()
        print(board)

        game_over, message = board.whats_next()

        if game_over:
            print(message)
            break

        requested_move = input(
            f"{message}. Enter a move: "
        )

        try:
            board.move(requested_move)
        except TictactoeException as error:
            print(error.message)

    print()
    print("Final board:")
    print(board)