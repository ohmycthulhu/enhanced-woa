# Enhanced Whale Optimization Algorithm

The repository contains the implementation for Enhanced Whale Optimization algorithm, discussed in
**Joint Compressed Sensing and  Enhanced Whale Optimization Algorithm 
for Pilot Allocation in Underwater Acoustic OFDM Systems**(RONGKUN JIANG 1 , XUETIAN WANG 1 , SHAN CAO 2 , JIAFEI ZHAO 1 , and XIAORAN LI 1, 2018).

The code uses Python3, `matplotlib`, `numpy` and virtual python environment for package management.

## Table of content
- [How to run the code](how-to-run-the-code)
- [Running user interface](running-user-interface)
- [Running all functions](running-all-functions)
- [Visualizing the evaluation](visualizing-the-evaluation)
- [Structure of the project](structure-of-the-project)


## How to run the code
The repository contains three ways of running the program:
- Running user interface
- Running all functions
- Visualizing the progress of the single run


## Running user interface
To run the user interface, you should run `main.py` file in terminal.
It will launch the whole program and will let you choose the function, evaluation parameters,
hyperparameters, and interactively explore the results. The results of the evaluation is stored in 
'results/result.json' file.

## Running all functions
To run all available functions with default parameters, you can run `run.py`.
It will optimize every function and store the results in 'results' folder in '{function_name}.json'
file. It will contain all needed information, but the results won't be displayed by the program itself.


## Visualizing the evaluation
There is a way for running visualizing of the algorithm works. The `visualize.py`
will run the optimization on 2D Rastrigin function and plot the position of the agents
for each iteration, including the initialization itself. The images will be stores in 
'plots' folder.

## Structure of the project
The source code of the project in located in 'src' folder. It's logically divided in
'algorithms' and 'user interface' parts. Everything related to the user interface, 
located in 'src/ui' folder. It includes manager for input, for text and internalization,
the screens and user interface manager.
Anything located not in the 'src/ui', serves the purpose other than user interface. It contains
the classes for algorithm evaluation, holding the algorithm results, benchmark functions, and `Application` class.

The repository also contains the tests for several essential classes.
They're located in 'test' folder and contains 3 tests `algorithm_test.py`, `benchmark_function_test.py`,
`execution_options_test.py`. To run the test, you may use:
```PYTHONPATH=`pwd` venv/bin/python3 test/algorithm_test.py```

