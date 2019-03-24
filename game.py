from state import *


class Game:
    def __init__(self):
        self.states = [[State()], []]   # array of sets of states (in 1 row all possible states)

    def print_set(self, no_set_of_states):
        """

        :param no_set_of_states: number of the set of states to be printed
        :return: -
        """
        if self.states.__len__() > no_set_of_states >= 0:
            for no, state in enumerate(self.states[no_set_of_states]):
                print("set_of_states: " + f'{no_set_of_states}' + " | state no: " + f'{no}')
                print(state)

    def generate_next_states(self):
        """
        Generates all possible states generated from the last one (appends to self.states)
        :return: -
        """
        pass    # TODO implement


def test_game():
    game = Game()
    game.states[1].append(game.states[0][0].move_to(5, 0, 4, 1))
    game.states[1].append(game.states[0][0].move_to(5, 2, 4, 1))
    game.states[1].append(game.states[0][0].move_to(5, 2, 4, 3))

    game.print_set(1)



if __name__ == '__main__':
    test_game()
