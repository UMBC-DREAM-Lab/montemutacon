from mml.node import Node
import numpy as np

class MctsMutator:
    def __init__(self, *, tree_policy, expansion_policy, simulation_policy):

        self.tree_policy = tree_policy
        self.expansion_policy = expansion_policy
        self.simulation_policy = simulation_policy

    def run(self, iterations, sample, starting_state):
                
        root = Node(-1, sample, starting_state, "root")
        # It is the root, we need to expand it anyway
        self.expansion_policy.evaluate(root)
        for _ in range(iterations):
            node = root
            search_path = [node]

            # Selection phase
            while node.expanded():
                node = self.tree_policy.evaluate(node)
                search_path.append(node)

            if node.is_terminal:
                continue

            if node.visit_count != 0:
                # We've seen the node previously and we are back, so we have to
                # expand it
                self.expansion_policy.evaluate(node)
                # We only check for a child if we were able to expand this.
                # Otherwise it means we can no longer continue down this path.
                if len(node.children) != 0:
                    node = self.tree_policy.evaluate(node)
            else:
                key = tuple(sorted(node.path_to_me))
                starting_state['tried_combinations'][key] = 1

            # Node here will either be the original one (that we visit for the
            # first time) or one of it's children since we jut expanded it
            path = self.simulation_policy.evaluate(node)

            # The score is negative here, so smaller path values will result in
            # a higher score
            score = -len(path) if path else -np.inf

            # backpropage the value
            for node in reversed(search_path):
                if node.score != -np.inf and score != -np.inf:
                    node.score += score
                else:
                    node.score = score

                node.visit_count += 1

        return root

    def get_optimum_child(self, node: Node) -> Node:
        """
        This is done during path recovery. We absolutely want to avoid children
        with 0 visits, as it means we never explored them. 
        """
        scores = []
        for child in node.children:
            if child.visit_count == 0:
                scores.append(-np.inf)
            else:
                scores.append(child.score / child.visit_count)
        index = np.argmax(scores)
        return node.children[index]

    def recover_path(self, root: Node):
        node = root
        path = [root]
        while node.expanded() and not node.is_terminal:
            node = self.get_optimum_child(node)
            path.append(node)
        return path
