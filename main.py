import random
from functools import wraps

from faker import Faker


class InputParameterVerificationError(Exception):
    pass


class ResultVerificationError(Exception):
    pass


def input_validation(*args, **kwargs):
    return random.choice([True, True])


def result_validation(result):
    return random.choice([False, False])


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
                    nonlocal on_fail_repeat_times
                    while on_fail_repeat_times != 0:
                        print(f"Вызов функции после провала валидации результата номер: {on_fail_repeat_times}")
                        result = func(*args, **kwargs)
                        if result_validation(result):
                            return result
                        else:
                            errors_list.append(ResultVerificationError(
                                f"Результат работы функции {result} невалиден!"))
                        on_fail_repeat_times -= 1
                    if default_behavior:
                        return default_behavior()
                    else:
                        raise errors_list[-1]
            else:
                raise InputParameterVerificationError(f"Входной параметр {args, kwargs} невалиден!")
        return wrapper
    return decoration


@decorator(input_validation, result_validation, on_fail_repeat_times=1)
def foo1(*args, **kwargs):
    """Our function number 1"""
    result = args, kwargs
    return result


@decorator(input_validation, result_validation)
def foo2(input_parameter):
    """Our function number 2"""
    result = None
    return result


if __name__ == "__main__":
    print(foo1("Привет", x=2))