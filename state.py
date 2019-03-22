from enum import Enum
from board import *


class Turn(Enum):
    WHITE = 0
    BLACK = 1


class State:

    def __init__(self, board_repr=(0x8a8a8a8a,
                                   0xa8a8a8a8,
                                   0x8a8a8a8a,
                                   0x88888888,
                                   0x88888888,
                                   0x28282828,
                                   0x82828282,
                                   0x28282828
                                   )):
        self.turn = Turn.BLACK
        # 8 not allowed or empty
        # 2 white man
        # 3 white king
        # a black man
        # b black king
        self.board_repr = board_repr
        self._cached_board = None

    @property
    def board(self):
        """
        Cache new Board object (using stored representation) if it doesn't exist
        :return: Cached or just created Board object
        """
        if self._cached_board is None:
            self._cached_board = Board(self.board_repr)
        return self._cached_board

    def clean_cached_board(self):
        self._cached_board = None

    def possible_states(self):
        """
        :return: all possible states one move from this state
        """
        states = []
        # todo
        return states


def test_cached_board():
    state = State()
    print(state.board)
    state.clean_cached_board()


if __name__ == '__main__':
    test_cached_board()
