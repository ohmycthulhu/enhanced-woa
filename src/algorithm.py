import numpy as np
import random
import time
from src.results import WOAResult, RunResult

SWITCH_STATE = np.random.random()


# Fuch function for chaotic switching
def random_switch():
    global SWITCH_STATE
    SWITCH_STATE = np.cos(1 / SWITCH_STATE ** 2)
    return SWITCH_STATE


# Class for managing multiple runs of Whale Optimization Algorithm
# It is responsible for:
# - holding the results of all runs
# - iteratively run algorithm, append the result to the all results
# - provide information about how many runs have been and how many left to do
class WOA:
    def __init__(self, options):
        self._options = options
        self._runs_count = options.execution_params['runs_count']
        self._current_run = 0
        self._result = None

    def iterate(self):
        if self._current_run >= self._runs_count:
            return

        run = WOARun(options=self._options)
        result = run.run()
        self._append_result(result)
        self._current_run += 1

        return self

    def _append_result(self, result):
        if self._result is None:
            self._result = WOAResult(function_name=self._options.function_name)

        self._result.append(result)

    @property
    def current_iteration(self):
        return self._current_run

    @property
    def iterations_left(self):
        return self._runs_count - self._current_run

    @property
    def has_started(self):
        return self._current_run > 0

    @property
    def has_finished(self):
        return self._current_run >= self._runs_count

    @property
    def result(self):
        return self._result


# Class for running the single run of Whale Optimization Algorithm
# It is responsible for:
# - Initializing the agents
# - Running provided amount of iterations
# - Holding the best found results
# - Providing the found results
# - Holding the history of agents over the iterations
class WOARun:
    def __init__(self, options):
        self._options = options
        self._result = None
        self._population_size = options.execution_params['population_size']
        self._iterations_count = options.execution_params['iterations_count']
        self._dimension = options.dimension
        self._history = []

    @property
    def result(self):
        return self._result

    def run(self):
        # The steps of algorithm:
        # - reset all counters, best values, and evaluation counters
        # - initialize the agents
        # - iterations time:
        #   - perform iteration
        #   - save the iteration information in history
        # - save and return the results
        start_time = time.time()
        self._options.reset_evaluation_counter()
        best_value, best_params = np.inf, []

        whales = self._initialize()
        self._add_to_history('Initialize', whales)

        for i in range(self._iterations_count):
            t = self._calculate_control_parameter(i)
            self._perform_iteration(t, whales)
            best_value, best_params = self._get_best_values(whales, best_value, best_params)
            self._add_to_history(f"Iteration #{i}", whales)

        execution_time = time.time() - start_time

        self._result = RunResult(
            best_value=best_value,
            best_params=best_params,
            execution_time=execution_time,
            evaluation_count=self._options.evaluation_count,
        )

        return self._result

    def _initialize(self):
        # Generate params by GPS provided by BenchmarkFunction
        params_list = self._options.generate_params(self._population_size)

        # Map each params set into agent
        return [
            Whale(
                params=params,
                eval_function=self._options.evaluate,
                constraint_params=self._options.constraint_params,
                dimension=self._dimension,
            )
            for params in params_list
        ]

    @staticmethod
    def _get_best_values(whales, current_best_value, current_best_params):
        best_whale = WOARun._get_best_whale(whales)

        if best_whale.fitness < current_best_value:
            return best_whale.fitness, best_whale.params
        else:
            return current_best_value, current_best_params

    @staticmethod
    def _get_best_whale(whales):
        best_value, best_whale = np.inf, None

        for whale in whales:
            if whale.fitness < best_value:
                best_value, best_whale = whale.fitness, whale

        return best_whale

    def _perform_iteration(self, control_param, whales):
        best_whale = WOARun._get_best_whale(whales)

        for whale in whales:
            if random_switch() < 0.5:
                A = 2 * control_param * self._get_r() - control_param

                if np.linalg.norm(A) < 1.0:
                    whale.encircle_prey(best_whale, A)
                else:
                    whale.search_prey(WOARun._get_random_whale(whales, whale), A)
            else:
                whale.bubble_net_attack(best_whale)

        return whales

    def _add_to_history(self, _id, whales):
        best_whale = self._get_best_whale(whales)
        self._history.append({
            'id': _id,
            'population': [{'value': w.fitness, 'params': [p for p in w.params]} for w in whales],
            'best': {'value': best_whale.fitness, 'params': [p for p in best_whale.params]},
        })

    @property
    def history(self):
        return self._history

    def _calculate_control_parameter(self, iteration):
        return 2 * (1 - np.tanh(3 * iteration / self._iterations_count))

    def _get_r(self):
        return np.random.uniform(0.0, 1.0, size=self._dimension)

    @staticmethod
    def _get_random_whale(whales, current_whale):
        if len(whales) < 2:
            return current_whale

        [random_whale] = random.sample(whales, 1)
        while random_whale == current_whale:
            [random_whale] = random.sample(whales, 1)
        return random_whale


# Single agent in Whale Optimization Algorithm
# Implements methods for movement types:
# - Bubble-net attack
# - Encircling prey
# - Search for prey
# Contains fitness parameter that is automatically calculated by the ExecutionOptions
# Also, contains ID for checking equality between the two whales
class Whale:
    ID = 1
    b = 0.5

    def __init__(self, params, eval_function, constraint_params, dimension):
        self._params = params
        self._func = eval_function
        self._constraint_params = constraint_params
        self._fitness = np.inf
        self._dimension = dimension
        self._calculate_fitness()
        self._id = Whale.ID
        Whale.ID += 1

    def bubble_net_attack(self, prey):
        D = self._get_D(prey)
        L = np.random.uniform(-1.0, 1.0, size=self._dimension)

        p1 = np.multiply(D, np.exp(self.b * L))

        p2 = np.multiply(p1, np.cos(2 * np.pi * L))
        res = self._params + p2
        return self._set_params(res)

    def encircle_prey(self, prey, A):
        C = self._get_c()
        D = self._get_D(prey, C)
        res = prey.params - np.multiply(A, D)
        return self._set_params(res)

    def search_prey(self, random_whale, A):
        C = self._get_c()
        D = self._get_D(random_whale, C)
        res = random_whale.params - np.multiply(A, D)
        return self._set_params(res)

    def _get_c(self):
        return 2.0 * np.random.uniform(0.0, 1.0, size=self._dimension)

    def _get_D(self, other_whale, C=1):
        return np.linalg.norm(np.multiply(C, other_whale.params) - self._params)

    def _calculate_fitness(self):
        self._fitness = self._func(*self._params)
        return self._fitness

    @property
    def fitness(self):
        return self._fitness

    @property
    def params(self):
        return self._params

    def _set_params(self, params):
        self._params = self._constraint_params(params)
        self._calculate_fitness()

    def __eq__(self, other):
        if isinstance(other, Whale):
            return self._id == other._id
        return False

