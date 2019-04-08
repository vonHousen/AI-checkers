from state import *


class SearchAlgorithm:

    def alpha_beta(self, root_state, depth):
        return self._alpha_beta(root_state, depth, -999999, 999999)

    def _alpha_beta(self, root_state, depth, alpha, beta):
        if depth <= 0 or root_state.is_terminal:
            return root_state.balance

        if root_state.turn == Color.WHITE:  # assuming white = player & black = opponent
            for child_state in root_state.next_states:

                alpha_beta = self._alpha_beta(child_state, depth - 1, alpha, beta)

                if alpha_beta > alpha:
                    alpha = alpha_beta
                    root_state.next_move = child_state
                if alpha >= beta:
                    return beta
            return alpha
        else:
            for child_state in root_state.next_states:

                alpha_beta = self._alpha_beta(child_state, depth - 1, alpha, beta)

                if alpha_beta < beta:
                    beta = alpha_beta
                    root_state.next_move = child_state
                if alpha >= beta:
                    return alpha
            return beta
