import logging
import logging.handlers
import inspect

from functools import wraps

from .log_config import handler


def log(logger):
    def deco(f):
        func = f

        logger.addHandler(handler)

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                main_name = inspect.stack()[1][3]
            except IndexError:
                main_name = logger.name
            step = 12
            log_pattern = 'Function\t{:<{}} \tcalled from \t{}'.format(func.__name__, step, main_name)
            result = func(*args, **kwargs)
            if result:
                logger.setLevel(logging.INFO)
                logger.info(log_pattern)
            else:
                logger.setLevel(logging.CRITICAL)
                logger.info(log_pattern)
            return result

        return wrapper

    return deco


if __name__ == '__main__':

    @log
    def some_func(*args):
        print('===some_func function===')
        print(args)
        if args[0]:
            return int(args[0][0]) + int(args[0][1])
        else:
            pass

    # print(some_func(1, 2))

    # print(some_func())
