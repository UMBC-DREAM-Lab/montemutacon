from abc import ABC, abstractclassmethod
from os import scandir
import numpy as np
import random
import json
from json import JSONEncoder

class SerializedMutation:
    def __init__(self, id: int, description: str):
        self.id = id
        self.description = description

    def __repr__(self) -> str:
        return f'{self.id} - {self.description}'

    def __str__(self) -> str:
        return self.__repr__()
    

class MutationEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Mutation(ABC):
    """
    Abstract base class for all of the mutations
    """

    def __init__(self, id=-1):
        self.id = id

    @abstractclassmethod
    def apply(self, sample, state) -> SerializedMutation:
        """
        The apply function should modify the state and sample variables to
        showcase the changes such a mutation would have on the binary. You are
        free to change the sample and state dictionaries as you see fit to match
        your environment.
        """
        pass


class AddStringMutation(Mutation):
    """
    Adds one string to the sample
    """

    def __init__(self, id=1):
        super().__init__(id)

    def apply(self, sample, state) -> SerializedMutation:
        sample["num_strings"] += 1

        if state["added_strings"]:
            state["added_strings"] += 1
        else:
            state["added_strings"] = 1

        return SerializedMutation(id=self.id, description=self.__repr__())

    def __repr__(self):
        return "Add a string"


class AddSectionMutation(Mutation):
    """
    Adds one section to the sample
    """

    def __init__(self, size=1024, id=2):
        super().__init__(id)
        self.size = size

    def apply(self, sample, state) -> SerializedMutation:
        sample["num_sections"] += 1
        sample["file_size"] += self.size

        return SerializedMutation(id=self.id, description=self.__repr__())

    def __repr__(self):
        return f"Add a section of {self.size} bytes"


class ImportFunctionMutation(Mutation):
    """
    Adds one function, and potentially it's accompanied dll to the sample
    """

    def __init__(self, function_table, id=3):
        super().__init__(id)
        self.function_table = function_table

    def apply(self, sample, state) -> SerializedMutation:
        keys = list(self.function_table.keys())
        choice = np.random.choice(keys, 1)[0]
        while choice in sample["imported_funcs"] and state["added_libs"] < len(self.function_table):
            choice = np.random.choice(keys, 1)[0]

        contains_dll = False
        for dll_candidate in self.function_table[choice]:
            if dll_candidate in sample["imported_libs"]:
                contains_dll = True
                break

        if not contains_dll:
            dll_index = np.random.randint(len(self.function_table[choice]))
            sample["imported_libs"].append(self.function_table[choice][dll_index])

        sample["imported_funcs"].append(choice)
        state["added_libs"] += 1
        return SerializedMutation(
            id=self.id,
            description=f"Add {self.function_table[choice][0]}::{choice} function to imports",
        )

    def __repr__(self):
        return "Add an import"


class ChangeTimestampMutation(Mutation):
    """
    Changes the timestamp of the sample, one step towards the  target timestamp
    """

    def __init__(self, target_timestamp, step=1, id=4):
        super().__init__(id)
        self.target_timestamp = target_timestamp
        self.step = step

    def apply(self, sample, state) -> SerializedMutation:
        sample_ts = sample["timestamp"]

        if sample_ts > self.target_timestamp:
            sample_ts -= self.step
        elif sample_ts < self.target_timestamp:
            sample_ts += self.step

        sample["timestamp"] = sample_ts
        return SerializedMutation(id=self.id, description=self.__repr__())

    def __repr__(self):
        return f"Move the timestamp by {self.step} towards {self.target_timestamp}"


class AddBytesMutation(Mutation):
    """
    Adds one byte to some section of the sample. Also extends the
    corresponding meta data
    """

    def __init__(self, num_bytes=1, id=5):
        super().__init__(id)
        self.num_bytes = num_bytes

    def apply(self, sample, state) -> SerializedMutation:
        sample["file_size"] += self.num_bytes
        return SerializedMutation(id=self.id, description=self.__repr__())

    def __repr__(self):
        return f"Add {self.num_bytes} byte(s) to some section the file"


class AddCodeBytesMutation(Mutation):
    """
    Adds one byte to the code section of the sample. Also extends the
    corresponding meta data
    """

    def __init__(self, num_bytes=1, id=5):
        super().__init__(id)
        self.num_bytes = num_bytes

    def apply(self, sample, state) -> SerializedMutation:
        sample["sizeof_code"] += self.num_bytes
        sample["file_size"] += self.num_bytes
        return SerializedMutation(id=self.id, description=self.__repr__())

    def __repr__(self):
        return f"Add {self.num_bytes} byte(s) to the code section the file"


class RemoveDebugMutation(Mutation):
    """
    Removes the debug flag from the sample
    """

    def __init__(self, id=6):
        super().__init__(id)

    def apply(self, sample, state) -> SerializedMutation:
        sample["has_debug"] = 0

        return SerializedMutation(id=self.id, description=self.__repr__())

    def __repr__(self):
        return "Remove debug flag"


class ChangeSignatureMutation(Mutation):
    """
    Changes the has_signature flag, to the specified option
    """

    def __init__(self, option: bool, id=7):
        super().__init__(id)
        self.option = option

    def apply(self, sample, state) -> SerializedMutation:
        sample["has_signature"] = "1" if self.option else "0"
        return SerializedMutation(id=self.id, description=self.__repr__())

    def __repr__(self):
        return f"Set has_signature to {self.option}"


class RemoveStringMutation(Mutation):
    def __init__(self, id=9):
        super().__init__(id)

    def apply(self, sample, state) -> SerializedMutation:
        sample["num_strings"] -= 1
        state["removed_strings"] += 1
        return SerializedMutation(id=self.id, description=self.__repr__())

    def __repr__(self):
        return "Remove a string"


class AddStringWithSizeMutation(Mutation):
    def __init__(self, string_size, id=10):
        super().__init__(id)
        self.string_size = string_size

    def apply(self, sample, state) -> SerializedMutation:
        sample["num_strings"] += 1
        sample["file_size"] += self.string_size
        state["added_strings"] += 1
        return SerializedMutation(id=self.id, description=self.__repr__())

    def __repr__(self):
        return f"Add one string of {self.string_size} bytes"


class ChangeStringEntropyMutation(Mutation):
    def __init__(self, target_entropy, step, id=10):
        super().__init__(id)
        self.target_entropy = target_entropy
        self.step = step

    def apply(self, sample, state) -> SerializedMutation:
        sample["num_strings"] += 1
        sample_entropy = sample["strings_entropy"]

        if sample_entropy > self.target_entropy:
            sample_entropy -= self.step
        elif sample_entropy < self.target_entropy:
            sample_entropy += self.step
        sample["strings_entropy"] = sample_entropy

        state["entropy_changes"] += 1
        return SerializedMutation(id=self.id, description=self.__repr__())

    def __repr__(self):
        return f"Change string entropy towards {self.target_entropy} by adding a string"


class ChangeStringEntropyWithSizeMutation(Mutation):
    def __init__(self, target_entropy, step, size, id=10):
        super().__init__(id)
        self.target_entropy = target_entropy
        self.step = step
        self.size = size

    def apply(self, sample, state) -> SerializedMutation:
        sample["num_strings"] += 1
        sample_entropy = sample["strings_entropy"]

        if sample_entropy > self.target_entropy:
            sample_entropy -= self.step
        elif sample_entropy < self.target_entropy:
            sample_entropy += self.step
        sample["strings_entropy"] = sample_entropy
        sample["file_size"] += self.size

        state["entropy_changes"] += 1

        return SerializedMutation(id=self.id, description=self.__repr__())

    def __repr__(self):
        return f"Change string entropy towards {self.target_entropy} by adding a string of size {self.size}"
