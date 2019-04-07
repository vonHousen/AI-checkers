from state import *
import time
import cProfile


class SearchAlgorithm:

    @staticmethod
    def min_max(state, levels_count_to_analyse):
        """
        Pure min_max algorithm for choosing the best move
        :param state: current state
        :param levels_count_to_analyse: count of levels taken into account
        :return: Tuple: ( h(state), state )
        """
        if levels_count_to_analyse <= 0 or state.is_terminal():
            return state._board.balance, state, None

        else:
            state.generate_next_states()
            child_states_tuples = []

            # recursively use min_max(...) level down, append results to table
            for child_state in state.next_states:
                min_max_tuple = SearchAlgorithm.min_max(child_state, levels_count_to_analyse - 1)
                child_states_tuples.append((min_max_tuple[0], min_max_tuple[1], child_state))

            if state.turn == Color.WHITE:  # assuming white = player & black = opponent

                # choose the best (max) state from the generated ones
                max_state_tuple = child_states_tuples[0]
                for child_state_tuple in child_states_tuples:
                    if child_state_tuple[0] > max_state_tuple[0]:
                        max_state_tuple = child_state_tuple

                state.next_move = max_state_tuple[2]
                return max_state_tuple

            else:  # state.turn == Color.BLACK

                # choose the best (min) state from the generated ones
                min_state_tuple = child_states_tuples[0]
                for child_state_tuple in child_states_tuples:
                    if child_state_tuple[0] < min_state_tuple[0]:
                        min_state_tuple = child_state_tuple

                state.next_move = min_state_tuple[2]
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

    final_state = alg.min_max(state, 6)[1]

    end_min_max = time.time()
    print(final_state)
    print(40 * "-")
    print("Final sequence:")
    state.print_final_sequence()
    print()
    print(40 * "-")
    print("min_max time [s]: " + f'{end_min_max - start_min_max}')


if __name__ == '__main__':
    # cProfile.run('test_min_max()')
    test_min_max()
