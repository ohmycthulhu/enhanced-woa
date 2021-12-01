# Class for managing execution options
class ExecutionOptions:
    DEFAULT_OPTIONS = {
        'iterations_count': 0,
    }

    def __init__(self, function):
        self._function = function
        self._execution_params = ExecutionOptions.DEFAULT_OPTIONS.copy()
        self._evaluation_count = 0

    def is_valid(self):
        return self._function.is_valid()

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
        return self.execution_params

    @execution_params.setter
    def execution_params(self, params):
        self._execution_params = params

    def evaluate(self, *values):
        # Evaluation may throw an error, so we increase evaluation count after ensuring there is no error
        result = self._function.evaluate(*values)
        self._evaluation_count += 1
        return result

    @property
    def evaluation_count(self):
        return self._evaluation_count

    def reset_evaluation_counter(self):
        self._evaluation_count = 0
