Reconstructing Market Indices
======================


## About this project

1. Problem Definition – This project focused on reconstructing financial indices, particularly the CRSP market return indices and the S&P 500 index, to enhance understanding of index construction and investment benchmarking. The goal was to approximate these indices using historical market data and assess the accuracy of the approximations compared to official indices. This problem is significant because market indices serve as benchmarks for portfolio performance, investment decision-making, and financial research.

2. Data Acquisition and Preparation – The data was sourced from the CRSP database, which includes monthly stock-level price, return, and shares outstanding data, as well as historical index information. The data was preprocessed by filtering for relevant securities, handling missing values, and computing adjusted market capitalizations to account for corporate actions such as stock splits. Additionally, constituent membership data was merged to track historical changes in index composition.

3. Modeling and Methodology – Two methodologies were implemented for index reconstruction: (a) a direct market capitalization sum approach and (b) a portfolio simulation with quarterly rebalancing. The first method approximated the index level by summing the market capitalization of all constituents, while the second method simulated a tradable portfolio that rebalances based on the index's weightings. The second method more accurately reflected the real-world trading dynamics of the S&P 500.

4. Evaluation – The reconstructed indices were evaluated by comparing return correlations and cumulative return differences with official indices. The portfolio rebalancing method demonstrated a near-perfect correlation (0.999) with the actual S&P 500 returns, significantly outperforming the market capitalization sum method. These findings emphasized the importance of proper rebalancing when modeling market indices.

5. Iteration and Learning – Challenges included imperfect data matches due to missing proprietary index criteria and the need to adjust methodologies for corporate actions. By iterating through different weighting strategies and refining data handling techniques, the project improved its accuracy in approximating index returns. These iterations reinforced the importance of understanding both theoretical index construction and practical financial data limitations.

6. Insights and Future Improvements – Improvements on this project could explore alternative weighting strategies like equal-weight and fundamentally weighted indices to enhance diversification and better reflect intrinsic company value. Additionally, advancements in real-time tracking, such as optimized Sequential Monte Carlo methods and reinforcement learning approaches, can improve index tracking accuracy while minimizing transaction costs.

## Quick Start

This project requires `conda`  or `mamba`, via [miniforge]
(https://github.com/conda-forge/miniforge) and [TexLive](https://tug.org/texlive/windows.html#install).
Open a terminal, navigate to the root directory of the project, and create a 
conda environment using the following command:
```
conda create -n blank python=3.12
conda activate blank
```
and then install the dependencies with pip
```
pip install -r requirements.txt
```
Finally, run
```
doit
```

If you would also like to run the R code included in this project, you can either install
R and the required packages manually, or you can use the included `environment.yml` file.
To do this, run
```
mamba env create -f environment.yml
```
I'm using `mamba` here because `conda` is too slow. Activate the environment. 
Then, make sure to uncomment
out the RMarkdown task from the `dodo.py` file. Then,
run `doit` as before.

### Other commands

#### Unit Tests and Doc Tests

You can run the unit test, including doctests, with the following command:
```
pytest --doctest-modules
```
You can build the documentation with:
```
rm ./src/.pytest_cache/README.md 
jupyter-book build -W ./
```
Use `del` instead of rm on Windows

#### Setting Environment Variables

You can 
[export your environment variables](https://stackoverflow.com/questions/43267413/how-to-set-environment-variables-from-env-file) 
from your `.env` files like so, if you wish. This can be done easily in a Linux or Mac terminal with the following command:
```
set -a ## automatically export all variables
source .env
set +a
```
In Windows, this can be done with the included `set_env.bat` file,
```
set_env.bat
```

### General Directory Structure

 - The `assets` folder is used for things like hand-drawn figures or other
   pictures that were not generated from code. These things cannot be easily
   recreated if they are deleted.

 - The `_output` folder, on the other hand, contains dataframes and figures that are
   generated from code. The entire folder should be able to be deleted, because
   the code can be run again, which would again generate all of the contents.

 - The `data_manual` is for data that cannot be easily recreated. This data
   should be version controlled. Anything in the `_data` folder or in
   the `_output` folder should be able to be recreated by running the code
   and can safely be deleted.

 - I'm using the `doit` Python module as a task runner. It works like `make` and
   the associated `Makefile`s. To rerun the code, install `doit`
   (https://pydoit.org/) and execute the command `doit` from the `src`
   directory. Note that doit is very flexible and can be used to run code
   commands from the command prompt, thus making it suitable for projects that
   use scripts written in multiple different programming languages.

 - I'm using the `.env` file as a container for absolute paths that are private
   to each collaborator in the project. You can also use it for private
   credentials, if needed. It should not be tracked in Git.

### Data and Output Storage

I'll often use a separate folder for storing data. Any data in the data folder
can be deleted and recreated by rerunning the PyDoit command (the pulls are in
the dodo.py file). Any data that cannot be automatically recreated should be
stored in the "data_manual" folder. Because of the risk of manually-created data
getting changed or lost, I prefer to keep it under version control if I can.
Thus, data in the "_data" folder is excluded from Git (see the .gitignore file),
while the "data_manual" folder is tracked by Git.

Output is stored in the "_output" directory. This includes dataframes, charts, and
rendered notebooks. When the output is small enough, I'll keep this under
version control. I like this because I can keep track of how dataframes change as my
analysis progresses, for example.

### Naming Conventions

 - **`pull_` vs `load_`**: Files or functions that pull data from an external
 data source are prepended with "pull_", as in "pull_fred.py". Functions that
 load data that has been cached in the "_data" folder are prepended with "load_".
 For example, inside of the `pull_CRSP_Compustat.py` file there is both a
 `pull_compustat` function and a `load_compustat` function. The first pulls from
 the web, whereas the other loads cached data from the "_data" directory.


### Dependencies and Virtual Environments

#### Working with `pip` requirements

`conda` allows for a lot of flexibility, but can often be slow. `pip`, however, is fast for what it does.  You can install the requirements for this project using the `requirements.txt` file specified here. Do this with the following command:
```
pip install -r requirements.txt
```

The requirements file can be created like this:
```
pip list --format=freeze
```

#### Working with `conda` environments

The dependencies used in this environment (along with many other environments commonly used in data science) are stored in the conda environment called `blank` which is saved in the file called `environment.yml`. To create the environment from the file (as a prerequisite to loading the environment), use the following command:

```
conda env create -f environment.yml
```

Now, to load the environment, use

```
conda activate blank
```

Note that an environment file can be created with the following command:

```
conda env export > environment.yml
```

However, it's often preferable to create an environment file manually, as was done with the file in this project.

Also, these dependencies are also saved in `requirements.txt` for those that would rather use pip. Also, GitHub actions work better with pip, so it's nice to also have the dependencies listed here. This file is created with the following command:

```
pip freeze > requirements.txt
```

**Other helpful `conda` commands**

- Create conda environment from file: `conda env create -f environment.yml`
- Activate environment for this project: `conda activate blank`
- Remove conda environment: `conda remove --name blank --all`
- Create blank conda environment: `conda create --name myenv --no-default-packages`
- Create blank conda environment with different version of Python: `conda create --name myenv --no-default-packages python` Note that the addition of "python" will install the most up-to-date version of Python. Without this, it may use the system version of Python, which will likely have some packages installed already.

#### `mamba` and `conda` performance issues

Since `conda` has so many performance issues, it's recommended to use `mamba` instead. I recommend installing the `miniforge` distribution. See here: https://github.com/conda-forge/miniforge

