# LPy training 

This project presents some examples of use of L-Py.

## Installation of the training material

To access git material, install first [Github Desktop](https://desktop.github.com/)

In a convenient directory, you will now download the training material using the following commands.

    cd /path/to/your/documents
    git clone https://github.com/fredboudon/lpy-training.git

or directly by using Github Desktop.

## Installation of L-Py using Conda


This installation is based on [Conda](https://conda.io). Conda is a package manager that can be installed on Linux, Windows, and Mac.
If you have not yet installed conda on your computer, follow these instructions:

[Conda Installation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). Follow instructions for Miniconda.

[Conda Download](https://conda.io/miniconda.html). Use the Python 3.8 based installation.

Then, after install of conda, run the following command to create an environment with openalea.lpy and its notebooks extension.

    conda env create -f environment.yml

Activate the environment using

    conda activate lpytraining

Test your installation by running

    lpy

Test notebooks by running

    jupyter notebook examples/L-systems-Topo-Turtle.ipynb

    
## Documentation on the tools

[L-Py Documentation](https://lpy.readthedocs.io/en/latest/)

[L-Py notebook integration documentation](https://github.com/jvail/plantgl-jupyter)

## Online access to the exercices

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fredboudon/lpy-training.git/imagina2021?filepath=examples)
[![NBViewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.jupyter.org/github/fredboudon/lpy-training/blob/imagina2021/examples/L-systems-Topo-Turtle.ipynb)
[![NBViewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.jupyter.org/github/fredboudon/lpy-training/blob/imagina2021/examples/L-systems-Rewritting.ipynb)
[![NBViewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.jupyter.org/github/fredboudon/lpy-training/blob/imagina2021/examples/Lsystems-InformationTransfert.ipynb)
