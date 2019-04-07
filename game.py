from state import *
from search_algorithm import SearchAlgorithm


class Game:
    def __init__(self):
        self.current_state = State()  # root for tree structure of States

    def make_move(self):
        if self.is_finished():
            raise RuntimeError("Making moves in a finished game")
        print("Starting alpha_beta")
        SearchAlgorithm.alpha_beta(self.current_state, 8)
        next_state = self.current_state.next_move
        # print("XD")
        # print(next_state._board)
        self.current_state = State(next_state.turn, next_state._board.board_repr)

    def is_finished(self):
        if self.current_state.is_terminal():
            return True
        return False


if __name__ == '__main__':
    game = Game()
    print(game.current_state)
    while game.is_finished() is False:
        game.make_move()
        print(game.current_state)
        input("Press key to continue...")
