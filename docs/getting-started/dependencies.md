---
layout: default
title: 'Pre-requisites'
parent: 'Getting Started'
nav_order: 1
---

### Dependencies
You can grab the code from
[GitHub](https://github.com/iboutsikas/mcts/tree/main). This includes all the
core dependencies that are required for the algorithm(s) to work.
You can make a new conda environment with everything required with:

```
conda env create -f environment.yml
```

This will create an environment called mml (You can edit environment.yml to
change that name).

Then change to that environment with (remember to change the name if you modified
`environment.yml`):
```
conda activate mml
```

### Additional dependencies
For the getting started tutorial you will also need
[scikit-learn](https://scikit-learn.org/stable/), as we will be using a
pre-trained model. You can install it with `conda install scikit-learn=0.23.2`.

<div class="alert alert-warning">
    The pre-trained model needs that specific version. Once you are done with the tutorial you can use whatever library and version you want for your models.
</div>