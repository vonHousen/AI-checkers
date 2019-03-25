from state import *


class Game:
    def __init__(self):
        self.states = [[State()]]   # array of sets of states (in 1 row all possible states)
        # TODO need to implement better data structure: tree

    def print_set(self, no_set_of_states):
        """

        :param no_set_of_states: number of the set of states to be printed
        :return: -
        """
        if self.states.__len__() > no_set_of_states >= 0:
            for no, state in enumerate(self.states[no_set_of_states]):
                print("set_of_states: " + f'{no_set_of_states}' + " | state no: " + f'{no}')
                print(state)

    def generate_next_states(self, turn):
        """
        Generates all possible states generated from the last one (appends to self.states)
        :param turn: decides what turn (what colour) it is for generating new states
        :return: -
        """

        last_state = self.states[-1][0]     # it should be parent in the tree structure
        self.states.append([])              # new set_of_states

        for piece in last_state.board.get_pieces(turn):

            if piece.can_attack():
                for destination in piece.list_possible_attacks:
                    attacker_row = piece.row
                    attacker_col = piece.column

                    self.states[-1].append(
                        last_state.attack_it(attacker_row, attacker_col, destination[0], destination[1]))

                    # TODO if just appended state result in multiple-attack: append new states, delete prev.
                    # TODO make it recursive (no one knows how many multiple-attacks a piece can perform

            elif piece.can_move():
                for destination in piece.list_possible_moves:
                    self.states[-1].append(
                        last_state.move_to(piece.row, piece.column, destination[0], destination[1]))

        if self.states[-1] == []:       # delete set_of_state if empty
                del self.states[-1]


def test_print_set():
    game = Game()
    game.states.append([])
    game.states[1].append(game.states[0][0].move_to(5, 0, 4, 1))
    game.states[1].append(game.states[0][0].move_to(5, 2, 4, 1))
    game.states[1].append(game.states[0][0].move_to(5, 2, 4, 3))

    game.print_set(1)


def test_generate_next_states():
    game = Game()
    game.generate_next_states()
    print(game.states.__len__())


if __name__ == '__main__':
    test_generate_next_states()
