# LPy training 

This project presents some examples of use of L-Py.

## Installation of the training material

In a convenient directory, you will now download the training material using the following commands.

    cd /path/to/your/documents
    git clone https://github.com/fredboudon/lpy-training.git


## Installation of L-Py using Conda


This installation is based on [Conda](https://conda.io). Conda is a package manager that can be installed on Linux, Windows, and Mac.
If you have not yet installed conda on your computer, follow these instructions:

[Conda Installation](https://conda.io/docs/user-guide/install/index.html). Follow instructions for Miniconda.

[Conda Download](https://conda.io/miniconda.html). Use the Python 3.8 based installation.

Then, after install of conda, run the following command 

    conda create -n lpy openalea.lpy notebook -c fredboudon -c conda-forge

Activate the environment using

    conda activate lpy
    
Test your installation by running

    lpy
    


