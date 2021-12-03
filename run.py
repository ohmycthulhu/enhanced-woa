from src.algorithm import WOA
from src.execution_options import ExecutionOptions
import src.functions as functions
from src.benchmark_function import BenchmarkFunction


def run_function(path, benchmark_function):
    execution_options = ExecutionOptions(function=benchmark_function)
    execution_options.execution_params = {
        'runs_count': 30,
        'population_size': 30,
        'iterations_count': 2000,
    }

    algorithm = WOA(options=execution_options)

    while not algorithm.has_finished:
        print(f"Run #{algorithm.current_iteration}, {algorithm.iterations_left} left")
        algorithm.iterate()

    print(f'Finished executing! Saving the results to {path}')
    result = algorithm.result
    result.save_json(path)


function_ackerman = BenchmarkFunction(
    hof=lambda a, b, c: lambda *xs: functions.ackley_function(a, b, c, xs),
    hyperparams=['a', 'b', 'c'],
    hyperparameter_defaults={'a': 20, 'b': 0.2, 'c': 2 * 3.1415},
    dimension=30,
    constraints=[{'min': -32.768, 'max': 32.768} for _ in range(30)],
)

function_rastrigin = BenchmarkFunction(
    hof=lambda: lambda *xs: functions.rastrigin_function(xs),
    hyperparams=[],
    hyperparameter_defaults={},
    dimension=30,
    constraints=[{'min': -5.12, 'max': 5.12} for _ in range(30)],
)

function_rosenblock = BenchmarkFunction(
    hof=lambda: lambda *xs: functions.rosenbrok_function(xs),
    hyperparams=[],
    hyperparameter_defaults={},
    dimension=30,
    constraints=[{'min': -2.048, 'max': 2.048} for _ in range(30)],
)

function_schwefel = BenchmarkFunction(
    hof=lambda: lambda *xs: functions.schwefel_function(xs),
    hyperparams=[],
    hyperparameter_defaults={},
    dimension=30,
    constraints=[{'min': -500, 'max': 500} for _ in range(30)],
)


run_function('results/ackerman.json', function_ackerman)
# run_function('results/rastrigin.json', function_rastrigin)
# run_function('results/rosenblock.json', function_rosenblock)
# run_function('results/shwefel.json', function_schwefel)
