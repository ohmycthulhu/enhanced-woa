from src.ui.text import Text
from src.ui.input_manager import InputManager
from src.ui.ui_manager import UIManager
from src.ui.screens.main_screen import MainScreen
from src.algorithm_manager import AlgorithmManager


class Application:
    def __init__(self):
        self._ui_manager = None
        self._algorithm_manager = None

    def boot(self):
        Text.initialize('config/texts.json')
        InputManager.initialize()
        self._ui_manager = UIManager(application=self)
        self._algorithm_manager = AlgorithmManager()

    def start(self):
        start_screen = MainScreen(manager=self._ui_manager)
        self._ui_manager.set_main(start_screen)
        self._ui_manager.go_to_main()

    def update(self):
        self._algorithm_manager.iterate()
        self._ui_manager.update()

    def should_continue(self):
        return self._ui_manager.has_screen()

    def start_algorithm(self, options):
        self._algorithm_manager.start_algorithm(options)

    @property
    def algorithm_progress(self):
        return self._algorithm_manager.progress

    @property
    def algorithm_result(self):
        return self._algorithm_manager.result
