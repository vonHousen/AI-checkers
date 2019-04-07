from state import *
import time


class SearchAlgorithm:

    @staticmethod
    def alpha_beta(root_state, depth, alpha, beta):
        if depth <= 0 or root_state.is_terminal():
            return root_state.balance
        else:
            root_state.generate_next_states()

        if root_state.turn == Color.WHITE:  # assuming white = player & black = opponent
            for child_state in root_state.next_states:
                alpha_beta_result_for_this_child = SearchAlgorithm.alpha_beta(child_state, depth - 1, alpha, beta)
                if alpha_beta_result_for_this_child > alpha:
                    alpha = alpha_beta_result_for_this_child
                    root_state.next_move = child_state
                if alpha >= beta:
                    return beta
            return alpha
        else:
            for child_state in root_state.next_states:
                alpha_beta_result_for_this_child = SearchAlgorithm.alpha_beta(child_state, depth - 1, alpha, beta)
                if alpha_beta_result_for_this_child < beta:
                    beta = alpha_beta_result_for_this_child
                    root_state.next_move = child_state
                if alpha >= beta:
                    return alpha
            return beta

    @staticmethod
    def min_max(root_state, levels_count_to_analyse):
        """
        Pure min_max algorithm for choosing the best move
        :param root_state: current state
        :param levels_count_to_analyse: count of levels taken into account
        :return: Tuple: ( h(state), state )
        """
        if levels_count_to_analyse <= 0 or root_state.is_terminal():
            return root_state.balance, root_state, None

        else:
            root_state.generate_next_states()
            child_states_tuples = []

            # recursively use min_max(...) level down, append results to table
            for child_state in root_state.next_states:
                min_max_tuple = SearchAlgorithm.min_max(child_state, levels_count_to_analyse - 1)
                child_states_tuples.append((min_max_tuple[0], min_max_tuple[1], child_state))

            if root_state.turn == Color.WHITE:  # assuming white = player & black = opponent

                # choose the best (max) state from the generated ones
                max_state_tuple = child_states_tuples[0]
                for child_state_tuple in child_states_tuples:
                    if child_state_tuple[0] > max_state_tuple[0]:
                        max_state_tuple = child_state_tuple

                root_state.next_move = max_state_tuple[2]
                return max_state_tuple

            else:  # state.turn == Color.BLACK

                # choose the best (min) state from the generated ones
                min_state_tuple = child_states_tuples[0]
                for child_state_tuple in child_states_tuples:
                    if child_state_tuple[0] < min_state_tuple[0]:
                        min_state_tuple = child_state_tuple

                root_state.next_move = min_state_tuple[2]
                return min_state_tuple


def test_min_max():
    board_r = (0x8a8a8a8a,
               0xa888a8a8,
               0x8a8a8a8a,
               0x88888888,
               0x8a888888,
               0x28282828,
               0x82828282,
               0x28282828)
    state = State(Color.WHITE)
    alg = SearchAlgorithm()
    print(40 * "-")
    print("Root state:")
    print(state)
    print(40 * "-")
    print("Best (final) state:")
    start_min_max = time.time()

    result = alg.min_max(state, 6)
    final_state = result[1]

    end_min_max = time.time()
    print(final_state)
    print(40 * "-")
    print("Final sequence:")
    state.print_final_sequence()
    print()
    print(40 * "-")
    print("min_max time [s]: " + f'{end_min_max - start_min_max}')


def test_alpha_beta():
    board_r = (0x8a8a8a8a,
               0xa888a8a8,
               0x8a8a8a8a,
               0x88888888,
               0x8a888888,
               0x28282828,
               0x82828282,
               0x28282828)
    state = State(Color.WHITE)
    print(40 * "-")
    print("Root state:")
    print(state)
    print(40 * "-")
    start_time = time.time()

    result = SearchAlgorithm.alpha_beta(state, 6, -999999, 999999)

    end_time = time.time()
    print(40 * "-")
    print("Final sequence:")
    state.print_final_sequence()
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

    result = SearchAlgorithm.alpha_beta(state, 3, -999999, 999999)

    end_time = time.time()
    print(40 * "-")
    print("Final sequence:")
    state.print_final_sequence()
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

    result = SearchAlgorithm.alpha_beta(state, 6, -999999, 999999)

    end_time = time.time()
    print(40 * "-")
    print("Final sequence:")
    state.print_final_sequence()
    print()
    print(40 * "-")
    print("alpha_beta time [s]: " + f'{end_time - start_time}')


if __name__ == '__main__':
    test_becoming_kings()

