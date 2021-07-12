from abc import ABC, abstractclassmethod
from mml.node import Node


class TreePolicy(ABC):
    """
    A tree policy decides which will be the next child to traverse
    during the traversal part of the algorithm
    """

    @abstractclassmethod
    def evaluate(self, node: Node) -> Node:
        """
        Should return the next node to be traversed
        """
        pass


class ExpansionPolicy(ABC):
    """
    An expansion policy dictates which of the available options are valid in the
    expansion phase of the algorithm
    """

    @abstractclassmethod
    def evaluate(self, node: Node) -> None:
        """
        Expands the given node. Expansion includes creating the children of this node, one
        child for every mutation that is allowed to be applied to the given node. The children
        should also have their own mutations to them. Creating a child should not change the current node's
        state (i.e. malware features).
        """
        pass


class SimulationPolicy(ABC):
    """
    A simulation policy (also seen as rollout policy) dictates how the algorithm
    will evaluate states while in the rollout phase.
    """

    @abstractclassmethod
    def evaluate(self, node: Node):
        pass