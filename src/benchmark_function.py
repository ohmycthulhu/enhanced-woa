import numpy as np


def is_prime(n):
    if n % 2 == 0 and n > 2:
        return False
    for i in range(3, int(np.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


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

    # Generate random params
    def generate_random(self, count):
        bounds = [
            [self._get_lower_bound(i), self._get_upper_bound(i)] for i in range(self._dimension)
        ]

        result = []
        _rho = self._get_minimum_prime_number(count)

        for j in range(1, count + 1):
            rho = 2 * np.cos(2 * np.pi * j / _rho)
            result.append([
                bounds[i][0] + (bounds[i][1] - bounds[i][0]) * ((rho * (i + 1)) % 1)
                for i, bound in enumerate(bounds)
            ])

        return np.array(result)

    @staticmethod
    def _get_minimum_prime_number(m):
        res = 2 * m + 3
        while not is_prime(res):
            res += 2
        return res

    def _get_upper_bound(self, index):
        constraint = self._constraints[index]
        if constraint is not None and 'max' in constraint:
            return constraint['max']
        return 1e4

    def _get_lower_bound(self, index):
        constraint = self._constraints[index]
        if constraint is not None and 'min' in constraint:
            return constraint['min']
        return -1e4

    def constraint_params(self, params):
        res = params.copy()

        for i, param in enumerate(params):
            b_l, b_u = self._get_lower_bound(i), self._get_upper_bound(i)
            if param < b_l:
                res[i] = b_l
            elif param > b_u:
                res[i] = b_u

        return res

    @property
    def dimension(self):
        return self._dimension

