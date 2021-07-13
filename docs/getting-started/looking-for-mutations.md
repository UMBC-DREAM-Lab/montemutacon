---
layout: default
title: 'Looking for mutations'
parent: 'Getting Started'
nav_order: 3
---

# {{page.title}}

Next we will use all of the things we've obtained so far, to try and produce a
mutation. You can find the final result of this page here <a
href="{{'assets/example.py.txt' | absolute_url}}">example.py</a>. We will start
by building from the bottom up.

## Transformation pipeline
As we mentioned earlier, the pipeline will featurize a given sample. We make our
own as follows:

```py
from utils.pipeline import Pipeline as CustomPipeline
pipeline = CustomPipeline(
    "full_pipeline_surrogate.dat",
    ["libs_vectorizer_surrogate.dat", "funcs_vectorizer_surrogate.dat"],
)
```
<div class="alert alert-warning">
    Remember to change the paths to wherever you placed those files.
</div>


## Classification function
This is a function the algorithm will call whenever it wants a prediction out of
your model. As the algorithm is model agnostic, you need to tell it how to use
your model. The classification must have the following signature, it returns 0
if the sample was classified as benign and 1 if it was classified as malicious.
model is _your_ model, and sample is a dict like the one in the json file you
downloaded earlier.

```py
def classification_function(model, sample) -> int:
    to_convert = sample.copy()
    to_convert["imported_libs"] = [[*to_convert["imported_libs"]]]
    to_convert["imported_funcs"] = [[*to_convert["imported_funcs"]]]
    df = pd.DataFrame.from_dict(to_convert)
    df.drop(columns=["y"], inplace=True)

    # Transform the sample through the pipeline. Depending on your model you 
    # might not need this
    transform = pipeline.transform(df, ["imported_libs", "imported_funcs"])
    return model.predict(transform)[0]
```

The content of this function depends entirely on you. For our specific
pre-trained model we need to convert the sample as shown, then transform it. 

<div class="alert alert-info">
    Please note that <code>["imported_libs", "imported_funcs"]</code> matches 
    the order we added the vectorizers in the pipeline.
</div>

## Model
To load the model we simply need to use dill (a replacement of pickle. Should
have been installed from `environment.yml`)

```py
import dill as pickle
model = pickle.load(open('trained_tree.dat', 'rb'))
```

## Tree Policy
The mcts tree policy. For details refer to the paper. We use 2 as our
exploration coefficient.

```py
from mml.mcts.tree_policy import MctsTreePolicy
tree_policy = MctsTreePolicy(2)
```
## Expansion Policy
How to expand a new node. The paper includes the details. `mutations_table` is a
data structure that contains the available mutations plus if it can be applied.
You can read more here. The given mutations_table works with samples.json you
downloaded.

```py
from mml.mcts.expansion_policy import MctsExpansionPolicy
from tables import mutations_table
expansion_policy = MctsExpansionPolicy(mutations_table)
```

## Simulation Policy
The simulation policy dictates how to handle the simulation step of MCTS. We use
25 for the simulation depth here.
```py
from mml.mcts.simulation_policy import MctsSimulationPolicy

simulation_policy = MctsSimulationPolicy(
    model,
    25,
    expansion_policy,
    mutations_table,
    classification_function,
)
```

## The mutator
```py
from mml.mcts.mcts_mutator import MctsMutator
mcts_mutator = MctsMutator(
    tree_policy=tree_policy,
    expansion_policy=expansion_policy,
    simulation_policy=simulation_policy,
)
```

## Loading our data set
We need to find all the malicious samples, there is no point trying to find
mutations on a benign sample.
```py
import json
samples = json.load(open('samples.json'))
malware = [sample for sample in samples if sample['y'] == 1]
```

## Finally, running everything
You could use the recovered path in many other ways. Here we are just storing it
in an array. You could also store it to disk to later use it in some way. Please
note that you must **NOT** remove the `tried_combinations` part of
`starting_state`. The algorithm needs it.
```py
results = []
for sample in malware:
    if classification_function(model, sample) == 0:
        # Skip it, it is already misclassified
        results.append(
            { "skipped": True, "changes": [] }
        )

    tried_combinations = {}
        
    # This is used to keep track of how many times we have performed these
    # changes below. You can add or remove things here to match your setup
    starting_state = {
        "added_strings": 0,
        "removed_strings": 0,
        "added_libs": 0,
        "entropy_changes": 0,
        "tried_combinations": tried_combinations, # This is the only one you cannot remove. You need this to there
    }
    root = mcts_mutator.run(300, sample, starting_state)
    path = mcts_mutator.recover_path(root)

    if path[-1].is_terminal:
        mutations = [node.serialized_option for node in path]
        results.append(
            { "skipped": False, "changes": mutations }
        ) 
    else:
        results.append(
            { "skipped": False, "changes": [] }
        )
```

# The end (?)
This concludes the getting started tutorial. Reminder that you can find the
whole python file here <a href="{{'assets/example.py.txt' | absolute_url}}"
target="_blank" rel="noopener noreferrer">example.py</a>
