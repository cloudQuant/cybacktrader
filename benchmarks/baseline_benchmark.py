# -*- coding: utf-8 -*-

import os
import time
import statistics
import datetime


def run_once(import_name):
    mod = __import__(import_name)
    bt = mod

    # Minimal SMA run using dataset in tests/datas
    base_dir = os.path.dirname(os.path.dirname(__file__))
    datapath = os.path.join(base_dir, 'tests', 'datas', '2006-day-001.txt')

    class RunStrategy(bt.Strategy):
        params = dict(main=False)

        def __init__(self):
            bt.indicators.SMA(self.data, period=30)

    data = bt.feeds.BacktraderCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2006, 1, 1),
        todate=datetime.datetime(2006, 12, 31),
    )
    cerebro = bt.Cerebro(runonce=True, preload=True, exactbars=-1)
    cerebro.adddata(data)
    cerebro.addstrategy(RunStrategy, main=False)

    t0 = time.perf_counter()
    cerebro.run()
    return time.perf_counter() - t0


def run_benchmark(rounds=3):
	results = {}
	for name in ("backtrader", "cybacktrader"):
		times = []
		for _ in range(rounds):
			t = run_once(name)
			times.append(t)
		results[name] = dict(
			min=min(times), max=max(times), avg=statistics.mean(times), raw=times
		)
	return results


if __name__ == "__main__":
	res = run_benchmark(rounds=3)
	print("Baseline benchmark (seconds):")
	for k, v in res.items():
		print(k, v)
