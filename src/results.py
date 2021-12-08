import numpy as np
import json
from src.ui.input_manager import InputManager


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

    @staticmethod
    def from_json(data):
        return RunResult(
            best_value=data.get('value'),
            best_params=np.array(data.get('params', [])),
            evaluation_count=data.get('evaluation_time'),
            execution_time=data.get('execution_time'),
        )


class WOAResult:
    def __init__(self, function_name, results=None, statistics=None):
        self._function_name = function_name
        self._results = results if results is not None else []
        self._statistics = statistics if statistics is not None else {'mean': None, 'std': None, 'best': None}

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
        InputManager.get_instance().save_json(self.to_json(), path)

    def to_json(self):
        return {
            'name': self._function_name,
            'statistics': self._statistics,
            'iterations': [r.as_json() for r in self._results]
        }

    @staticmethod
    def from_json(data):
        results = [RunResult.from_json(it) for it in data.get('iterations', [])]

        return WOAResult(
            function_name=data.get('name'),
            results=results,
            statistics=data.get('statistics'),
        )

    @property
    def length(self):
        return len(self._results)

    @property
    def statistics(self):
        return self._statistics

    @property
    def iterations(self):
        return self._results

    @property
    def function_name(self):
        return self._function_name
