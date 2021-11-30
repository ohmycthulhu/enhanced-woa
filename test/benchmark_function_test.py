from src.benchmark_function import BenchmarkFunction
import test_helpers


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
    hyperparameters = ['x', 'y', 'z']
    defaults = {'x': 0}
    dimension = 1
    value_constraints = [
        {'min': -10, 'max': 10}
    ]

    func1 = BenchmarkFunction(
        hof=lambda x, y: lambda z: z * (x ** 2 + y),
        hyperparams=hyperparameters,
        hyperparameter_defaults=defaults,
        dimension=dimension,
        constraints=value_constraints
    )

    # Hyper parameters test
    if not test_helpers.expect_error(
            lambda: func1.set_hyperparams({'x': 10}),
            'Hyper parameter validation failed',
            'Hyper parameter validation works'
    ):
        return False

    if not test_helpers.expect_no_error(
            lambda: func1.set_hyperparams({'y': 10}),
            'Hyper parameter defaults do not work',
            'Hyper parameter defaults work'
    ):
        return False

    if not test_helpers.expect_no_error(
            lambda: func1.set_hyperparams({'x': 10, 'y': 20}),
            'Hyper parameter defaults do not work',
            'Hyper parameter defaults work'
    ):
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
