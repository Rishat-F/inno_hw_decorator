import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from constant_test_cases import LOCALE_TEST_CASES, FULLNAME_TEST_CASES
from main import (InputParameterVerificationError, ResultVerificationError,
                  decorator, validate_locale, check_fullname, create_fake_fullname)


class TestDecoratorRaisingErrors:

    @decorator(input_validation=lambda *args, **kwargs: False,
                    result_validation=lambda result: True)
    def func_with_input_error(self):
        pass

    @decorator(input_validation=lambda *args, **kwargs: True,
                    result_validation=lambda result: False)
    def func_with_result_error(self):
        pass

    def test_input_parameter_verification_error(self):
        with pytest.raises(InputParameterVerificationError) as exc_raised:
            self.func_with_input_error()
        assert exc_raised.errisinstance(InputParameterVerificationError)

    def test_result_verification_error(self):
        with pytest.raises(ResultVerificationError) as exc_raised:
            self.func_with_result_error()
        assert exc_raised.errisinstance(ResultVerificationError)


class TestDecorator:
    @decorator(input_validation=lambda *args, **kwargs: True,
               result_validation=lambda *args, **kwargs: False,
               default_behavior=lambda: "default behavior"
               )
    def func_should_call_default_behavior(self):
        pass

    def test_decorator_calls_default_behavior_function(self):
        assert self.func_should_call_default_behavior() == "default behavior"

    @decorator(input_validation=lambda *args, **kwargs: True,
                    result_validation=lambda result: True)
    def decorated_func(self):
        result = 200
        return result

    def test_result_of_decorated_function(self):
        assert self.decorated_func() == 200


class TestMainFunctions:

    def test_validating_valid_locales(self):
        for valid_locale_dict in LOCALE_TEST_CASES["valid"]:
            assert validate_locale(valid_locale_dict)

    def test_validating_invalid_locales(self):
        for invalid_locale_dict in LOCALE_TEST_CASES["invalid"]:
            assert not validate_locale(invalid_locale_dict)

    def test_validating_valid_fullnames(self):
        for valid_fullname in FULLNAME_TEST_CASES["valid"]:
            assert check_fullname(valid_fullname)

    def test_validating_invalid_fullnames(self):
        for invalid_fullname in FULLNAME_TEST_CASES["invalid"]:
            assert not check_fullname(invalid_fullname)

    def test_create_fake_fullname(self):
        fullname = create_fake_fullname({"locale": "it_IT"})
        assert isinstance(fullname, str)
