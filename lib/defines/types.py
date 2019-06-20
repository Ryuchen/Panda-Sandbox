#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-06-20 22:45
# @Author : ryuchen
# @File : types.py
# @Desc :
# ==================================================
import re
import click
import numbers
import logging

log = logging.getLogger(__name__)


def parse_bool(value):
    """Attempt to parse a boolean value."""
    if value in ("true", "True", "yes", "1", "on"):
        return True
    if value in ("false", "False", "None", "no", "0", "off"):
        return False
    return bool(int(value))


class Type:
    """Base Class for Type Definitions"""

    def __init__(self, default=None, required=True, sanitize=False, allow_empty=False):
        self.default = self.parse(default)

        self.required = required
        self.sanitize = sanitize
        self.allow_empty = allow_empty

    def parse(self, value):
        """Parse a raw input value."""

    def check(self, value):
        """Checks the type of the value."""

    def emit(self, value):
        """String-readable version of this object"""


class Int(Type):
    """Integer Type Definition class."""

    def parse(self, value):
        if isinstance(value, (int, numbers.Complex)):
            return value

        if isinstance(value, str) and value.isdigit():
            return int(value)

    def check(self, value):
        if self.allow_empty and not value:
            return True

        try:
            click.INT(value)
            return True
        except click.exceptions.BadParameter:
            return False

    def emit(self, value):
        return "%d" % value if value else ""


class String(Type):
    """String Type Definition class."""

    def parse(self, value):
        return value.strip() if value else None

    def check(self, value):
        if self.allow_empty and not value:
            return True

        return isinstance(value, str)

    def emit(self, value):
        return value or ""


class Path(String):
    """Path Type Definition class."""

    def __init__(
        self,
        default=None,
        exists=False,
        writable=False,
        readable=False,
        required=True,
        allow_empty=False,
        sanitize=False,
    ):
        self.exists = exists
        self.writable = writable
        self.readable = readable
        super(Path, self).__init__(default, required, sanitize, allow_empty)

    def parse(self, value):
        if self.allow_empty and not value:
            return

        try:
            c = click.Path(
                exists=self.exists, writable=self.writable, readable=self.readable
            )
            return c.convert(value, None, None)
        except click.exceptions.BadParameter:
            return value

    def check(self, value):
        if self.allow_empty and not value:
            return True

        try:
            c = click.Path(
                exists=self.exists, writable=self.writable, readable=self.readable
            )
            c.convert(value, None, None)
            return True
        except click.exceptions.BadParameter:
            return False

    def emit(self, value):
        return value or ""


class Boolean(Type):
    """Boolean Type Definition class."""

    def parse(self, value):
        try:
            return parse_bool(value)
        except ValueError:
            log.error("Incorrect Boolean %s", value)
            return False

    def check(self, value):
        try:
            parse_bool(value)
            return True
        except ValueError:
            return False

    def emit(self, value):
        return "yes" if value else "no"


class UUID(Type):
    """UUID Type Definition class."""

    def parse(self, value):
        try:
            c = click.UUID(value)
            return str(c)
        except click.exceptions.BadParameter:
            log.error("Incorrect UUID %s", value)

    def check(self, value):
        """Check if the value is of type UUID."""
        try:
            click.UUID(value)
            return True
        except click.exceptions.BadParameter:
            return False

    def emit(self, value):
        return value


class List(Type):
    """List Type Definition class."""

    def __init__(self, subclass, default, sep=",", strip=True):
        self.subclass = subclass
        self.sep = sep
        self.strip = strip
        super(List, self).__init__(default)

    def parse(self, value):
        if value is None:
            return []

        try:
            ret = []

            if isinstance(value, (tuple, list)):
                for entry in value:
                    ret.append(self.subclass().parse(entry))
                return ret

            for entry in re.split("[%s]" % self.sep, value):
                if self.strip:
                    entry = entry.strip()
                    if not entry:
                        continue

                ret.append(self.subclass().parse(entry))
            return ret
        except ValueError:
            log.error("Incorrect list: %s", value)
            return []

    def check(self, value):
        try:
            value.split(self.sep)
            return True
        except AttributeError:
            return False

    def emit(self, value):
        return (", " if self.sep[0] == "," else self.sep[0]).join(value or "")
