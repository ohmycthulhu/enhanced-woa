# Class for managing execution options
# Contains BenchmarkFunction as `function` argument and provides default values for every option
# It has these purposes:
# - Allows getting / setting default parameters alongside with validation
# - Provides the bridge for interacting with BenchmarkFunction
# - Counts the number of function evaluation
class ExecutionOptions:
    DEFAULT_OPTIONS = {
        'iterations_count': 200,
        'population_size': 30,
        'runs_count': 10,
    }

    def __init__(self, function):
        self._function = function
        self._execution_params = ExecutionOptions.DEFAULT_OPTIONS.copy()
        self._evaluation_count = 0

    def is_valid(self):
        return self._function.is_valid()

    @staticmethod
    def validate_execution_param(name, value):
        return value > 0

    @property
    def hyper_params(self):
        return self._function.hyperparams

    @hyper_params.setter
    def hyper_params(self, params):
        try:
            self._function.hyperparams = params
        except AttributeError:
            pass

    @property
    def execution_params(self):
        return self._execution_params

    @property
    def dimension(self):
        return self._function.dimension

    @execution_params.setter
    def execution_params(self, params):
        self._execution_params = {**self._execution_params, **params}

    def evaluate(self, *values):
        # Evaluation may throw an error, so we increase evaluation count after ensuring there is no error
        result = self._function.evaluate(*values)
        self._evaluation_count += 1
        return result

    @property
    def function_name(self):
        return self._function.name

    @property
    def evaluation_count(self):
        return self._evaluation_count

    def reset_evaluation_counter(self):
        self._evaluation_count = 0

    def generate_params(self, count):
        return self._function.generate_random(count)

    def constraint_params(self, params):
        return self._function.constraint_params(params)
