from src.algorithm import WOA
from src.execution_options import ExecutionOptions
from src.benchmark_function import AVAILABLE_FUNCTIONS
from src.application import Application


def run_function(path, benchmark_function):
    execution_options = ExecutionOptions(function=benchmark_function)
    execution_options.execution_params = {
        'runs_count': 10,
        'population_size': 30,
        'iterations_count': 200,
    }

    algorithm = WOA(options=execution_options)

    while not algorithm.has_finished:
        print(f"Run #{algorithm.current_iteration}, {algorithm.iterations_left} left")
        algorithm.iterate()

    print(f'Finished executing! Saving the results to {path}')
    result = algorithm.result
    result.save_json(path)


application = Application()
application.boot()


for function in AVAILABLE_FUNCTIONS:
    function_name = function.name
    file_name = function_name.lower().replace('function', '').strip()
    print(f"Running optimization for {function_name}")
    run_function(f"results/{file_name}.json", function)

