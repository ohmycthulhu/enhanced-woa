from src.benchmark_function import BenchmarkFunction
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
    func1 = factory.get_benchmark_function()

    # Hyper parameters test
    try:
        func1.hyperparams = ({'x': 10})
        print('Hyper parameter validation failed')
        return False
    except AttributeError:
        print('Hyper parameter validation works')

    try:
        func1.hyperparams = {'y': 10}
        print('Hyper parameter defaults work')
    except AttributeError as e:
        print('Hyper parameter defaults do not work')
        return False

    try:
        func1.hyperparams = {'x': 10, 'y': 20}
        print('Hyper parameter defaults work')
    except AttributeError:
        print('Hyper parameter defaults do not work')
        return False

    # Evaluation test
    # Call with no parameters
    if not test_helpers.expect_error(
            lambda: func1.evaluate(),
            'Evaluation validation failed',
            'Evaluation validation works'
    ):
        return False

    # Call with correct parameter
    if not test_helpers.expect_value(120, func1.evaluate(1)):
        return False

    if not test_helpers.expect_different(2400, func1.evaluate(20)):
        return False

    if not test_helpers.expect_different(-2400, func1.evaluate(-20)):
        return False

    return True


test_result = test()
if test_result:
    print('Tests passed successfully!')
else:
    print('Tests failed')
