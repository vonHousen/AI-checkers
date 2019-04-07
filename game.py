from state import *
from search_algorithm import SearchAlgorithm


class Game:
    def __init__(self, depth):
        self.current_state = State()
        self.depth = depth

    def make_move(self):
        if self.is_finished():
            raise RuntimeError("Making moves in a finished game")
        print("Starting alpha_beta")
        SearchAlgorithm.alpha_beta(self.current_state, self.depth)
        next_state = self.current_state.next_move
        # print("XD")
        # print(next_state._board)
        self.current_state = State(next_state.turn, next_state._board.board_repr)

    def is_finished(self):
        if self.current_state.is_terminal():
            return True
        return False


def run_game():
    while True:
        try:
            depth = int(input("Give me the depth you want to search:\n"))
        except ValueError:
            print("Try harder pls.")
        else:
            break
    game = Game(depth)
    print(game.current_state)
    while game.is_finished() is False:
        game.make_move()
        print(game.current_state)
        # i = input("If you want to see how the decision will be made type 'd', else press enter")
        # print(i)
        # if i is "d":
        # game.current_state.print_final_sequence() todo fix thix xd
        input("press enter")


if __name__ == '__main__':
    run_game()
