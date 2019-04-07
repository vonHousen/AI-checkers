from state import *


class SearchAlgorithm:

    def __init__(self, state):
        self._root_state = state
        self._terminal_state = None

    def generate_new(self, levels_count_to_generate):
        """
        Generates multiple levels of new states
        :param levels_count_to_generate: number of levels algorithm will generate new states
        :return: -
        """
        SearchAlgorithm._generate_new_from(self._root_state, levels_count_to_generate)

    @staticmethod
    def _generate_new_from(state_to_generate_from, levels_count_to_generate):
        """
        Recursively generates tree structure from new states
        :param state_to_generate_from:
        :param levels_count_to_generate: number of levels algorithm will generate new states
        :return:
        """
        if levels_count_to_generate <= 0:
            return
        else:
            state_to_generate_from.generate_next_states()
            for new_state in state_to_generate_from.next_states:
                SearchAlgorithm._generate_new_from(new_state, levels_count_to_generate - 1)

        # if state_to_generate_from.level == 1: state_to_generate_from.print_next_states()

    @staticmethod
    def min_max(state, levels_count_to_analyse):
        """
        Pure min_max algorithm for choosing the best move
        :param state: current state
        :param levels_count_to_analyse: count of levels taken into account
        :return: Tuple: ( h(state), state )
        """
        if levels_count_to_analyse <= 0 or state.is_terminal():
            return state.board.balance, state

        else:
            state.generate_next_states()
            states_to_choose_from = []

            # recursively use min_max(...) level down, append results to table
            for new_state in state.next_states:
                states_to_choose_from.append(SearchAlgorithm.min_max(new_state, levels_count_to_analyse - 1))

            if state.turn == Color.WHITE:     # assuming white - player & black - opponent

                # choose the best (max) state from the generated ones
                max_state_tuple = states_to_choose_from[0]
                for appended_state in states_to_choose_from:
                    if appended_state[0] > max_state_tuple[0]:
                        max_state_tuple = appended_state

                # state.next_move = max_state_tuple[1]
                return max_state_tuple

            else:   # state.turn == Color.BLACK

                # choose the best (min) state from the generated ones
                min_state_tuple = states_to_choose_from[0]
                for appended_state in states_to_choose_from:
                    if appended_state[0] < min_state_tuple[0]:
                        min_state_tuple = appended_state

                # state.next_move = min_state_tuple[1]
                return min_state_tuple


def test_generating_levels():
    board_r = (0x8a8a8a8a,
               0xa8a8a8a8,
               0x888a8a8a,
               0x88888888,
               0x8a888888,
               0x28282828,
               0x82828282,
               0x28282828)
    state = State(Color.WHITE, board_r)

    alg = SearchAlgorithm(state)
    print(state)
    alg.generate_new(2)


def test_min_max():
    board_r = (0x8a8a8a8a,
               0xa888a8a8,
               0x8a8a8a8a,
               0x88888888,
               0x8a888888,
               0x28282828,
               0x82828282,
               0x28282828)
    state = State(Color.WHITE, board_r)

    alg = SearchAlgorithm(state)
    print("Root state:")
    print(state)
    print("Best state:")
    print(alg.min_max(state, 3)[1])


if __name__ == '__main__':
    test_min_max()
