import random
from functools import wraps

from faker import Faker


class InputParameterVerificationError(Exception):
    pass


class ResultVerificationError(Exception):
    pass


def input_validation(input_parameter):
    return random.choice([True, False])


def result_validation(result):
    return random.choice([True, False])


def decorator(input_validation, result_validation, on_fail_repeat_times=1, default_behavior=None):
    def decoration(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Multipurpose decorator"""
            errors_list = []
            if input_validation(*args, **kwargs):
                result = func(*args, **kwargs)
                if result_validation(result):
                    return result
                else:
                    errors_list.append(ResultVerificationError(f"Результат работы функции {result} невалиден!"))
                    for _ in range(on_fail_repeat_times):
                        result = func(*args, **kwargs)
                        if result_validation(result):
                            return result
                        else:
                            errors_list.append(ResultVerificationError(
                                f"Результат работы функции {result} невалиден!"))
                    if default_behavior:
                        default_behavior()
                    else:
                        raise errors_list[-1]
            else:
                raise InputParameterVerificationError(f"Входной параметр {args, kwargs} невалиден!")
        return wrapper
    return decoration


@decorator(input_validation, result_validation, default_behavior=lambda: print("Default behavior"))
def foo1(input_parameter):
    """Our function number 1"""
    result = input_parameter
    print(result)
    return result


@decorator(input_validation, result_validation)
def foo2(input_parameter):
    """Our function number 2"""
    result = None
    print(result)
    return result


if __name__ == "__main__":
    foo1("Привет")
