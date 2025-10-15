# -*- coding: utf-8 -*-

import os
import sys
import cProfile
import pstats
import datetime


def run_once(bt):
	base_dir = os.path.dirname(os.path.dirname(__file__))
	datapath = os.path.join(base_dir, 'tests', 'datas', '2006-day-001.txt')

	class RunStrategy(bt.Strategy):
		params = dict(main=False)

		def __init__(self):
			# A couple of indicators to increase compute
			bt.indicators.SMA(self.data, period=30)
			bt.indicators.EMA(self.data, period=21)
			bt.indicators.RSI(self.data, period=14)

	data = bt.feeds.BacktraderCSVData(
		dataname=datapath,
		fromdate=datetime.datetime(2006, 1, 1),
		todate=datetime.datetime(2006, 12, 31),
	)
	cerebro = bt.Cerebro(runonce=True, preload=True, exactbars=-1)
	cerebro.adddata(data)
	cerebro.addstrategy(RunStrategy, main=False)
	cerebro.run()


def main(modname: str, rounds: int = 200, out_path: str = None):
	bt = __import__(modname)
	prof = cProfile.Profile()
	prof.enable()
	for _ in range(rounds):
		run_once(bt)
	prof.disable()

	if out_path is None:
		out_path = f"profile_{modname}.pstats"
	prof.dump_stats(out_path)
	stats = pstats.Stats(prof)
	stats.sort_stats(pstats.SortKey.CUMULATIVE)
	print(f"Top 30 cumulative for {modname}:")
	stats.print_stats(30)


if __name__ == "__main__":
	mod = sys.argv[1] if len(sys.argv) > 1 else "backtrader"
	rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 200
	out = sys.argv[3] if len(sys.argv) > 3 else None
	main(mod, rounds, out)


