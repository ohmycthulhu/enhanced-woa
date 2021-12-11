from src.algorithm import WOA


# Class for managing algorithm run
# Provides the interface for starting the algorithm with ExecutionOptions, checking the progress, and getting the result
class AlgorithmManager:
    def __init__(self):
        self._running = None
        self._options = None

    def start_algorithm(self, options):
        self._running = WOA(options)

    def iterate(self):
        if self._running is None:
            return

        self._running.iterate()

    @property
    def progress(self):
        if self._running is None:
            return None, None
        return self._running.current_iteration, self._running.iterations_left

    @property
    def result(self):
        return self._running.result if self._running is not None else None
