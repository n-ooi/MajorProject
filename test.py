class Piece:
    def __init__(self, color):
        self.color = color

    def can_move(self, x1, y1, x2, y2):
        """Return True if the piece can move from (x1, y1) to (x2, y2), False otherwise."""
        raise NotImplementedError


class Pawn(Piece):
    def can_move(self, x1, y1, x2, y2):
        if self.color == "white":
            return (x1, y1 + 1) == (x2, y2)
        else:
            return (x1, y1 - 1) == (x2, y2)


class Knight(Piece):
    def can_move(self, x1, y1, x2, y2):
        return ((x2, y2) in ((x1 + 2, y1 + 1), (x1 + 2, y1 - 1), (x1 - 2, y1 + 1), (x1 - 2, y1 - 1),
                             (x1 + 1, y1 + 2), (x1 + 1, y1 - 2), (x1 - 1, y1 + 2), (x1 - 1, y1 - 2)))


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def move_piece(self, x1, y1, x2, y2):
        piece = self.board[x1][y1]
        if piece and piece.can_move(x1, y1, x2, y2):
            self.board[x2][y2] = piece
            self.board[x1][y1] = None
            return True
        return False


def play_game():
    board = Board()

    # Place pieces on the board
    board.board[0][0] = Rook("white")
    board.board[0][1] = Knight("white")
    board.board[0][2] = Bishop("white")
    # ...

    while True:
        # Display the board
        for row in board.board:
            print(" ".join("R" if piece else "-" for piece in row))
        print()

        # Get move from player
        x1, y1, x2, y2 = map(int, input("Enter move (x1 y1 x2 y2): ").split())
        if not board.move_piece(x1, y1, x2, y2):
            print("Illegal move")


if __name__ == '__main__':
    play_game()