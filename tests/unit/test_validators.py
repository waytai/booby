# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from expects import expect

from booby import validators, fields, models, errors

from ._helpers import stub_validator


class TestRequired(object):
    def test_when_value_is_none_then_raises_validation_error(self):
        expect(lambda: self.validator(None)).to.raise_error(
            errors.ValidationError, 'is required')

    def test_when_value_is_not_none_then_does_not_raise(self):
        self.validator('foo')

    def setup(self):
        self.validator = validators.Required()


class TestIn(object):
    def test_when_value_is_not_in_choices_then_raises_validation_error(self):
        expect(lambda: self.validator('baz')).to.raise_error(
            errors.ValidationError, "should be in \[u?'foo', u?'bar'\]")

    def test_when_value_is_in_choices_then_does_not_raise(self):
        self.validator('bar')

    def setup(self):
        self.validator = validators.In(['foo', 'bar'])


class StringMixin(object):
    def test_when_value_is_not_string_then_raises_validation_error(self):
        expect(lambda: self.validator(1)).to.raise_error(
            errors.ValidationError, 'should be a string')

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator(None)


class TestString(StringMixin):
    def test_when_value_is_a_string_then_does_not_raise(self):
        self.validator('foo')

    def test_when_value_is_unicode_then_does_not_raise(self):
        self.validator('foo')

    def setup(self):
        self.validator = validators.String()


class TestInteger(object):
    def test_when_value_is_not_an_integer_then_raises_validation_error(self):
        expect(lambda: self.validator('foo')).to.raise_error(
            errors.ValidationError, 'should be an integer')

    def test_when_value_is_an_integer_then_does_not_raise(self):
        self.validator(1)

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator(None)

    def setup(self):
        self.validator = validators.Integer()


class TestFloat(object):
    def test_when_value_is_not_a_float_then_raises_validation_error(self):
        expect(lambda: self.validator('foo')).to.raise_error(
            errors.ValidationError, 'should be a float')

    def test_when_value_is_a_float_then_does_not_raise(self):
        self.validator(1.0)

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator(None)

    def setup(self):
        self.validator = validators.Float()


class TestBoolean(object):
    def test_when_value_is_not_a_boolean_then_raises_validation_error(self):
        expect(lambda: self.validator('foo')).to.raise_error(
            errors.ValidationError, 'should be a boolean')

    def test_when_value_is_a_boolean_then_does_not_raises(self):
        self.validator(False)

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator(None)

    def setup(self):
        self.validator = validators.Boolean()


class TestModel(object):
    def test_when_value_is_not_instance_of_model_then_raises_validation_error(self):
        expect(lambda: self.validator(object())).to.raise_error(
            errors.ValidationError, "should be an instance of 'User'")

    def test_when_model_validate_raises_validation_error_then_raises_validation_error(self):
        class InvalidUser(User):
            def validate(self):
                raise errors.ValidationError()

        expect(lambda: self.validator(InvalidUser())).to.raise_error(
            errors.ValidationError)

    def test_when_model_validate_does_not_raise_then_does_not_raise(self):
        self.validator(User())

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator(None)

    def setup(self):
        self.validator = validators.Model(User)


class TestList(object):
    def test_when_value_is_not_a_list_then_raises_validation_error(self):
        expect(lambda: self.validator(object())).to.raise_error(
            errors.ValidationError, 'should be a list')

    def test_when_value_is_none_then_raises_validation_error(self):
        expect(lambda: self.validator(None)).to.raise_error(
            errors.ValidationError, 'should be a list')

    def test_when_value_is_a_list_then_does_not_raise(self):
        self.validator(['foo', 'bar'])

    def test_when_inner_validator_raises_validation_error_then_raises_validation_error(self):
        def inner_validator(value):
            if value == 'bar':
                raise errors.ValidationError('invalid')

        self.validator = validators.List(stub_validator, inner_validator)

        expect(lambda: self.validator(['foo', 'bar'])).to.raise_error(
            errors.ValidationError, 'invalid')

    def setup(self):
        self.validator = validators.List()


class TestEmail(StringMixin):
    def test_when_value_doesnt_match_email_pattern_then_raises_validation_error(self):
        expect(lambda: self.validator('foo@example')).to.raise_error(
            errors.ValidationError, 'should be a valid email')

    def test_when_value_doesnt_have_at_sign_then_raises_validation_error(self):
        expect(lambda: self.validator('foo%example.com')).to.raise_error(
            errors.ValidationError, 'should be a valid email')

    def test_when_value_is_a_valid_email_then_does_not_raise(self):
        self.validator('foo2bar@example.com')

    def setup(self):
        self.validator = validators.Email()


class User(models.Model):
    name = fields.String()
