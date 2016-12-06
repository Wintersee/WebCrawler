import datetime
from functools import wraps


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = datetime.datetime.now()
        print(t0)
        result = function(*args, **kwargs)
        t1 = datetime.datetime.now()
        print(t1)
        print("Total time running %s: %s seconds" %
              (function.__name__, str(t1 - t0))
              )
        return result

    return function_timer
