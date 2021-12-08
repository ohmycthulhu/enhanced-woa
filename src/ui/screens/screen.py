class Screen:
    def __init__(self, manager):
        self._manager = manager

    def render(self):
        pass

    def close(self):
        self._manager.go_back()

    def go_to_main(self):
        self._manager.go_to_main()

    def terminate(self):
        pass
