from state import *


class Game:
    def __init__(self):
        self.states = [[State()], []]   # array of sets of states (in 1 row all possible states)

    def print(self, no_set_of_states):
        """

        :param no_set_of_states: number of the set of states to be printed
        :return: -
        """
        pass    # TODO implement

    def generate_next_states(self):
        """
        Generates all possible states generated from the last one (appends to self.states)
        :return: -
        """
        pass    # TODO implement


def test_game():
    game = Game()
    game.print(1)


if __name__ == '__main__':
    test_game()
