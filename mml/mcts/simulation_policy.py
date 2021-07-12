from mml.policy import SimulationPolicy, ExpansionPolicy
from mml.node import Node
import pandas as pd
import numpy as np
import copy


class MctsSimulationPolicy(SimulationPolicy):
    def __init__(
        self, model, max_depth, exp_policy: ExpansionPolicy, mutations, classification_function
    ):
        super().__init__()
        self.model = model
        self.max_depth = max_depth
        self.exp_policy = exp_policy
        self.mutations = mutations
        self.classification_function = classification_function

    def evaluate(self, node: Node):
        """
        In essence, this performs random search from this node, up to the maximum depth. If it finds a
        successfull mutation, it terminates early.
        """

        # This couldbe true if the current node is terminal. We just need to reconstruct the
        # path to us, and return it
        if self.classification_function(self.model, node.sample) == 0:
            node.is_terminal = True
            path = [node.mutation_id]
            p = node.parent
            while p != None:
                path.append(p.mutation_id)
                p = p.parent
            return [node.mutation_id]

        current_node = copy.deepcopy(node)
        self.exp_policy.evaluate(current_node)
        path = []
        
        iterations = 0
        while iterations < self.max_depth:

            if not current_node.expanded():
                self.exp_policy.evaluate(current_node)

            # The mutation, should have already been applied
            if not current_node.is_mutated:
                self.mutations[current_node.mutation_id]["mutation"].apply(
                    current_node.sample, current_node.state
                )

            y_hat = self.classification_function(self.model, current_node.sample)

            path.append(current_node.mutation_id)

            if y_hat == 0:
                # print('Found a successful mutation')
                return path

            if len(current_node.children) == 0:
                # Welp we have no more options here, we've tried everything
                return path

            choice = np.random.choice(current_node.children, 1)[0]
            current_node = choice
            iterations += 1

        return path

    def __repr__(self):
        return "MctsSimulationPolicy"
