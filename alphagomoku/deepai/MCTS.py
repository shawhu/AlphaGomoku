import numpy as np 
import copy

def softmax(x):
    probs = np.exp(x-np.max(x))
    probs /= np.sum(probs)
    return probs

class TreeNode:
    def __init__(self,parent,prior_p):
        self._parent = parent
        self._childern = {} # Save childre nodes in Hash data structure
        self._n_visits = 0
        self._Q = 0
        self._u = 0
        self._P = prior_p

    def expand(self,action_priors):
        for action, prob in action_priors:
            if action not in self._childern:
                self._childern[action] = TreeNode(self,prob)

    def select(self,c_puct):
        return max(self._childern.items(),
            key=lambda action_node: action_node[1].get_value(c_puct)
            )

    def update(self,leaf_value):
        self._n_visits += 1
        self._Q += 1.0*(leaf_value - self._Q) / self._n_visits

    def update_recuresive(self, leaf_value):
        if self._parent:
            self._parent.update_recuresive(-leaf_value)
        self.update(leaf_value)

    def get_value(self,c_puct):
        self._u = (c_puct * self._P * np.sqrt(self._parent._n_visits) / (1 + self._n_visits))
        return self._Q + self._u

    def is_leaf(self):
        return self._childern == {}

    def is_root(self):
        return self._parent is None

class MCTS:
    def __init__(self,value_function, c_puct, n_playout):
        self._root = TreeNode(None, 1.0)
        self._value_function = _value_function
        self._c_puct = c_puct
        self._n_playout = n_playout

    def _playout(self, state):
        node = self._root
        while 1:
            if node.is_leaf():
                break
            action, node = node.select(self._c_puct)
            # TODO apply move action

        # TODO return (action, probility, leaf value)
        action_probs, leaf_value = self._value_function(state)

        # TODO return 
        end, winner = 

        if not end:
            node.expand(action_probs)
        else:
            # Game end process

    def get_move_probs(self, state, temperature, eps=1e-10):
        for i in range(self._n_playout):
            _state = copy.deepcopy(state)
            self._playout(_state)

        action_visits = [(action, node._n_visits) 
                        for action, node in self._root._childern.items()]
        actions, visits = zip(*action_visits)
        actions_probs = softmax(1.0/temperature*np.log(np.array(visits) + eps))
        return actions, action_probs

    def update_with_move(self, move):
        if move in self._root._childern:
            self._root = self._root._childern[move]
            self._root._parent = None
        else:
            self._root = TreeNode(None, 1.0)

    def __str__(self):
        return "Monte Carlo Tree Search"

class MCTSPlayer:
    def __init__(self, value_function, c_puct, n_playout, is_selfplay, verbose=False):
        self.mcts = MCTS(value_function, c_puct, n_playout)
        self._is_selfplay = is_selfplay
        self.verbose = verbose

    def set_player_index(self, player):
        self.player = player

    def reset_player(self):
        self.mcts.update_with_move(-1)

    def get_action(self, board, temperature, return_prob=0):
        # TODO initiate move prob 
        move_probs = np.zeros()

        if board.is_available():
            actions, probs = self.mcts.get_move_probs(board, temperature)

            # TODO consider flatten data structure
            move_probs[list(actions)] = probs
            if self._is_selfplay:
                move = np.random.choice(
                    actions,
                    p=0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs)))
                )
                self.mcts.update_with_move(move)
            else:
                move = np.random.choice(actions,p=probs)
                self.mcts.update_with_move(-1)

            if return_prob:
                return move, move_probs
            else:
                return move
        else:
            if self.verbose:
                # TODO need modification
                print("The board is full")

    def __str__(self):
        return "Monte Carlo Tree Search: {player}".format(player=player)