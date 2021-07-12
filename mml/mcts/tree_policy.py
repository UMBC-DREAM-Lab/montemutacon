import numpy as np

from mml.policy import TreePolicy
from mml.node import Node

def ucb1(node: Node, child: Node, c: float) -> float:
    # Dividing by 0 is not a good idea. This also makes unseen children
    # the perfect candidate. Meaning we will always explore each child at least once!
    if child.visit_count == 0:
        return np.inf
    return (child.score / child.visit_count) + (c * np.sqrt(np.log(node.visit_count) / child.visit_count))

class MctsTreePolicy(TreePolicy):

    def __init__(self, exploration_coefficient: float):
        self.c = exploration_coefficient

    def evaluate(self, node: Node) -> Node:
        """
        The best child is the child with the highest UCB1 score
        """
        children = node.children
        scores = [ucb1(node, child, self.c) for child in children]
        index = np.argmax(scores)
        return node.children[index]
    
    def __repr__(self):
        return 'MctsTreePolicy'