# -*- coding: utf-8 -*-
"""
This module contains some utilities to maintain compatibility between python 2.5+ and 3
"""
from __future__ import unicode_literals, absolute_import
import sys
import types
import operator

# Define different types for comparison
if sys.version_info[0] == 3:
    str_type = str
    int_type = int
    bool_type = bool
    class_type = type
else:
    str_type = basestring
    int_type = (int, long)
    bool_type = bool
    class_type = (type, types.ClassType)

# Ensure unicode string from byte array
if sys.version_info[0] == 3:
    def b_unicode(x):
        return x.decode('utf-8')
else:
    def b_unicode(x):
        return str(x).encode('utf-8')

# No xrange in python 3
try:
    xrange
except NameError:
    xrange = range
