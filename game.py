from state import *
from search_algorithm import SearchAlgorithm
import time


class Game:
    def __init__(self, depth):
        self.moves_made = 0
        self.current_state = State()
        self.depth = depth

    def calculate_next_move(self):
        if self.is_finished():
            raise RuntimeError("Making moves in a finished game")
        print(f"Calculating move number {self.moves_made + 1}")
        SearchAlgorithm.alpha_beta(self.current_state, self.depth)

    def make_move(self):
        if self.is_finished():
            raise RuntimeError("Making moves in a finished game")

        next_state = self.current_state.next_move
        self.current_state = State(next_state.turn,
                                   next_state._board.board_repr)  # todo remove _board after moving gen states
        self.moves_made += 1

    @property
    def decision_chain(self):
        result = []
        state = self.current_state
        while state.next_move is not None:
            result.append(state.next_move)
            state = state.next_move
        return result

    def is_finished(self):
        if self.current_state.is_terminal():
            return True
        return False


def run_game():
    while True:
        try:
            depth = int(input("Give me the depth you want to search:\n"))
            if not (0 < depth < 10):
                raise ValueError()
        except ValueError:
            print("pls be serious: 0 < depth < 10")
        else:
            break
    game = Game(depth)
    game_history = []

    start_time = time.time()
    while game.is_finished() is False:
        game.calculate_next_move()
        game_history.append((game.current_state, game.decision_chain))
        game.make_move()
    end_time = time.time()

    print("calculation time [s]: " + f'{end_time - start_time}')

    for state, decision_chain in game_history:
        user_input = input(
            "If you want to see how the decision will be made type 'd' and press enter, else just enter\n")
        print(state)
        if user_input is "d" or user_input is "D":
            for decision_state in decision_chain:
                print(decision_state)


if __name__ == '__main__':
    run_game()
