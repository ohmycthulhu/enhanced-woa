from src.ui.input_manager import InputManager
from src.ui.text import Text


class InputRequest:
    def print(self):
        pass

    def get_input(self):
        val = input(self._get_msg())
        while not self._is_valid(val) and not self._return_none(val):
            val = input(self._get_msg())
        return self._parse_input(val) if not self._return_none(val) else None

    def _is_valid(self, inp):
        return True

    def _return_none(self, inp):
        return False

    def _parse_input(self, inp):
        return None

    def _get_msg(self):
        return 'Not implemented'


class NumberInputRequest(InputRequest):
    def __init__(self, name, range_min=None, range_max=None, int_only=False):
        self._name = name
        self._min = range_min
        self._max = range_max
        self._int_only = int_only

    def _is_valid(self, inp):
        val = self._parse_input(inp)

        if self._min is not None and self._min > val:
            return False
        if self._max is not None and self._max < val:
            return False

        return True

    def _parse_input(self, inp):
        try:
            return int(inp) if self._int_only else float(inp)
        except:
            return None

    def _get_msg(self):
        return Text.get_text(
            self._get_string(),
            {'name': self._name, 'min': self._min, 'max': self._max}
        )

    def _get_string(self):
        if self._min is None and self._max is None:
            return 'input.numeric_input'
        elif self._min is None:
            return 'input.numeric_input_max'
        elif self._max is None:
            return 'input.numeric_input_min'
        else:
            return 'input.numeric_input_min_max'


class OptionsInputRequest(InputRequest):
    def __init__(self, msg, option_names):
        self._msg = msg
        self._options = [OptionsRequestOption(index, name) for index, name in enumerate(option_names)]
        self._count = len(self._options)

    def _is_valid(self, inp):
        val = self._parse_input(inp)

        return val is not None and (
            0 <= val < len(self._options)
        )

    def _parse_input(self, inp):
        try:
            return int(inp)
        except:
            return None

    def _get_msg(self):
        return Text.get_text("input.options.request")

    def print(self):
        im = InputManager.get_instance()
        im.print(self._msg)
        for option in self._options:
            im.print(option.get_name())


class OptionsRequestOption:
    def __init__(self, index, name):
        self._index = index
        self._name = name

    def get_name(self):
        return Text.get_text("input.options.option", {'name': self._name, 'index': self._index})
