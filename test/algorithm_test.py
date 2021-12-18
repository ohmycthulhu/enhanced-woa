from src.execution_options import ExecutionOptions
from src.algorithm import WOARun, WOA
from src.application import Application
import test_helpers
import factory
import json


def test():
    # Test steps:
    # 1. Initialize class instance
    # 2. Test setting hyper parameters
    # 3. Test evaluation

    # Each test consists of these steps;
    # 1. Test validation
    # 2. Test defaults
    # 3. Test evaluation

    # Initialization execution option
    execution_options = ExecutionOptions(function=factory.get_minimization_function())

    execution_options.execution_params = {'iterations_count': 200}

    algorithm_run = WOARun(options=execution_options)

    # Hyper parameter setting
    if not test_helpers.expect_no_error(
        lambda: algorithm_run.run(),
        'Algorithm run failed',
        'Algorithm run works',
    ):
        return False

    result = algorithm_run.result

    if not test_helpers.expect_not_none(result):
        return False

    if not test_helpers.expect_not_none(result.best_value):
        return False

    if not test_helpers.expect_not_none(result.best_params):
        return False

    if not test_helpers.expect_not_none(result.execution_time):
        return False

    print("Best found parameters", result.best_value, result.best_params, result.evaluation_count)

    with open('whales.json', 'w') as file:
        json.dump(algorithm_run.history, file)

    return True


def complete_algorithm_run_test():
    runs_count = 10
    execution_options = ExecutionOptions(function=factory.get_minimization_function())

    execution_options.execution_params = {'iterations_count': 200, 'runs_count': runs_count}

    algorithm = WOA(options=execution_options)

    if not test_helpers.expect_value(False, algorithm.has_started):
        return False

    algorithm.iterate()

    if not test_helpers.expect_value(True, algorithm.has_started):
        return False

    if not test_helpers.expect_value(1, algorithm.current_iteration):
        return False

    if not test_helpers.expect_value(runs_count - 1, algorithm.iterations_left):
        return False

    for i in range(runs_count - 1):
        algorithm.iterate()

    if not test_helpers.expect_value(runs_count, algorithm.current_iteration):
        return False

    if not test_helpers.expect_value(0, algorithm.iterations_left):
        return False

    if not test_helpers.expect_no_error(
        lambda: algorithm.iterate(),
        'Algorithm run after finishing raises error',
        'Algorithm run after finishing works well',
    ):
        return False

    result = algorithm.result

    if not test_helpers.expect_not_none(result):
        return False

    if not test_helpers.expect_value(runs_count, result.length):
        return False

    file_path = 'woa.json'
    result.save_json(file_path)
    if not test_helpers.expect_file_exists(file_path, False):
        return False

    return True


Application().boot()
test_result = test()
if test_result:
    print('Algorithm test passed successfully!')
else:
    print('Algorithm test failed')
    exit(1)

test_result = complete_algorithm_run_test()
if test_result:
    print('Algorithm multiple run test passed successfully!')
else:
    print('Algorithm multiple run test failed')
    exit(1)




