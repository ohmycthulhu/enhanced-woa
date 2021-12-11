from src.application import Application
from src.ui.input_manager import InputManager
from src.ui.input import NumberInputRequest, OptionsInputRequest

application = Application()

application.boot()

application.start()

while application.should_continue():
    application.update()
