#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

# Import from compiled Cython plot module
try:
    from cybacktrader.plot.plot import *
except ImportError:
    pass  # plot may require additional dependencies
