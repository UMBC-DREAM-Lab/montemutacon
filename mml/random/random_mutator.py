from mml.policy import ExpansionPolicy, SimulationPolicy, TreePolicy
from mml.node import Node

class RandomMutator:
    def __init__(self, *, tree_policy: TreePolicy, expansion_policy: ExpansionPolicy, simulation_policy: SimulationPolicy):
        self.tree_policy = tree_policy
        self.expansion_policy = expansion_policy
        self.evaluation_policy = simulation_policy

    def run(self, iterations, sample, starting_state):
        root = Node(-1, sample, starting_state, "root")
        
        # It is the root, we need to expand it anyway
        node = root
        for _ in range(iterations):
            self.expansion_policy.evaluate(node)
            # Selection phase. In random this should always
            # evaluate to children[0]
            node = self.tree_policy.evaluate(node)

            self.evaluation_policy.evaluate(node)

            if node.is_terminal:
                break

            key = tuple(sorted(node.path_to_me))
            starting_state['tried_combinations'][key] = 1
        return root

    def recover_path(self, root: Node):
        path = [root]
        node = root
        while node.expanded() and not node.is_terminal:
            node = node.children[0]
            path.append(node)
        return path