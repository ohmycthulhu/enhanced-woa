import numpy as np
import json


class RunResult:
    def __init__(self, best_value, best_params, evaluation_count, execution_time):
        self._best_value = best_value
        self._best_params = best_params
        self._evaluation_count = evaluation_count
        self._execution_time = execution_time

    @property
    def best_value(self):
        return self._best_value

    @property
    def best_params(self):
        return self._best_params

    @property
    def execution_time(self):
        return self._execution_time

    @property
    def evaluation_count(self):
        return self._evaluation_count

    def as_json(self):
        return {
            'value': self._best_value,
            'params': [p for p in self._best_params],
            'execution_time': self._execution_time,
            'evaluation_time': self._evaluation_count,
        }


class WOAResult:
    def __init__(self, options):
        self._options = options
        self._results = []
        self._statistics = {'mean': None, 'std': None, 'best': None}

    def _update_statistics(self):
        if len(self._results) == 0:
            self._statistics = {'mean': None, 'std': None, 'best': None}
            return

        values = [r.best_value for r in self._results]
        best_result = self._best_result()

        self._statistics = {
            'mean': float(np.mean(values)),
            'std': float(np.std(values)),
            'best': {'value': best_result.best_value, 'params': [x for x in best_result.best_params]},
            'mean_execution_time': float(np.mean([r.execution_time for r in self._results])),
            'function_evaluation_count': int(np.sum([r.evaluation_count for r in self._results])),
        }

    def _best_result(self):
        min_val, best = np.inf, None
        for result in self._results:
            if result.best_value < min_val:
                best = result
                min_val = result.best_value
        return best

    def append(self, result):
        self._results.append(result)
        self._update_statistics()

    def save_json(self, path):
        with open(path, 'w') as file:
            json.dump(self.to_json(), file)

    def to_json(self):
        return {
            'name': self._options.function_name,
            'statistics': self._statistics,
            'iterations': [r.as_json() for r in self._results]
        }

    @property
    def length(self):
        return len(self._results)
