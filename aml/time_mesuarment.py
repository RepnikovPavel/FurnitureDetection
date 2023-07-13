import time
from functools import wraps

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

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

