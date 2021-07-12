from mml.mutations import MutationEncoder
from utils.features import EmberFeatures
from utils.pipeline import Pipeline as CustomPipeline

from mml.mcts.mcts_mutator import MctsMutator
from mml.mcts.simulation_policy import MctsSimulationPolicy
from mml.mcts.expansion_policy import MctsExpansionPolicy
from mml.mcts.tree_policy import MctsTreePolicy

from mml.random.random_mutator import RandomMutator
from mml.random.tree_policy import RandomTreePolicy
from mml.random.expansion_policy import RandomExpansionPolicy
from mml.random.simulation_policy import RandomSimulationPolicy

import pandas as pd
import dill as pickle
import json
import datetime
from joblib import Parallel, delayed
import multiprocessing
import time
# import keras
from pathlib import Path
import math
import os
import sys

# This table includes the available mutations along
# with a predicate on whether they can be applied or not
from tables import mutations_table

"""
This is the full transformation pipeline, specific to the surrogate model. The
first is the standard transformers, and the second argument is an array of
transformers for vectorized and categorical features. In the same order that was
used in the training of the surrogate model. If your model does not require
something like this (or something completely different), you can skip it as it
is only used in classification_function below.
"""
pipeline = CustomPipeline(
    "models/surrogate/full_pipeline_surrogate.dat",
    ["models/surrogate/libs_vectorizer_surrogate.dat", "models/surrogate/funcs_vectorizer_surrogate.dat"],
)


def classification_function(model, sample):
    """
    You can use this to change how a model predicts it's value. This function
    depends entirely on how your model functions, and what data you are using.
    Below we have an example of what we did. You need to adjust this to your use
    case.

    In our example here, we need to transform the sample through the pipeline so
    our model can classify it. We also need to change the layout of
    imported_libs and imported_funcs as Pandas needs it this way.
    """
    to_convert = sample.copy()
    to_convert["imported_libs"] = [[*to_convert["imported_libs"]]]
    to_convert["imported_funcs"] = [[*to_convert["imported_funcs"]]]
    df = pd.DataFrame.from_dict(to_convert)
    df.drop(columns=["y"], inplace=True)

    # Transform the sample through the pipeline. Depending on your model you might not need this
    transform = pipeline.transform(df, ["imported_libs", "imported_funcs"])
   
    # For MLP model
    # thing = (model.predict(transform) > 0.5).astype("int32")
    # return thing[0][0]
   
    # For the Decision Tree model
    thing = model.predict(transform)
    return thing[0]


def mcts_thread_function(sample, i, exp, iterations, depth):
    print(f"Processing sample {i}")
    """
    Swap this to change how a model is loaded. The model will be just passed to the
    classification function above, so you can use it however you want. We need to do it this way
    as some models cannot be pickled by the joblib library later on. So each thread loads the model
    for itself. If that does not work with your model for some reason, you will need to rework this.
    """
    # You probably don't want to use the actual victim model. This is just
    # an example on how you can use different models
    # model = keras.models.load_model("models/victim/mlp_model")
    model = pickle.load(open('models/surrogate/trained_tree.dat', 'rb'))

    exploration_coefficient = exp
    simulation_depth = depth

    tree_policy = MctsTreePolicy(exploration_coefficient)
    expansion_policy = MctsExpansionPolicy(mutations_table)
    """
    You can pass different classification functions here, to change how
    classification happens.
    """
    simulation_policy = MctsSimulationPolicy(
        model,
        simulation_depth,
        expansion_policy,
        mutations_table,
        classification_function,
    )
    mcts_mutator = MctsMutator(
        tree_policy=tree_policy,
        expansion_policy=expansion_policy,
        simulation_policy=simulation_policy,
    )

    if classification_function(model, sample) == 0:
        # print('Sample is misclassified in the first place, skipping...')
        return {"skipped": True, "changes": [], "time": 0}

    start = time.time()
    root = mcts_mutator.run(iterations, sample)
    path = mcts_mutator.recover_path(root)
    end = time.time()
    if path[-1].is_terminal:
        mutations = [node.serialized_option for node in path]
        # print(f'Found terminal path : {mutations}')
        return {"skipped": False, "changes": mutations, "time": end - start}
    else:
        # print('Could not find a mutation')
        return {"skipped": False, "changes": [], "time": end - start}


def random_thread_function(sample, i, iterations):
    print(f"Processing sample {i}")
    # You probably don't want to use the actual victim model. This is just
    # an example on how you can use different models
    # model = keras.models.load_model("models/victim/mlp_model")     
    model = pickle.load(open('models/surrogate/trained_tree.dat', 'rb'))

    tree_policy = RandomTreePolicy()
    expansion_policy = RandomExpansionPolicy(mutations_table)
    simulation_policy = RandomSimulationPolicy(
        model=model,
        mutations=mutations_table,
        classification_function=classification_function,
    )

    random_mutator = RandomMutator(
        tree_policy=tree_policy,
        expansion_policy=expansion_policy,
        simulation_policy=simulation_policy,
    )

    if classification_function(model, sample) == 0:
        # print('Sample is misclassified in the first place, skipping...')
        return {"skipped": True, "changes": [], "time": 0}

    start = time.time()
    root = random_mutator.run(iterations, sample)
    path = random_mutator.recover_path(root)
    end = time.time()
    if path[-1].is_terminal:
        mutations = [node.serialized_option for node in path]
        # print(f'Found terminal path : {mutations}')
        return {"skipped": False, "changes": mutations, "time": end - start}
    else:
        # print('Could not find a mutation')
        return {"skipped": False, "changes": [], "time": end - start}


if __name__ == "__main__":
    """
    Which GPU  node we want to use. We can use nvidia-smi to see GPU usage. Only
    applicable if your model uses GPU processing. The algorithm itself does not
    use cuda.
    """
    # os.environ["CUDA_VISIBLE_DEVICES"] = "1"

    """
    Settings for the mutator
    mutator:                    Which mutator to use. Valid values are "mcts" 
                                and "random"
    exploration_coefficient:    Only makes sense for mcts, ignored for random
    simulation_depth:           Only makes sense for mcts, ignored for random
    iterations:                 How many iterations mcts will execute, and the 
                                depth for random
    """
    mutator = "random"
    exploration_coefficient = 2
    simulation_depth = 10
    iterations = 5

    """
    This is specific to loading the things we want from the Ember2018 dataset.
    If the model is trained on different datasets you need to adjust this part.
    We are using a bit under 200000 samples, and generate mutations on those.

    You can see the features we picked out of the Ember2018 Data set. We have
    specific ones we wanted stored in MongoDB. You can adjust here as you see
    fit to match your own environment. You can use any other data source as long
    as your models know about this, and you modify the mutations accordingly.
    """
    num_samples = 200000

    features = EmberFeatures(collection="test", num_instances=num_samples)
    labels = features.get_feature("label")
    df = pd.DataFrame(
        list(
            zip(
                features.get_feature("strings_entropy"),
                features.get_feature("num_strings"),
                features.get_feature("file_size"),
                features.get_feature("num_exports"),
                features.get_feature("num_imports"),
                features.get_feature("has_debug"),
                features.get_feature("has_signature"),
                features.get_feature("timestamp"),
                features.get_feature("sizeof_code"),
                features.get_feature("entry"),
                features.get_feature("num_sections"),
                features.get_feature("imported_libs"),
                features.get_feature("imported_funcs"),
                features.get_feature("label"),
            )
        ),
        columns=[
            "strings_entropy",
            "num_strings",
            "file_size",
            "num_exports",
            "num_imports",
            "has_debug",
            "has_signature",
            "timestamp",
            "sizeof_code",
            "entry",
            "num_sections",
            "imported_libs",
            "imported_funcs",
            "y",
        ],
    )
    df["has_debug"] = df["has_debug"].astype(str)
    df["has_signature"] = df["has_signature"].astype(str)
    df["entry"] = df["entry"].astype(str)

    malicious = df[df.y == 1]

    """
    Figure out how many to cores to use to run in parallel. Adjust as you see fit
    """
    num_cores = multiprocessing.cpu_count()
    num_jobs = num_cores if num_cores == 1 else math.floor(num_cores / 2)
    # num_jobs = 35
    print(f"Running with {num_jobs} jobs")

    results = None

    run_start = time.time()
    if mutator == "mcts":
        results = Parallel(n_jobs=num_jobs)(
            delayed(mcts_thread_function)(
                malicious.iloc[i].to_dict(),
                i,
                exploration_coefficient,
                iterations,
                simulation_depth,
            )
            for i in range(len(malicious))
        )
    elif mutator == "random":
        results = Parallel(n_jobs=num_jobs)(
            delayed(random_thread_function)(malicious.iloc[i].to_dict(), i, iterations)
            for i in range(len(malicious))
        )
    else:
        print(f"Invalid mutator {mutator}. Exiting...")
        sys.exit(1)

    run_end = time.time()

    """
    Save the results ina JSON file. You probably want a better naming scheme here!
    """
    current_date_and_time = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")

    directory = Path(f"results/{mutator}")
    directory.mkdir(parents=True, exist_ok=True)
    file_name = Path(directory, f"result-{current_date_and_time}.json")

    tricked = 0
    for r in results:
        if len(r["changes"]) > 1:
            tricked += 1

    output = {
        "settings": {
            "exploration_coefficient": exploration_coefficient,
            "simulation_depth": simulation_depth,
            "iterations": iterations,
            "mutator": mutator,
            "found": tricked,
            "runtime": run_end - run_start
        },
        "results": results,
    }
    with open(file_name, "w+") as f:
        json.dump(output, f, cls=MutationEncoder)


    
    message = ''
    if mutator == 'mcts':
        message = (
            f"Finished run using the {mutator} mutator and {num_samples} samples\n"
            "Settings:\n"
                f"\tExploration Coefficient: {exploration_coefficient}\n"
                f"\tDepth: {iterations}\n"
                f"\tSimulation Depth: {simulation_depth}\n"
                f"\tFound mutations for {tricked}/{len(malicious)} malicious samples\n"
        )
    else:
        message = (
            f"Finished run using the {mutator} mutator and {num_samples} samples\n"
            "Settings:\n"
                f"\tDepth: {iterations}\n"
                f"\tFound mutations for {tricked}/{len(malicious)} malicious samples\n"
        )
    print(message)
