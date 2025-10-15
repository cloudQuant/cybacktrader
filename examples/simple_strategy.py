#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单的 cybacktrader 策略示例

展示如何使用 cybacktrader 进行回测。
这个示例与 backtrader 完全兼容，只需更改导入即可。
"""

import datetime
import os

# 只需将 backtrader 改为 cybacktrader
import cybacktrader as bt


class SimpleStrategy(bt.Strategy):
    """
    简单的移动平均交叉策略
    
    当快速移动平均线向上穿越慢速移动平均线时买入
    当快速移动平均线向下穿越慢速移动平均线时卖出
    """
    
    params = (
        ('fast_period', 10),
        ('slow_period', 30),
        ('printlog', True),
    )
    
    def __init__(self):
        """初始化策略"""
        # 保存收盘价的引用
        self.dataclose = self.datas[0].close
        
        # 追踪待处理订单和买入价格/佣金
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
        # 添加移动平均指标
        self.fast_sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.fast_period)
        
        self.slow_sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.slow_period)
        
        # 交叉信号
        self.crossover = bt.indicators.CrossOver(self.fast_sma, self.slow_sma)
    
    def log(self, txt, dt=None):
        """记录策略日志"""
        if self.params.printlog:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()} {txt}')
    
    def notify_order(self, order):
        """订单状态通知"""
        if order.status in [order.Submitted, order.Accepted]:
            # 订单已提交/接受 - 无需操作
            return
        
        # 检查订单是否完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'买入执行, 价格: {order.executed.price:.2f}, '
                    f'成本: {order.executed.value:.2f}, '
                    f'佣金: {order.executed.comm:.2f}'
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # 卖出
                self.log(
                    f'卖出执行, 价格: {order.executed.price:.2f}, '
                    f'成本: {order.executed.value:.2f}, '
                    f'佣金: {order.executed.comm:.2f}'
                )
            
            self.bar_executed = len(self)
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金不足/拒绝')
        
        # 重置订单
        self.order = None
    
    def notify_trade(self, trade):
        """交易通知"""
        if not trade.isclosed:
            return
        
        self.log(f'交易利润, 毛利润: {trade.pnl:.2f}, 净利润: {trade.pnlcomm:.2f}')
    
    def next(self):
        """策略主逻辑"""
        # 记录收盘价
        self.log(f'收盘价: {self.dataclose[0]:.2f}')
        
        # 检查是否有待处理订单
        if self.order:
            return
        
        # 检查是否持仓
        if not self.position:
            # 没有持仓，检查买入信号
            if self.crossover > 0:
                self.log(f'买入信号, {self.dataclose[0]:.2f}')
                # 买入
                self.order = self.buy()
        
        else:
            # 已持仓，检查卖出信号
            if self.crossover < 0:
                self.log(f'卖出信号, {self.dataclose[0]:.2f}')
                # 卖出
                self.order = self.sell()
    
    def stop(self):
        """策略结束时调用"""
        self.log(
            f'策略结束 - 快速周期: {self.params.fast_period}, '
            f'慢速周期: {self.params.slow_period}, '
            f'期末资金: {self.broker.getvalue():.2f}',
            dt=None
        )


def run_strategy():
    """运行回测"""
    # 创建 Cerebro 引擎
    cerebro = bt.Cerebro()
    
    # 添加策略
    cerebro.addstrategy(SimpleStrategy)
    
    # 获取数据文件路径
    modpath = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join(modpath, '..', 'tests', 'datas', '2006-day-001.txt')
    
    # 创建数据源
    data = bt.feeds.BacktraderCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2006, 1, 1),
        todate=datetime.datetime(2006, 12, 31)
    )
    
    # 添加数据到 Cerebro
    cerebro.adddata(data)
    
    # 设置初始资金
    cerebro.broker.setcash(100000.0)
    
    # 设置佣金 - 0.1%
    cerebro.broker.setcommission(commission=0.001)
    
    # 设置每次交易的股数
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    
    # 添加分析器
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    
    # 打印初始资金
    print(f'初始资金: {cerebro.broker.getvalue():.2f}')
    
    # 运行回测
    results = cerebro.run()
    strat = results[0]
    
    # 打印最终资金
    print(f'期末资金: {cerebro.broker.getvalue():.2f}')
    
    # 打印分析结果
    print('\n--- 分析结果 ---')
    print(f'夏普比率: {strat.analyzers.sharpe.get_analysis()}')
    print(f'收益率: {strat.analyzers.returns.get_analysis()}')
    print(f'回撤: {strat.analyzers.drawdown.get_analysis()}')
    
    # 绘图（可选）
    # cerebro.plot()


if __name__ == '__main__':
    run_strategy()

