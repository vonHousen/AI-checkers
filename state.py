from board import *


class State:

    def __init__(self, next_turn=Color.WHITE, board_repr=(0x8a8a8a8a,
                                                          0xa8a8a8a8,
                                                          0x8a8a8a8a,
                                                          0x88888888,
                                                          0x88888888,
                                                          0x28282828,
                                                          0x82828282,
                                                          0x28282828
                                                          )):
        self.turn = next_turn
        # 8 not allowed or empty
        # 2 white man
        # 3 white king
        # a black man
        # b black king
        self.board_repr = board_repr
        self.level = "fix"
        self._cached_board = None

        self.next_move = None
        self._value = None

    @property
    def next_states(self):
        boards = self._board.get_next_boards()
        result = []
        for board in boards:
            result.append(State(board.turn, board.board_repr))
        return result

    @property
    def balance(self):
        if self.is_terminal():
            if self.turn is Color.WHITE:  # black wins
                return -1000
            else:  # white wins
                return 1000

        if self._value is None:
            self._value = self._board.balance
        return self._value

    @property
    def _board(self):
        """
        Cache new Board object (using stored representation) if it doesn't exist
        :return: Cached or just created Board object
        """
        if self._cached_board is None:
            self._cached_board = Board(self.board_repr, self.turn)
        return self._cached_board

    def is_terminal(self):
        """
        Defines if state is terminal or not
        :return: true/false
        """
        # get pieces of player that is moving in this turn
        pieces = self._board.get_pieces_of_color(self.turn)

        if not pieces:  # if you have no pieces left its game over
            return True

        # check if there's any move or attack current player can perform
        found_move_or_attack = False
        for piece in pieces:
            if piece.possible_attacks or piece.possible_moves:
                found_move_or_attack = True
                break
        if found_move_or_attack is False:
            return True

        return False

    def clean_cached_board(self):
        self._cached_board = None


    def __str__(self):
        printout = ""
        printout += "Turn = " + f'{self.turn}'
        printout += "   Balance = " + f'{self._board.balance}'
        if self._board.balance < 0:
            printout += "(black is winning)"
        elif self._board.balance > 0:
            printout += "(white is winning)"
        printout += "   Depth_level = " + f'{self.level}' + "\n"
        printout += self._board.__str__()

        return printout
