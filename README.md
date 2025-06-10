# FABM workshop 2025

The software we will use for this workshop is available for Windows, Mac (Intel and Apple CPUs) and Linux.
It does not require administrator/root privileges to install.

We will work in a terminal window while installing necessary files and running the models.
On Windows, use the "Anaconda prompt" from the start menu (instructions on how to install that below).

We will be editing text files ([YAML](https://en.wikipedia.org/wiki/YAML), [Python](https://en.wikipedia.org/wiki/Python_(programming_language)), [Fortran](https://en.wikipedia.org/wiki/Fortran)) with model code and configurations. This can be done with many different editors, e.g., [Visual Studio Code](https://code.visualstudio.com/), Notepad on Windows, `vi` on Linux/Mac. We recommend using one you are already familiar with.

## Installation

### Step 1. Anaconda

Ensure you have Anaconda:
- Linux/Mac: execute `conda --version` in a terminal
- Windows: look for “Anaconda prompt” in the start menu

If you *do not* have Anaconda, [install Miniconda](https://docs.anaconda.com/miniconda/miniconda-install/).

### Step 2. Download this repository

You will need the [Git](https://en.wikipedia.org/wiki/Git) command line tool. To verify this is installed, open a terminal window (on Windows, use the "Anaconda prompt" from the start menu), type `git --version` and press Enter.
If this returns the git version, you are all set. If it returns an error such as `'git' is not recognized as an internal or external command`,
please install git first with `conda install conda-forge::git`

Now get a copy of all necessary software and setups by "cloning" the workshop repository:

```
git clone --recurse-submodules https://github.com/BoldingBruggeman/fabmws2025.git
```

This will create a new directory `fabmws2025`.
In subsequent steps we will assume you are in this directory.
When you are in a terminal window, you can enter it with `cd fabmws2025`.

### Step 3. Install software

1. Create an isolated `fabmws2025` environment with all packages for model compilaiton, analysis and visualization.
   To do this, open a terminal window (on Windows, use the "Anaconda prompt" from the start menu), ensure you are in the `fabmws2025` directory, and type:

   ```
   conda env create -f environment.yml
   ```

   If you experience any issue with the above, we recommend you first execute `conda update conda` to ensure your conda is up to date.
   Should this fail because of lack of permissions, we recommend you [install Miniconda](https://docs.anaconda.com/miniconda/miniconda-install/).
   After you have an up-to-date conda, retry the `conda env create ...` command.

2. From the terminal window and `fabmws2025` directory, compile the models and tools. On Windows, use:

   ```
   conda activate fabmws2025
   install
   ```

   And on Mac and Linux:

   ```
   conda activate fabmws2025
   ./install
   ```


### Step 4. Test your installation

Test your installation by running the following in a terminal window:
   ```
   conda activate fabmws2025
   gotm --version
   python show_versions.py
   ```
   These three commands should complete without errors.

## Observations

Observations used for calibration (parsac) or data assimilation (EAT) must be provided as a whitespace-separated tab-separated
text file. Each observed variable must use a separate file.
Each observation must be on its own line, which should contain:
* the date + time as `YYYY-mm-dd HH:MM:SS`. For instance, a value of `2000-05-08 06:20:00` for 6:20 am on 8 May 2000.
* _only if you are providing depth-dependent observations:_ the depth (m) at which the
   observation was taken. It decreases downwards from the water surface, e.g., a
   value of `-5.4` indicates a depth of 5.4 meter below the water surface.
* the observed value
* _optional:_ the standard deviation of the observation. This will be interpreted as the combination of measurement and model error.
