import numpy as np

class MinMaxSolver:
    def __init__(self, config):
        self.config = list(config)
        self.player = 2
        self.opponent = 1

    def isMovesLeft(self):
        """ This function returns true if there are moves remaining on the board. It returns false if
         there are no moves left to play."""
        return 0 in self.config

    def evaluate(self):
        matrix = np.array(self.config).reshape(3, 3)
        for dim in range(matrix.shape[0]):
            if np.all(matrix[:, dim] == 1) or np.all(matrix[dim, :] == 1):
                return -10
            if np.all(matrix[:, dim] == 2) or np.all(matrix[dim, :] == 2):
                return 10
        if np.all(np.diagonal(matrix) == 1) or np.all(np.diagonal(np.fliplr(matrix)) == 1):
            return -10
        if np.all(np.diagonal(matrix) == 2) or np.all(np.diagonal(np.fliplr(matrix)) == 2):
            return 10
        return 0

    def minimax(self, depth, player_turn):
        """# This is the minimax function. It considers all the possible ways the game can go and returns
         the value of the board"""
        score = self.evaluate()

        # If Maximizer has won the game return his/her evaluated score
        if score == 10:
            return score

        # If Minimizer has won the game return his/her evaluated score
        if score == -10:
            return score

        # If there are no more moves and no winner then it is a tie
        if not self.isMovesLeft():
            return 0

        # If this player's turn
        if player_turn:
            best = -1000

            # Traverse all cells
            for index, _ in enumerate(self.config):
                # Check if cell is empty
                if self.config[index] == 0:
                    # Make the move
                    self.config[index] = self.player

                    # Call minimax recursively and choose the maximum value
                    best = max(best, self.minimax(depth + 1, not player_turn))

                    # Undo the move
                    self.config[index] = 0
            return best

        # If this minimizer's move
        else:
            best = 1000

            # Traverse all cells
            for index, _ in enumerate(self.config):
                # Check if cell is empty
                if self.config[index] == 0:
                    # Make the move
                    self.config[index] = self.opponent

                    # Call minimax recursively and choose the minimum value
                    best = min(best, self.minimax(depth + 1, not player_turn))

                    # Undo the move
                    self.config[index] = 0
            return best



    def findBestMove(self):
        """This will return the best possible move for the player"""
        best_val = -1000
        best_move = (-1, -1)

        # Traverse all cells, evaluate minimax function for all empty cells. And return the cell with optimal value.
        for index, _ in enumerate(self.config):
            # Check if cell is empty
            if self.config[index] == 0:
                # Make the move
                self.config[index] = self.player

                # compute evaluation function for this move.
                move_val = self.minimax(0, False)

                # Undo the move
                self.config[index] = 0

                # If the value of the current move is more than the best value, then update best
                if move_val > best_val:
                    best_move = index
                    best_val = move_val
        return best_move
