from src.ui.text import Text
from src.ui.input_manager import InputManager
from src.ui.ui_manager import UIManager
from src.ui.screens.main_screen import MainScreen
from src.algorithm_manager import AlgorithmManager


# Class that is responsible for the whole application
# Contains method for booting the application and main loop
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
        self._ensure_application_booted()
        start_screen = MainScreen(manager=self._ui_manager)
        self._ui_manager.set_main(start_screen)
        self._ui_manager.go_to_main()

    def update(self):
        self._ensure_application_booted()
        self._algorithm_manager.iterate()
        self._ui_manager.update()

    def should_continue(self):
        self._ensure_application_booted()
        return self._ui_manager.has_screen()

    def start_algorithm(self, options):
        self._ensure_application_booted()
        self._algorithm_manager.start_algorithm(options)

    def _ensure_application_booted(self):
        if self._ui_manager is None or self._algorithm_manager is None:
            raise Exception("Application has not been booted yet")

    @property
    def algorithm_progress(self):
        self._ensure_application_booted()
        return self._algorithm_manager.progress

    @property
    def algorithm_result(self):
        self._ensure_application_booted()
        return self._algorithm_manager.result
