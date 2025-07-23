from typing import List, Optional, Tuple

class TicTacToeGame:
    @staticmethod
    def create_empty_board() -> List[List[Optional[str]]]:
        return [[None for _ in range(3)] for _ in range(3)]

    @staticmethod
    def make_move(board: List[List[Optional[str]]], row: int, col: int, player: int) -> bool:
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        
        if board[row][col] is not None:
            return False

        board[row][col] = 'X' if player == 1 else 'O'
        return True

    @staticmethod
    def check_winner(board: List[List[Optional[str]]]) -> Optional[str]:
        """
        Check if there is a winner on the board by examining all possible winning combinations.
        Returns 'X' or 'O' if there's a winner, or None if there's no winner yet.
        
        Checks for:
        - Complete rows (horizontal)
        - Complete columns (vertical) 
        - Both diagonals
        """
        # Check rows
        for row in board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]

        # Check columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
                return board[0][col]

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
            return board[0][2]

        return None

    @staticmethod
    def is_board_full(board: List[List[Optional[str]]]) -> bool:
        return all(cell is not None for row in board for cell in row)

    @staticmethod
    def get_game_status(board: List[List[Optional[str]]]) -> Tuple[bool, Optional[str], bool]:
        winner = TicTacToeGame.check_winner(board)
        is_completed = winner is not None or TicTacToeGame.is_board_full(board)
        is_draw = is_completed and winner is None
        return is_completed, winner, is_draw
