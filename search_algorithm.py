from state import *


class SearchAlgorithm:

    @staticmethod
    def alpha_beta(root_state, depth):
        return SearchAlgorithm._alpha_beta(root_state, depth, -999999, 999999)

    @staticmethod
    def _alpha_beta(root_state, depth, alpha, beta):
        if depth <= 0 or root_state.is_terminal():
            return root_state.balance
        else:
            root_state.generate_next_states()

        if root_state.turn == Color.WHITE:  # assuming white = player & black = opponent
            for child_state in root_state.next_states:
                alpha_beta_result_for_this_child = SearchAlgorithm._alpha_beta(child_state, depth - 1, alpha, beta)
                if alpha_beta_result_for_this_child > alpha:
                    alpha = alpha_beta_result_for_this_child
                    root_state.next_move = child_state
                if alpha >= beta:
                    return beta
            return alpha
        else:
            for child_state in root_state.next_states:
                alpha_beta_result_for_this_child = SearchAlgorithm._alpha_beta(child_state, depth - 1, alpha, beta)
                if alpha_beta_result_for_this_child < beta:
                    beta = alpha_beta_result_for_this_child
                    root_state.next_move = child_state
                if alpha >= beta:
                    return alpha
            return beta
