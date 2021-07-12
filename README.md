# Evading Malware Classifiers via Monte Carlo Mutant Feature Discovery

This repository contains the code for the mutation search. Both MCTS and Random
Search are included here. It does not contain any of the evaluation code. More
details can be found in the paper
[https://arxiv.org/abs/2106.07860](https://arxiv.org/abs/2106.07860).

## Dependancies
There is an `environment.yml` included. Please note that it includes the core
dependancies only, so it can be used on any platform. It also includes a
dependancy on `scikit-learn` and `tensorflow` because our models required that.
If your models do not use that, you can safely remove the dependacies from
`environment.yml`.

The code as of now, uses mongo db to retrieve some pre-processed features. This
is yet another dependacy that can be removed if you want to handle this
differently.

## Installing
To install all the dependancies

```
conda env create -f environment.yml
```

## Usage
main.py is the entry point to the whole thing. It will require adjustments for
your own use-case as it is not a standalone library right now. The code is
documented to help you figure out what's what, since you are not in our heads!
