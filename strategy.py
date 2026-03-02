import pandas as pd
import ta
from config import *

class TradingState:

    def __init__(self):
        self.df = pd.DataFrame()
        self.in_trade = False
        self.entry_price = 0
        self.stoploss = 0
        self.target = 0
        self.pnl = 0
        self.position = None

    def update_price(self, price):
        new_row = {"close": price}
        self.df = pd.concat([self.df, pd.DataFrame([new_row])])

        if len(self.df) < 25:
            return None

        self.df["ema9"] = ta.trend.ema_indicator(self.df["close"], 9)
        self.df["ema21"] = ta.trend.ema_indicator(self.df["close"], 21)

        if self.df["ema9"].iloc[-2] < self.df["ema21"].iloc[-2] and \
           self.df["ema9"].iloc[-1] > self.df["ema21"].iloc[-1]:
            return "BUY_CE"

        if self.df["ema9"].iloc[-2] > self.df["ema21"].iloc[-2] and \
           self.df["ema9"].iloc[-1] < self.df["ema21"].iloc[-1]:
            return "BUY_PE"

        return None

    def enter_trade(self, price):
        self.in_trade = True
        self.entry_price = price
        self.stoploss = price * (1 - STOPLOSS_PERCENT)
        self.target = price * (1 + TARGET_PERCENT)

    def check_exit(self, ltp):
        if not self.in_trade:
            return None

        if ltp <= self.stoploss:
            self.in_trade = False
            return "STOPLOSS"

        if ltp >= self.target:
            self.in_trade = False
            return "TARGET"

        return None