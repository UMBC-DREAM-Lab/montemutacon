from mml.policy import ExpansionPolicy
from mml.node import Node
import copy
import numpy as np

class RandomExpansionPolicy(ExpansionPolicy):
    """
    Expansion policy for randomm search. In this case we just pick one of the available children at random, and
    use that.
    """
    def __init__(self, mutations_table):
        self.mutations = mutations_table

    def evaluate(self, node: Node) -> None:
        options = []

        # figure out all of the mutations that can be applied to this node
        for key, value in self.mutations.items():
            potential_path = [value["mutation"].id, *node.path_to_me]
            potential_path.sort()
            potential_path = tuple(potential_path)

            allowed_by_predicate = value["predicate"](node.sample, node.state)
            not_tried_before = potential_path not in node.state["tried_combinations"]

            if allowed_by_predicate and not_tried_before:
                options.append(value["mutation"])

        # pick on at random
        selection = np.random.choice(options, 1)[0]
        child = Node(
            selection.id,
            copy.deepcopy(node.sample),
            copy.copy(node.state),
            name='',
            parent=node,
        )

        # apply it
        serialized_option = selection.apply(child.sample, child.state)
        child.is_mutated = True
        child.serialized_option = serialized_option
        node.children.append(child)
    
    def __repr__(self):
        return "RandomExpansionPolicy"