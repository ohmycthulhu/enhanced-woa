from src.ui.input_manager import InputManager
from src.ui.text import Text


# Main class for interacting with UI
# Creates and manages the screens (Screen)
# Provides the interface for starting and updating screens
# Also, provides interface for Screens to interact with the rest of the application
class UIManager:
    def __init__(self, application):
        self._application = application
        self._screens = []
        self._current_screen = None
        self._main_screen = None

    def update(self):
        if self._current_screen is None:
            return

        InputManager.get_instance().clear()
        self._current_screen.render()

    def go_to_screen(self, screen):
        if self._current_screen is not None:
            self._screens.append(self._current_screen)

        self._current_screen = screen

    def terminate(self):
        if self._current_screen is None:
            return

        self._current_screen.terminate()
        for screen in self._screens:
            screen.terminate()
        self._current_screen = None
        InputManager.get_instance().print(Text.get_text('ui.goodbye'))

    def go_back(self):
        screen = self._screens.pop()
        self._current_screen.terminate()
        self._current_screen = screen

    def has_screen(self):
        return self._current_screen is not None

    def go_to_main(self):
        self.go_to_screen(self._main_screen)

    def set_main(self, screen):
        self._main_screen = screen

    @property
    def application(self):
        return self._application
