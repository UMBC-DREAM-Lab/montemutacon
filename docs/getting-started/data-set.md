---
layout: default
title: 'Data set and models'
parent: 'Getting Started'
nav_order: 2
---

# Data set

In the paper we make use of the [EMBER 2018](https://github.com/elastic/ember)
dataset. Out of the dataset, we extracted some specific features and used those
to train/mutate. For the purposes of the tutorial, we have a <a
href="{{'assets/samples.json' | absolute_url}}" target="_blank" rel="noopener
noreferrer" download>json file</a> with 100 pre-processed samples. The split of
the samples should be around 50-50.

<div class="alert alert-info">
    We only need these pre-processed samples as the pre-trained model, and the pre-existing mutations use those. Otherwise you can use whatever your model requires.
</div>

Each sample in the JSON file, looks like this:
```json
{
    "strings_entropy":6.5547189713,
    "num_strings":4029,
    "file_size":966594,
    "num_exports":0,
    "num_imports":2,
    "has_debug":"0",
    "has_signature":"0",
    "timestamp":1504401044,
    "sizeof_code":192512,
    "entry":"   ",
    "num_sections":6,
    "imported_libs":["kernel32.dll","comctl32.dll"],
    "imported_funcs":["lstrcpy","InitCommonControls"],
    "y":1 // 1 for malicious, 0 for benign
}
```

# Models

In addition to the data, we have some pre-trained <a
href="https://github.com/iboutsikas/mcts/releases/download/v1.0/models.zip"
target="_blank" rel="noopener noreferrer" download>models available</a>. In the
zip you will find 2 folders:

* **surrogate**: This is the surrogate model, a binary decision tree. We need
  this.
* **victim**: This is the victim model, an MLP. We do not need this for the
  tutorial.

If you are not sure what those mean, you can refer back to the original paper.




The tree is trained on the entirety of EMBER 2018 test set (~200,000 samples).
In the surrogate folder you will find 4 files:

* **trained_tree.dat**: The scikit-learn trained model.
* **full_pipeline_surrogate.dat**: The serialized transform pipeline for all the
  numerical features in our data set.
* **funcs_vectorizer_surrogate.dat**: The serialized vectorizer for the
  functions categorical feature in the data set.
* **libs_vectorizer_surrogate.dat**: The serialized vectorizer for the libraries
  categorical feature in the data set.

We need the pipeline and vectorizers so we can featurize the sample in format
the trained tree can understand and use. Again this is tied to the specific
model we are using, and it is a dependency of the search itself.