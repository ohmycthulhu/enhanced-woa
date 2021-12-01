import numpy as np


class BenchmarkFunction:
    def __init__(self, hof, hyperparams, hyperparameter_defaults, dimension, constraints):
        self._hof = hof
        self._hyperparams_list = hyperparams
        self._hyperparams_defaults = hyperparameter_defaults
        self._dimension = dimension
        self._constraints = constraints
        self._hyperparams = self._hyperparams_defaults.copy()
        self._func = None

    @property
    def all_hyperparams(self):
        return self._hyperparams_list

    @property
    def hyperparams(self):
        return self._hyperparams_with_defaults(self._hyperparams)

    @hyperparams.setter
    def hyperparams(self, params):
        hyperparams = self._hyperparams_with_defaults(params)

        if not self._validate(hyperparams):
            raise AttributeError("Not all hyperparamaters are filled")

        self._hyperparams = hyperparams

    def evaluate(self, *values):
        # The evaluating process requires several steps:
        # - to hyperparameters be set before
        # - to values to be not less than dimension of function
        # - to values to be in constrainted space
        if not self.is_valid():
            raise NotImplementedError("Evaluation is used before setting hyperparameters")
        if len(values) < self._dimension:
            raise AttributeError("Values count mismatch dimensions of evaluating function")
        if not self._values_in_constraints(values):
            return np.inf
        if self._func is None:
            self._func = self._hof(*self.hyperparams.values())
        return self._func(*values)

    # Checks if current hyperparameters are valid
    def is_valid(self):
        return self._validate(self._hyperparams)

    def _hyperparams_with_defaults(self, params):
        # Merge dictionary of default params with actual params
        if params is None:
            return self._hyperparams_defaults
        return {**self._hyperparams_defaults, **params}

    # Function for checking hyperparameters
    # params should be already merged with default values
    def _validate(self, params):
        for param_name in self._hyperparams_list:
            if param_name not in params or params[param_name] is None:
                return False
        return True

    # Check if every value is inside constraints
    # Constraints may be None (if no constraint), contain either min, max, or both
    def _values_in_constraints(self, values):
        for constraint, value in zip(self._constraints, values):
            if not constraint:
                continue
            if 'min' in constraint and constraint['min'] > value:
                return False
            if 'max' in constraint and constraint['max'] < value:
                return False

        return True
