# Task 1

import logging
from functools import wraps
from pathlib import Path


log_file = Path(__file__).parent / "decorator.log"

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    file_handler = logging.FileHandler(
        log_file,
        mode="a",
        encoding="utf-8",
    )
    logger.addHandler(file_handler)


def logger_decorator(func):
    """Log the function name, parameters, and return value."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        positional_parameters = list(args) if args else "none"
        keyword_parameters = kwargs if kwargs else "none"

        logger.info("function: %s", func.__name__)
        logger.info(
            "positional parameters: %s",
            positional_parameters,
        )
        logger.info(
            "keyword parameters: %s",
            keyword_parameters,
        )
        logger.info("return: %s", result)

        return result

    return wrapper


@logger_decorator
def say_hello():
    """Take no parameters and return nothing."""
    print("Hello, World!")


@logger_decorator
def accept_positional_arguments(*args):
    """Take any number of positional arguments and return True."""
    return True


@logger_decorator
def accept_keyword_arguments(**kwargs):
    """Take keyword arguments and return logger_decorator."""
    return logger_decorator


if __name__ == "__main__":
    say_hello()

    accept_positional_arguments(
        "Python",
        100,
        True,
    )

    accept_keyword_arguments(
        course="Python 100",
        assignment=3,
    )