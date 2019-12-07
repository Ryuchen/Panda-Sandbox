#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ========================================================
# @Author: Ryuchen
# @Time: 2019/06/20-22:45
# @Site: https://ryuchen.github.io
# @Contact: chenhaom1993@hotmail.com
# @Copyright: Copyright (C) 2019-2020 Panda-Sandbox.
# ========================================================
"""
Basic variables type setting to protect every setting is correct set
"""

import abc

from numbers import Number

from lib.exceptions.critical import PandaStartupError


class Type(metaclass=abc.ABCMeta):
    """ Base Class for Panda-Sandbox Type Definitions """

    __doc__ = """
    Must Implement this class for subtype to create new instance.
    Initialise its with params:
    :param default::默认值
    :param allow_empty::可取空
    @Must implement with below methods:
    :method parse::转化
    :method check::校验
    """

    def __init__(self, default=None, allow_empty=False):
        self.default = default
        self.allow_empty = allow_empty

        self._value = None

    def __set__(self, instance, value):
        if self.check(value):
            self._value = value
        else:
            self._value = self.parse(value)

    def __str__(self):
        if not self._value:
            return str(self.default)
        return str(self._value)

    @abc.abstractmethod
    def parse(self, value):
        """ parse a raw input value to correct type value and locate in the value range """

    @abc.abstractmethod
    def check(self, value):
        """ check the type of a raw value whether we need this type in this instance """


class Int(Type):
    """ Integer Type Definition class """

    __doc__ = """
    Initialise its with params below:
        :param default::默认值
        :param allow_empty::可取空
        :param v_range::范围 eg: (1, 10)
    """

    def __init__(self, default, allow_empty, v_range=None):
        if v_range:
            (self.min_value, self.max_value) = v_range
            if self.min_value > self.max_value:
                raise PandaStartupError("value range incorrect")
        else:
            (self.min_value, self.max_value) = (None, None)
        super(Int, self).__init__(default, allow_empty)

    def parse(self, value):
        def num_range(ctx, val):
            _fin = val
            if ctx.min_value and val < ctx.min_value:
                _fin = ctx.min_value

            if ctx.max_value and ctx.max_value < val:
                _fin = ctx.max_value
            return _fin

        if isinstance(value, Number):
            if isinstance(value, bool):
                return 1 if value else 0

            return num_range(self, value)

        if isinstance(value, str) and value.isdigit():
            _value = int(value)
            return num_range(self, _value)
        else:
            return self.default

    def check(self, value):
        if isinstance(value, Number):
            if isinstance(value, bool):
                return False

            if self.min_value and value < self.min_value:
                return False

            if self.max_value and self.max_value < value:
                return False
        else:
            return False

        return True


class String(Type):
    """ String Type Definition class """

    __doc__ = """
    Initialise its with params below:
        :param default::默认值
        :param allow_empty::可取空
    """

    def parse(self, value):
        return str(value).strip() if value else self.default

    def check(self, value):
        return isinstance(value, str)


class Boolean(Type):
    """ Boolean Type Definition class """

    __doc__ = """
    Initialise its with params below:
        :param default::默认值
        :param allow_empty::可取空
    """

    def parse(self, value):
        if value in ("true", "True", "yes", "1", "on", "open"):
            return True
        if value in ("false", "False", "no", "0", "off", "close"):
            return False
        return self.default

    def check(self, value):
        return isinstance(value, bool)
