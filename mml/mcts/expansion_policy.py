from mml.policy import ExpansionPolicy
from mml.node import Node
import copy


class MctsExpansionPolicy(ExpansionPolicy):
    def __init__(self, mutations_table):
        self.mutations = mutations_table

    def evaluate(self, node: Node) -> None:
        """
        Create a child node for every available mutation from this node.
        """
        options = []

        # figure out all acceptable mutations
        for key, value in self.mutations.items():
            potential_path = [value["mutation"].id, *node.path_to_me]
            potential_path.sort()
            # A tuple is hashable. A list is not.
            potential_path = tuple(potential_path)

            allowed_by_predicate = value["predicate"](node.sample, node.state)
            not_tried_before = potential_path not in node.state["combinations_tried"]

            if allowed_by_predicate and not_tried_before:
                options.append(value["mutation"])

        # Make a child for EACH mutation
        for index, option in enumerate(options):
            child = Node(
                option.id,
                copy.deepcopy(node.sample),
                copy.copy(node.state),
                name=str(index),
                parent=node,
            )
            # Apply the mutation
            serialized_option = option.apply(child.sample, child.state)
            child.is_mutated = True
            child.serialized_option = serialized_option
            node.children.append(child)

        return options

    def __repr__(self):
        return "MctsExpansionPolicy"
