from src.execution_options import ExecutionOptions
from src.algorithm import WOARun
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


test_result = test()
if test_result:
    print('Tests passed successfully!')
else:
    print('Tests failed')
