# -*- coding: utf-8 -*-


class Field(object):
    def __init__(self, **kwargs):
        self.name = None
        self.required = kwargs.get('required', False)
        self.choices = kwargs.get('choices')

        if self.choices and not isinstance(self.choices, (list, tuple)):
            raise TypeError("'choices' should be a sequence type")

        default = kwargs.get('default')
        self.default = self.validate(default) if default is not None else default

    def __get__(self, instance, owner):
        if instance is not None:
            return instance._data.get(self, self.default)
        return self

    def __set__(self, instance, value):
        instance._data[self] = self._validate(value)

    def _validate(self, value):
        if value is None:
            if self.required:
                raise ValueError("Field '{0}' is required".format(self.name))
            return value

        if self.choices and value not in self.choices:
            raise ValueError('Invalid value: {0}'.format(value))

        return self.validate(value)

    def validate(self, value):
        raise NotImplementedError()


class StringField(Field):
    def validate(self, value):
        if not isinstance(value, basestring):
            raise ValueError('Invalid value: {0}'.format(value))
        return value
