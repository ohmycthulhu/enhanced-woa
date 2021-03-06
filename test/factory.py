from src.benchmark_function import BenchmarkFunction
from src.functions import ackley_function
import numpy as np


def get_benchmark_function():
    hyperparameters = ['x', 'y']
    defaults = {'x': 0}
    dimension = 1
    value_constraints = [
        {'min': -10, 'max': 10}
    ]

    return BenchmarkFunction(
        name='factory_func_1',
        hof=lambda x, y: lambda z: z * (x ** 2 + y),
        hyperparams=hyperparameters,
        hyperparameter_defaults=defaults,
        dimension=dimension,
        constraints=value_constraints
    )


def get_minimization_function():
    hyperparameters = ['a', 'b', 'c']
    defaults = {'a': 10, 'b': 0.2, 'c': 2 * np.pi}
    dimension = 2
    value_constraints = [
        {'min': -32.76, 'max': 32.76},
        {'min': -32.76, 'max': 32.76},
    ]
    return BenchmarkFunction(
        name='ackley_test',
        hof=lambda a, b, c: lambda *xs: ackley_function(a, b, c, xs),
        hyperparams=hyperparameters,
        hyperparameter_defaults=defaults,
        dimension=dimension,
        constraints=value_constraints
    )

