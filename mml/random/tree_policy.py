from mml.policy import TreePolicy
from mml.node import Node

class RandomTreePolicy(TreePolicy):
    """
    Selecting the "best" child for this node. In Random Search we only have
    a single option
    """
    def __init__(self):
        pass

    def evaluate(self, node: Node) -> Node:
        """
        We should only have one child. If there is more than one, something is wrong. But we don't deal with it.
        We always return node.children[0]
        """
        if len(node.children) > 0:
            return node.children[0]
        else:
            return None

    def __repr__(self):
        return 'RandomTreePolicy'