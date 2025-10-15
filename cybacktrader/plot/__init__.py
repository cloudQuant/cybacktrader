#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Import from compiled Cython plot module
try:
    from cybacktrader.plot.plot import *
except ImportError:
    pass  # plot may require additional dependencies
