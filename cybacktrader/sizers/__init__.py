#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Import from compiled Cython sizer modules
from cybacktrader.sizers.fixedsize import *
from cybacktrader.sizers.percents_sizer import *

# Alias for compatibility
SizerFix = FixedSize
