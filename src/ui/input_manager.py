from os.path import exists
import os
import json


# Singleton class that handles the implementation of UI interaction
# Allows reading and printing the messages to the user
# For getting certain input, user provides InputRequest that handles constraints and specifics of some request
class InputManager:
    _instance = None

    @staticmethod
    def get_instance():
        return InputManager._instance

    @staticmethod
    def initialize():
        InputManager._instance = InputManager()

    def request_input(self, input_request):
        input_request.print()
        return input_request.get_input()

    def print(self, text):
        print(text)

    def read_input(self, msg=''):
        return input(msg)

    def file_exists(self, path):
        return exists(path)

    def save_json(self, obj, path):
        dir_name = '/'.join(path.split('/')[:-1])
        if not exists(dir_name):
            os.mkdir(dir_name)

        with open(path, 'w') as file:
            json.dump(obj, file, indent=4, ensure_ascii=False)

    def load_json(self, path):
        if not exists(path):
            return None

        with open(path) as file:
            result = json.load(file)

        return result

    def clear(self):
        self.print('\n'*10)
        os.system('cls' if os.name == 'nt' else 'clear')
