#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import testcommon

chkdatas = 1
chkvals = [
    ['nan', 'nan', 'nan'],
    ['nan', 'nan', '3553.692850']
]

chkmin = 5
from cybacktrader.utils.fractal import Fractal as chkind

def test_run(main=False):
    datas = [testcommon.getdata(i) for i in range(chkdatas)]
    testcommon.runtest(datas,
                       testcommon.TestStrategy,
                       main=main,
                       plot=main,
                       chkind=chkind,
                       chkmin=chkmin,
                       chkvals=chkvals)

if __name__ == '__main__':
    test_run(main=True)
