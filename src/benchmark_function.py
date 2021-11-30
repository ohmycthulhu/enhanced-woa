import numpy as np


class BenchmarkFunction:
    def __init__(self, hof, hyperparams, hyperparameter_defaults, dimension, constraints):
        self.hof = hof
        self.hyperparams_list = hyperparams
        self.hyperparams_defaults = hyperparameter_defaults
        self.dimension = dimension
        self.constraints = constraints
        self.func = None

    def set_hyperparams(self, params):
        hyperparams = self._hyperparams_with_defaults(params)
        self._validate(hyperparams)
        self.func = self.hof(*hyperparams.values())

    def evaluate(self, *values):
        if self.func is None:
            raise NotImplementedError("Evaluation is used before setting hyperparameters")
        if len(values) < self.dimension:
            raise AttributeError("Values count mismatch dimensions of evaluating function")
        if not self._values_in_constraints(values):
            return np.inf
        return self.func(*values)

    def _hyperparams_with_defaults(self, params):
        result = params.copy()

        for param_name in self.hyperparams_list:
            if param_name not in result and param_name in self.hyperparams_defaults:
                result[param_name] = self.hyperparams_defaults[param_name]

        return result

    def _validate(self, params):
        for param_name in self.hyperparams_list:
            if param_name not in params or params[param_name] is None:
                return False
        return True

    def _values_in_constraints(self, values):
        for constraint, value in zip(self.constraints, values):
            if not constraint:
                continue
            if 'min' in constraint and constraint['min'] > value:
                return False
            if 'max' in constraint and constraint['max'] < value:
                return False

        return True
