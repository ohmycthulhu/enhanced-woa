from src.execution_options import ExecutionOptions
from src.benchmark_function import AVAILABLE_FUNCTIONS
from src.ui.screens.screen import Screen
from src.ui.screens.progress_screen import ProgressScreen
from src.ui.input_manager import InputManager
from src.ui.input import OptionsInputRequest, NumberInputRequest
from src.ui.text import Text
from copy import deepcopy


# Class for specifying hyperparameters and changing execution parameters
# Steps are controller by _step variable
# User may go back on each step, going back on the first part will close the screen
# Going forward on the last screen, launches the algorithm and navigates the user to the ProgressScreen
class ExecutionScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)

        self._func = None
        self._hyper_params = {}
        self._execution_params = {}
        self._step = 0

    # Function that decides what should be rendered in the current step
    def render(self):
        if self._step == 0:
            self._render_function_choosing()
        elif self._step == 1:
            self._render_hyperparam_input()
        elif self._step == 2:
            self._render_execution_param_input()
        else:
            self._start()

    def _render_header(self):
        InputManager.get_instance().print(
            Text.get_text('ui.execution.header')
        )

    # Function for rendering function choosing
    # The functions are accessed from AVAILABLE_FUNCTIONS in benchmark_functions file
    # When user chooses a function, it'll be deep copied
    def _render_function_choosing(self):
        self._render_header()

        if self._func is not None:
            InputManager.get_instance().print(
                Text.get_text('ui.execution.chosen_function', {'name': self._func.name})
            )

        req = OptionsInputRequest(
            Text.get_text('ui.execution.choose_function'),
            [func.name for func in AVAILABLE_FUNCTIONS]
        )

        inp = InputManager.get_instance().request_input(req)

        if inp is None:
            return

        if inp < len(AVAILABLE_FUNCTIONS):
            self._func = deepcopy(AVAILABLE_FUNCTIONS[inp])
            self._step += 1
        else:
            self.close()

    # Function for rendering hyperparamater input
    # If there are no available hyperparameters, user will be redirected to the next page
    # Reads the possible hyperparameters and default values from the chosen benchmark function
    def _render_hyperparam_input(self):
        self._render_header()

        if len(self._func.all_hyperparams) == 0:
            self._step += 1
            return

        current_values = {**self._func.hyperparams, **self._hyper_params}
        res = self._render_param_input(self._func.all_hyperparams, current_values, self._can_proceed())

        if res is not None:
            name, val = res
            self._hyper_params[name] = val

    # Function for rendering the step for changing execution options
    # All options are filled by default, so user may always move to the next screen (start algorithm)
    # It gets the list of possible execution options from ExecutionOptions
    def _render_execution_param_input(self):
        self._render_header()

        current_values = {**ExecutionOptions.DEFAULT_OPTIONS, **self._execution_params}
        res = self._render_param_input(current_values.keys(), current_values, True)

        if res is not None:
            name, val = res
            if ExecutionOptions.validate_execution_param(name, val):
                self._execution_params[name] = int(val)

    def _can_proceed(self):
        if not self._func:
            return False

        try:
            self._func.hyperparams = self._hyper_params
        except AttributeError:
            return False

        return True

    def _start(self):
        execution_options = ExecutionOptions(self._func)
        execution_options.hyper_params = self._hyper_params
        execution_options.execution_params = self._execution_params
        self._manager.application.start_algorithm(execution_options)
        self._manager.go_to_screen(ProgressScreen(manager=self._manager))

    # Function for rendering parameter input
    def _render_param_input(self, available_params, param_values, can_proceed):
        im = InputManager.get_instance()

        # Print all parameters
        for name, value in param_values.items():
            im.print(
                Text.get_text('ui.execution.current_hyper_param', {'name': name, 'value': value})
            )

        # Display current parameters
        options = [name for name in available_params] + [Text.get_text('ui.go_back')] + (
            [Text.get_text('ui.next')] if can_proceed else []
        )

        inp = im.request_input(OptionsInputRequest('', options))

        if inp is None:
            return
        if inp < len(available_params):
            param_name = options[inp]
            return param_name, im.request_input(NumberInputRequest(param_name))
        elif inp == len(available_params):
            self._step = 0
        else:
            self._step += 1

    @property
    def _is_valid(self):
        return False
