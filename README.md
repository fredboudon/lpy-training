# LPy training 

This project presents some examples of use of L-Py.

## Installation of the training material

In a convenient directory, you will now download the training material using the following commands.

    cd /path/to/your/documents
    git clone https://github.com/fredboudon/lpy-training.git
    git checkout imagina2019


## Installation of L-Py

###  Bundle Installation for Linux and Windows

Download the bundle for Ubuntu
```bash
wget https://gforge.inria.fr/frs/download.php/file/38215/lpy-ubuntu64.tar.gz
```
It should be working for compatible linux distributions.

For windows, the following archive is accessible
```bash
wget https://gforge.inria.fr/frs/download.php/file/38214/lpy-win64.tar.gz
```

Unpack and install the bundle.
```bash
# Unpack environment into directory `lpy`
mkdir -p lpy
tar -xzf lpy-XXX.tar.gz -C lpy

# Activate the environment. This adds `lpy/bin` to your path
source lpy/bin/activate

# Cleanup prefixes from in the active environment.
# Note that this command can also be run without activating the environment
# as long as some version of python is already installed on the machine.
conda-unpack

# At this point the environment is exactly as if you installed it here
# using conda directly. All scripts should work fine.
lpy

# Deactivate the environment to remove it from your path
source lpy/bin/deactivate
```


### Conda Installation for Mac

This installation is based on [Conda](https://conda.io). Conda is a package manager that can be installed on Linux, Windows, and Mac.
If you have not yet installed conda on your computer, follow these instructions:

[Conda Installation](https://conda.io/docs/user-guide/install/index.html). Follow instructions for Miniconda.

[Conda Download](https://conda.io/miniconda.html). Use the Python 2.7 based installation.

To install L-Py, you need to copy the file [macenv.txt](https://gist.github.com/fredboudon/e1b6a7933d26c7335b87cb8b0234df45) containing the specification of an environment containing L-Py onto your computer. For this, use this command in a shell:
    
    wget https://gist.github.com/fredboudon/e1b6a7933d26c7335b87cb8b0234df45/raw/3b53fd413d4284b701b9fd89f641b4fa3e4d66b6/macenv.txt

If it fails copy the content in a file macenv.txt.

Then, after install of conda, run the following command 

    conda create -n lpy --file macenv.txt

Activate the environment using

    conda activate lpy
    
Test your installation by running

    lpy
    


