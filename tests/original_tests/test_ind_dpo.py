#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import testcommon

import cybacktrader.indicators as btind

chkdatas = 1
chkvals = [
    ['83.271000', '105.625000', '1.187000'],
]

chkmin = 29
chkind = btind.DPO

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
