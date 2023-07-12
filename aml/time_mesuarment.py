import time


class Timer:
    execution_time = 0.0

    def start(self):
        self.execution_time = 0.0
        self.execution_time = time.time()

    def stop(self):
        self.execution_time = time.time() - self.execution_time

    def get_execution_time(self):
        return self.execution_time

    def print_execution_time(self):
        print('elapsed time {} sek'.format(self.get_execution_time()))
