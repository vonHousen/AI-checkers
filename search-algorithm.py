from state import *


class MinMax:

    def __init__(self, state):
        self._root_state = state
        self._terminal_state = None

    def generate_new(self, levels_count_to_generate):
        """
        Generates multiple levels of new states
        :param levels_count_to_generate: number of levels algorithm will generate new states
        :return: -
        """
        MinMax._generate_new_from(self._root_state, levels_count_to_generate)

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
            for new_state in state_to_generate_from._next_states:
                MinMax._generate_new_from(new_state, levels_count_to_generate - 1)

        # TODO fix it to generate new states in correct order
        state_to_generate_from.print_next_states()


def test_generating_attacks():
    board_r = (0x8a8a8a8a,
               0xa888a8a8,
               0x8a8a8a8a,
               0x88888888,
               0x8a888888,
               0x28282828,
               0x82828282,
               0x28282828)
    state = State(Color.WHITE, board_r)
    print(state.board)

    for attack in state.board.get_piece_at(0, 1).possible_attacks:
        print(attack)

    state.print_next_states()
    state.generate_next_states()
    state.print_next_states()


def test_generating_levels():
    board_r = (0x8a8a8a8a,
               0xa888a8a8,
               0x8a8a8a8a,
               0x88888888,
               0x8a888888,
               0x28282828,
               0x82828282,
               0x28282828)
    state = State(Color.WHITE, board_r)

    alg = MinMax(state)
    print(state)
    alg.generate_new(2)


if __name__ == '__main__':
    test_generating_levels()
