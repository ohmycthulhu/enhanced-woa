from src.execution_options import ExecutionOptions
from src.algorithm import WOARun
import test_helpers
import factory


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

    algorithm_run = WOARun(options=execution_options)

    # Hyper parameter setting
    if test_helpers.expect_no_error(
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

    return True


test_result = test()
if test_result:
    print('Tests passed successfully!')
else:
    print('Tests failed')
