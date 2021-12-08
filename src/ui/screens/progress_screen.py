from src.ui.screens.screen import Screen
from src.ui.screens.results_screen import ResultsScreen
from src.ui.input_manager import InputManager
from src.ui.text import Text


class ProgressScreen(Screen):
    def render(self):
        current_iteration, iterations_left = self._manager.application.algorithm_progress
        InputManager.get_instance().print(
            Text.get_text(
                'ui.progress.current_progress',
                {'index': current_iteration, 'max': iterations_left + current_iteration}
            )
        )

        if iterations_left <= 0:
            result = self._manager.application.algorithm_result
            result.save_json('results/results.json')
            self._manager.go_to_screen(ResultsScreen(self._manager, result))

