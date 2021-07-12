from mml.policy import SimulationPolicy
from mml.node import Node

class RandomSimulationPolicy(SimulationPolicy):

    """
    There is no simmulation for random. This is mainly so we can use the same API
    for both cases.
    """
    def __init__(self, *, model, mutations, classification_function) -> None:
        super().__init__()
        self.model = model
        self.mutations = mutations
        self.classification_function = classification_function

    def evaluate(self, node: Node):
        """
        Performs the evaluation, and marks the node as terminal if classification function returns
        0.
        """
        thing = self.classification_function(self.model, node.sample)
        node.is_terminal = (thing == 0)
        return


    def __repr__(self):
        return "RandomSimulationPolicy"