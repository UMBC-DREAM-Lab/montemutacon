# Evading Malware Classifiers via Monte Carlo Mutant Feature Discovery

This repository contains the code for the mutant malware feature discovery with Monte Carlo Tree Search (MCTS). 
This method is based on our [paper](https://arxiv.org/abs/2106.07860) that was presented at the [12th Annual Malware Technical Exchange Meeting
](https://www.sandia.gov/mtem/). Both MCTS and Random
Search are included in the repository; however, the repository does not contain any of the performance evaluation code used in our research.

<div align="center", style="font-size: 50px">

### [:information_source: Documentation](https://umbc-dream-lab.github.io/montemutacon/) &emsp; [:page_facing_up: Paper](https://arxiv.org/abs/2106.07860)

</div>

## Dependencies
There is an `environment.yml` included. Please note that it includes the core
dependencies only, so it can be used on any platform. It also includes a
dependency on `scikit-learn` and `tensorflow` because the models used in our research utilized these libraries.
If your models do not use that, you can safely remove the dependencies from
`environment.yml`.

The code as of now uses *MongoDB* to retrieve some pre-processed features. This
is yet another dependency that can be removed if you want to handle this
differently.

## Installing
To install all the dependancies:
```
conda env create -f environment.yml
```

## Usage
[main.py](main.py) is the entry point to the software. It will require adjustments for
your use case as it is not a standalone library right now. The code is
documented to help you figure out what's what since you are not in our heads!

## How to Cite?
If you use our software, please consider citing the original paper:
```
@article{Boutsikas2021EvadingMC,
  title={Evading Malware Classifiers via Monte Carlo Mutant Feature Discovery},
  author={John Boutsikas and M. E. Eren and Charles K. Varga and Edward Raff and Cynthia Matuszek and Charles Nicholas},
  journal={ArXiv},
  year={2021},
  volume={abs/2106.07860}
}
```

## Authors
- John Boutsikas
- [Maksim E. Eren](https://www.maksimeren.com)
- [Charles Varga](https://www.linkedin.com/in/cvar-ga/)
- [Edward Raff](https://www.edwardraff.com)
- Cynthia Matuszek
- Charles Nicholas
