import re
from functools import wraps
from typing import Any, Callable, Optional

from faker import Faker
from faker.config import AVAILABLE_LOCALES
import jsonschema


class InputParameterVerificationError(Exception):
    """Error that raises when input parameter is not valid."""

    pass


class ResultVerificationError(Exception):
    """Error that raises when result of decorated function is not valid."""

    pass


def decorator(
    input_validation: Callable[..., bool],
    result_validation: Callable[[Any], bool],
    on_fail_repeat_times: int = 1,
    default_behavior: Optional[Callable] = None,
) -> Callable:
    """Multipurpose decorator with parameters.

    Checks if decorated function input paramaters and result are valid.
    If they are alright returns result of decorated function,
    else do dome stuff (see args below).

    Arghs:
        input_validation:
            Function validating input parameters of decorated function.
        result_validation:
            Function validating result of decorated function.
        on_fail_repeat_times:
            Optional; Defines how much times (after first validation of
            decorated function result in case when this first validation
            is failed) decorator should recall decorated function until
            it return valid result. If on_fail_repeat_times is negative
            there would be infinite recalling decorated function
            until it return valid result.
        default_behavior:
            Optional; A function that should be called in the end if
            decorated function didn't return valid result.
            If default_behavior=None decorator returns result of decorated
            function if result is valid else raises ResultVerificationError.

    Returns:
        Result of decorated function or result of other function
        defined as default_behavior parameter.

    Raises:
        InputParameterVerificationError:
            If decorated function input paramaters are invalid.
        ResultVerificationError:
            If decorated function result is invalid and parameter
            default_behavior in decorator not defined.
    """

    def decoration(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            errors_list = []
            if input_validation(*args, **kwargs):
                result = func(*args, **kwargs)
                if result_validation(result):
                    return result
                else:
                    errors_list.append(ResultVerificationError(f"Результат работы функции {result} невалиден!"))
                    nonlocal on_fail_repeat_times
                    while on_fail_repeat_times != 0:
                        result = func(*args, **kwargs)
                        if result_validation(result):
                            return result
                        else:
                            errors_list.append(ResultVerificationError(f"Результат работы функции {result} невалиден!"))
                        on_fail_repeat_times -= 1
                    if default_behavior:
                        return default_behavior()
                    else:
                        raise errors_list[-1]
            else:
                raise InputParameterVerificationError(f"Входной параметр {args, kwargs} невалиден!")

        return wrapper

    return decoration


SCHEMA = {
    "type": "object",
    "title": "Fake name creating schema",
    "description": "The root schema comprises the entire JSON document",
    "default": {},
    "examples": [{"locale": "ru_RU"}],
    "required": ["locale"],
    "additionalProperties": False,
    "properties": {
        "locale": {
            "description": "Defines the locale of name that should be created",
            "type": "string",
            "enum": AVAILABLE_LOCALES,
        }
    },
}


def validate_locale(argument: dict) -> bool:
    """Validate dictionary according schema.

    Arghs:
        argument: Dictionary to validate.

    Returns:
        True if dictionary is valid, else False.
    """
    try:
        return not bool(jsonschema.validate(argument, SCHEMA))
    except jsonschema.ValidationError:
        return False


def check_fullname(fullname: str) -> bool:
    """Check if fullname meets the requirement.

    Fullname should be a string including only a-z and A-Z letters and whitespace,
    also first letter of the each word should be uppercase and all other lowercase.
    """
    regex = re.compile(r"^[A-Z][a-z]*( [A-Z][a-z]*)+$")
    return bool(regex.match(fullname))


def default_behavior_for_create_fake_fullname() -> None:
    """Function that should be called if result of create_fake_fullname function is invalid."""
    print("Function didn't create a name with only a-z and A-Z letters and whitespace")


def create_fake_fullname(argument: dict) -> str:
    """Create fake name.

    Args:
        argument: Dictionary with required "locale" key.

    Returns:
        String with fake name appropriated with locale specified in argument.
    """
    fake = Faker(argument["locale"])  # type: ignore
    return fake.name()


if __name__ == "__main__":
    create_fake_fullname = decorator(
        validate_locale,
        check_fullname,
        on_fail_repeat_times=1,
        default_behavior=default_behavior_for_create_fake_fullname,
    )(create_fake_fullname)
    print(create_fake_fullname({"locale": "it_IT"}))
