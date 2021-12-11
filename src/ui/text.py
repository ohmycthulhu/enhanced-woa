import json


# Singleton class for accessing text
# Makes base for internationalization, but doesn't provide language other than English
# Reads JSON file and stores the content in the memory
# For accessing the file, the user uses Text.get_text(key, {}) syntax
# key is point-separated list of keys. E.g. "some.key.to.value" translated to data['some']['key']['to']['value']
class Text:
    _instance = None

    @staticmethod
    def initialize(path):
        Text._instance = Text(path)
        return Text.get_instance()

    @staticmethod
    def get_instance():
        return Text._instance

    @staticmethod
    def get_text(path, variables=None):
        string = Text._instance.get_string(path)
        return Text._interpolate(string, variables if variables is not None else {})

    def __init__(self, path):
        self._path = path
        self._locale = 'en'
        with open(path) as file:
            self._texts = json.load(file)

    @staticmethod
    def _interpolate(string, variables):
        res = string
        for key in variables:
            res = res.replace(f'{{{key}}}', str(variables[key]))
        return res

    def get_string(self, path):
        locale_texts = self._texts[self._locale]
        current_text = locale_texts
        steps = path.split('.')
        for step in steps:
            if step not in current_text:
                raise IndexError(f"{self._locale}.{path} does not exists")
            current_text = current_text[step]

        return str(current_text)
