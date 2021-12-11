from src.ui.input_manager import InputManager
from src.ui.input import OptionsInputRequest
from src.ui.text import Text
from src.ui.screens.screen import Screen
from src.ui.screens.execution_screen import ExecutionScreen
from src.ui.screens.results_screen import ResultsScreen
from src.results import WOAResult


# Class for the main screen
# It checks whether the last results are available, navigate user to the ExecutionScreen or ResultsScreen
# For navigating to the ResultsScreen, it loads results from JSON file and creates the screen
class MainScreen(Screen):
    LAST_RESULTS = 'results/results.json'

    def render(self):
        available_options = self._get_options()

        input_request = OptionsInputRequest(
            msg=Text.get_text('ui.select_screen'),
            option_names=available_options
        )

        chosen_index = InputManager.get_instance().request_input(input_request)

        if chosen_index is None:
            return

        screen = self._get_screen(chosen_index)
        if screen is not None:
            self._manager.go_to_screen(screen)
        else:
            self._manager.terminate()

    def _get_options(self):
        available_screens = [
            Text.get_text('screens.execution'),
        ]

        if self._last_results_exists():
            available_screens.append(Text.get_text('screens.results'))

        return available_screens + [Text.get_text('ui.close_application')]

    def _last_results_exists(self):
        return InputManager.get_instance().file_exists(self.LAST_RESULTS)

    def _load_last_results(self):
        data = InputManager.get_instance().load_json(self.LAST_RESULTS)

        if data is None:
            return None

        return WOAResult.from_json(data)

    def _get_screen(self, index):
        if index == 0:
            return ExecutionScreen(self._manager)
        if index == 1:
            results = self._load_last_results()
            if results is None:
                return None
            return ResultsScreen(self._manager, results)


