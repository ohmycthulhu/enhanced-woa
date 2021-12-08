from src.ui.screens.screen import Screen
from src.ui.input_manager import InputManager
from src.ui.input import OptionsInputRequest
from src.ui.text import Text


class ResultsScreen(Screen):
    def __init__(self, manager, results):
        super().__init__(manager)
        self._results = results
        self._current_screen = 'brief'

    def render(self):
        im = InputManager.get_instance()
        im.print(Text.get_text('ui.results.header'))
        im.print(Text.get_text(self._get_header()))

        if self.show_brief:
            self._print_brief()
        else:
            self._print_detailed()

        inp = im.request_input(OptionsInputRequest(
            msg=Text.get_text('ui.select_screen'),
            option_names=self._get_options()
        ))

        if inp is None:
            return

        if inp == 0:
            self._current_screen = 'detailed' if self.show_brief else 'brief'
        else:
            self.go_to_main()

    def _print_info(self):
        InputManager.get_instance().print(
            Text.get_text('ui.results.func_name', {'name': self._results.function_name})
        )

    def _print_brief(self):
        self._print_info()
        im = InputManager.get_instance()
        statistics = self._results.statistics
        im.print(Text.get_text('ui.results.best', {'value': statistics['best']['value']}))
        im.print(Text.get_text('ui.results.mean', {'mean': statistics['mean']}))
        im.print(Text.get_text('ui.results.std', {'std': statistics['std']}))
        im.print(Text.get_text('ui.results.evaluation_count', {'count': statistics['function_evaluation_count']}))

    def _print_detailed(self):
        self._print_info()
        im = InputManager.get_instance()
        im.print(
            '#\tValue\tExecution Time\tEvaluation Count'
        )
        for index, iteration in enumerate(self._results.iterations):
            im.print(
                f'{index}\t{iteration.best_value}\t'
                f'{iteration.execution_time}\t{iteration.evaluation_count}'
            )

    def _go_to_detailed(self):
        self._current_screen = 'detailed'

    def _go_to_brief(self):
        self._current_screen = 'brief'

    def _get_header(self):
        return 'ui.results.' + ('brief' if self.show_brief else 'detailed')

    def _get_options(self):
        base = Text.get_text('screens.main')

        if self.show_brief:
            return [Text.get_text('screens.results_detailed')] + [base]
        else:
            return [Text.get_text('screens.results_brief')] + [base]

    @property
    def show_brief(self):
        return self._current_screen == 'brief'
