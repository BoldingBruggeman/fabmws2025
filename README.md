# FABM workshop 2025

The software we will use for this workshop is available for Windows, Mac (Intel and Apple CPUs) and Linux.
It does not require administrator/root privileges to install.

We will work in a terminal window while installing necessary files and running the models.
On Windows, use the "Anaconda prompt" from the start menu (instructions on how to install that below).

We will be editing text files (yaml files and Python scripts) with model configurations. This can be done with many different editors, e.g., [Visual Studio Code](https://code.visualstudio.com/), Notepad on Windows, `vi` on Linux/Mac. We recommend using one you are already familiar with.

## Installation

### Step 1. Anaconda

Ensure you have Anaconda:
- Linux/Mac: execute `conda --version` in a terminal
- Windows: look for “Anaconda prompt” in the start menu

If you *do not* have Anaconda, [install Miniconda](https://docs.anaconda.com/miniconda/miniconda-install/).

### Step 2. Install software

1. Create an isolated `fabmws2025` environment with the model and visualization tools.
   To do this, open a terminal window (on Windows, use the "Anaconda prompt" from the start menu) and type:
   ```
   conda env create -f environment.yml
   ```

   If you experience any issue with the above, we recommend you first execute `conda update conda` to ensure your conda is up to date.
   Should this fail because of lack of permissions, we recommend you [install Miniconda](https://docs.anaconda.com/miniconda/miniconda-install/).
   After you have an up-to-date conda, retry the `conda create ...` command.

   The above command installs pre-compiled versions of [GOTM](https://gotm.net), [pyfabm](https://fabm.net/python), [pygetm](https://github.com/BoldingBruggeman/getm-rewrite), [fabmos](https://github.com/BoldingBruggeman/fabmos) and [parsac](https://github.com/BoldingBruggeman/parsac). They include reference versions of the biogeochemical models [ERSEM](https://github.com/pmlmodelling/ersem), [ECOSMO](https://doi.org/10.5194/gmd-15-3901-2022), [PISCES](https://www.pisces-community.org/), [iHAMOCC](https://doi.org/10.5194/gmd-13-2393-2020), [ERGOM](https://ergom.net/), and [MOPS](https://doi.org/10.5194/gmd-8-2929-2015), among others.

2. Test your installation by running the following in a terminal window:
   ```
   conda activate fabmws2025
   gotm --version
   python show_versions.py
   ```
   These three commands should complete without errors.
