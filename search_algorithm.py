from state import *
import time


class SearchAlgorithm:

    @staticmethod
    def alpha_beta(root_state, depth):
        return SearchAlgorithm._alpha_beta(root_state, depth, -999999, 999999)

    @staticmethod
    def _alpha_beta(root_state, depth, alpha, beta):
        if depth <= 0 or root_state.is_terminal():
            return root_state.balance
        else:
            root_state.generate_next_states()

        if root_state.turn == Color.WHITE:  # assuming white = player & black = opponent
            for child_state in root_state.next_states:
                alpha_beta_result_for_this_child = SearchAlgorithm._alpha_beta(child_state, depth - 1, alpha, beta)
                if alpha_beta_result_for_this_child > alpha:
                    alpha = alpha_beta_result_for_this_child
                    root_state.next_move = child_state
                if alpha >= beta:
                    return beta
            return alpha
        else:
            for child_state in root_state.next_states:
                alpha_beta_result_for_this_child = SearchAlgorithm._alpha_beta(child_state, depth - 1, alpha, beta)
                if alpha_beta_result_for_this_child < beta:
                    beta = alpha_beta_result_for_this_child
                    root_state.next_move = child_state
                if alpha >= beta:
                    return alpha
            return beta


def test_alpha_beta():
    board_r = (0x8a8a8a8a,
               0xa888a8a8,
               0x8a8a8a8a,
               0x88888888,
               0x8a888888,
               0x28282828,
               0x82828282,
               0x28282828)
    state = State(Color.WHITE, board_r)
    print(40 * "-")
    print("Root state:")
    print(state)
    print(40 * "-")
    start_time = time.time()

    SearchAlgorithm.alpha_beta(state, 6)

    end_time = time.time()
    print(40 * "-")
    print("Final sequence:")
    print_final_decision_chain(state)
    print()
    print(40 * "-")
    print("alpha_beta time [s]: " + f'{end_time - start_time}')


def test_kings():
    board_r = (0x88838888,
               0x88888888,
               0x88888888,
               0x88888888,
               0x888a8888,
               0x88888888,
               0x88888288,
               0x88888888)
    state = State(Color.WHITE, board_r)
    print(40 * "-")
    print("Root state:")
    print(state)
    print(40 * "-")
    start_time = time.time()

    SearchAlgorithm.alpha_beta(state, 3)

    end_time = time.time()
    print(40 * "-")
    print("Final sequence:")
    print_final_decision_chain(state)
    print()
    print(40 * "-")
    print("alpha_beta time [s]: " + f'{end_time - start_time}')


def test_becoming_kings():
    board_r = (0x88888888,
               0x28888888,
               0x88888888,
               0x88888888,
               0x88888888,
               0x8888a888,
               0x88888288,
               0x88888888)
    state = State(Color.BLACK, board_r)
    print(40 * "-")
    print("Root state:")
    print(state)
    print(40 * "-")
    start_time = time.time()

    SearchAlgorithm.alpha_beta(state, 6)

    end_time = time.time()
    print(40 * "-")
    print("Final sequence:")
    print_final_decision_chain(state)
    print()
    print(40 * "-")
    print("alpha_beta time [s]: " + f'{end_time - start_time}')


if __name__ == '__main__':
    test_becoming_kings()
