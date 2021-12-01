from src.execution_options import ExecutionOptions
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

    # Initialization
    execution_options = ExecutionOptions(
        function=factory.get_benchmark_function()
    )

    # Hyper parameter setting
    execution_options.hyper_params = {'x': 4}
    if not test_helpers.expect_value(False, execution_options.is_valid()):
        return False

    execution_options.hyper_params = {'y': 10}
    if not test_helpers.expect_value(True, execution_options.is_valid()):
        return False

    execution_options.hyper_params = {'x': 20, 'y': 10}
    if not test_helpers.expect_value(True, execution_options.is_valid()):
        return False

    # Execution parameters setting
    if not test_helpers.expect_value(0, execution_options.evaluation_count):
        return False

    if not test_helpers.expect_value(
        2050,
        execution_options.evaluate(5)
    ):
        return False

    if not test_helpers.expect_value(1, execution_options.evaluation_count):
        return False

    return True


test_result = test()
if test_result:
    print('Tests passed successfully!')
else:
    print('Tests failed')
