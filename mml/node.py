from typing import List
from mml.mutations import Mutation


class Node:
    """
    A single node in the tree. It is used in both MCTS and Random search, allthough
    not all member variables are used in both. Semantically, a node is one mutation on
    top of whatever mutations were on the parent node.

    Contains the current state of the malware, i.e. how many strings have been added,
    how many dlls, how many functions, etc.

    It also contains the sample, with all the mutations applied so far (including this node's).
    """

    def __init__(self, mutation: int, sample, state=None, name="", parent=None):
        self.children: List[Node] = []
        self.state = {} if state == None else state
        self.visit_count = 0
        self.score = 0
        self.mutation_id = mutation
        self.sample = sample
        self.name = name
        self.parent: Node = parent
        self.is_terminal = False
        self.serialized_option = "None"
        self.path_to_me = []
        self.is_mutated = False

        p: Node = self
        while p != None:
            if p.mutation_id != None:
                self.path_to_me.append(p.mutation_id)
            p = p.parent

    def expanded(self) -> bool:
        return len(self.children) > 0

    
    def __repr__(self):
        parent_name = self.parent.name if self.parent != None else "None"
        return f"Node {parent_name} : {self.name}, score: {self.score}, visits: {self.visit_count}"

    def __str__(self):
        return "Potato"
