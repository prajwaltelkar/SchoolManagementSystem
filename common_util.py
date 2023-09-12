class ApplicationState:
    def __init__(self):
        self.program_running = True

    def stop_program(self):
        self.program_running = False

    def is_program_running(self):
        return self.program_running
