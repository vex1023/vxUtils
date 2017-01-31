# endcoding = utf-8
'''
author : vex1023
email : vex1023@qq.com
'''

from __future__ import absolute_import, unicode_literals

import six

__all__ = ['to_text', 'to_binary', 'is_string', 'byte2int']

string_types = (six.string_types, six.text_type, six.binary_type)


def to_text(value, encoding="utf-8"):
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def to_binary(value, encoding="utf-8"):
    if isinstance(value, six.binary_type):
        return value
    if isinstance(value, six.text_type):
        return value.encode(encoding)
    return six.binary_type(value)


def is_string(value):
    return isinstance(value, string_types)


def byte2int(s, index=0):
    """Get the ASCII int value of a character in a string.
    :param s: a string
    :param index: the position of desired character
    :return: ASCII int value
    """
    if six.PY2:
        return ord(s[index])
    return s[index]
