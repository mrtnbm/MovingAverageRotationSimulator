from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass
import pandas as pd
import numpy as np
from technical_indicators import TechnicalIndicators
from strategy_simulator import StrategySimulator

class TradingStrategy:
    def __init__(self):
        self.circuit_breakers = False
        self.invested_sum = 1
        self.last_tax_buy_value = 1

    def update(self, index, values, dates):
        pass
    
    def calculate_daily_price_change(self, values_i, values_i_1, leverage):
        price_change = (values_i - values_i_1) / values_i_1
        if self.circuit_breakers:
            price_change = self.apply_circuit_breaker(price_change)
        return leverage * self.invested_sum * price_change

    def calculate_daily_fees(self, fee_factors=[]):
        total_fees = 0
        for fee_factor in fee_factors:
            total_fees += self.invested_sum * fee_factor / 365.0
        return total_fees
    
    def apply_circuit_breaker(self, change):
        return max(-0.2, change)


class BuyAndHoldStrategy(TradingStrategy):
    def __init__(self, dates, values_close, leverage, ter, spread):
        super().__init__()
        self.dates = dates
        self.values_close = values_close
        self.leverage = leverage
        self.ter = ter
        self.spread = spread

    def update(self, i):
        # apply daily change
        change = self.calculate_daily_price_change(
            self.values_close[i], self.values_close[i - 1], self.leverage)
        self.invested_sum += change

        # deduct TER
        self.invested_sum -= self.calculate_daily_fees([self.ter])

        if self.dates[i].weekday() == 4: # also deduct TER on weekends
            self.invested_sum -= 2 * self.calculate_daily_fees([self.ter])


class RotaryMAStrategy(TradingStrategy):
    def __init__(self, dates, values_open, values_close, window_size, leverage, ter, certificate_fee, spread, performance_fee=0, tax_at_rotation=False):
        super().__init__()
        self.bought = True
        self.ter = ter
        self.leverage = leverage
        self.window_size = window_size
        self.spread = spread
        self.ma = TechnicalIndicators.get_moving_average(values_close, window_size, type='sma')
        self.ma = self.ma[window_size:]
        self.dates = dates[window_size:]
        self.values_open = values_open[window_size:]
        self.values_close = values_close[window_size:]
        self.last_year = self.dates[0].year
        self.losses = 0
        self.high_watermark = 0
        self.tax_at_rotation = tax_at_rotation
        self.performance_fee = performance_fee
        self.certificate_fee = certificate_fee

        if self.values_close[0] > self.ma[0]:
            self.bought = True
            self.invested_sum -= self.spread * self.invested_sum

    def update(self, i):
        year = self.dates[i].year

        if year != self.last_year:
            self.last_year = year
            self.high_watermark = self.invested_sum
        
        # daily change
        if self.bought:
            self.invested_sum += self.calculate_daily_price_change(
                self.values_open[i], self.values_close[i-1], self.leverage)
            
            self.invested_sum += self.calculate_daily_price_change(
                self.values_close[i], self.values_open[i], self.leverage)
            
            self.invested_sum -= self.calculate_daily_fees([self.ter])

        self.invested_sum -= self.calculate_daily_fees([self.certificate_fee])

        # rotation
        if self.values_close[i] > self.ma[i] and not self.bought:
            self.bought = True
            self.last_tax_buy_value = self.invested_sum
            self.invested_sum -= self.spread * self.invested_sum

        elif self.values_close[i] < self.ma[i] and self.bought:
            self.bought = False
            if self.tax_at_rotation:
                if self.invested_sum > self.last_tax_buy_value:
                    tax = (self.invested_sum - self.last_tax_buy_value) * 0.26375
                    if tax > self.losses:
                        tax -= self.losses
                        self.losses = 0
                    else:
                        self.losses -= tax
                        tax = 0
                    self.invested_sum -= tax
                else:
                    self.losses += self.last_tax_buy_value - self.invested_sum
            self.invested_sum -= self.spread * self.invested_sum
        
        if self.invested_sum > self.high_watermark:
            new_high_watermark = self.invested_sum
            self.invested_sum -= (self.invested_sum - self.high_watermark) * self.performance_fee
            self.high_watermark = new_high_watermark

        # also deduct fees on weekends
        if self.dates[i].weekday() == 4:
            if self.bought:
                self.invested_sum -= 2 * self.calculate_daily_fees(
                    [self.ter])
        
    @staticmethod
    def calculate_best_params(dates,
                          values_open,
                          values_close,
                          window_sizes,
                          leverages,
                          ter,
                          certificate_fee,
                          spread,
                          performance_fee,
                          tax_at_rotation):
        best_growth = 0
        best_lev = 1
        best_window_size = 200
        max_window_size = window_sizes[-1]

        for ws in window_sizes:
            for lev in leverages:
                rotary_strategy = RotaryMAStrategy(
                    dates=dates[max_window_size-ws:],
                    values_open=values_open[max_window_size-ws:],
                    values_close=values_close[max_window_size-ws:],
                    window_size=ws,
                    leverage=lev,
                    ter=ter,
                    certificate_fee=certificate_fee,
                    spread=spread,
                    performance_fee=performance_fee,
                )
                invested_sums = StrategySimulator.simulate(rotary_strategy)
                growth = invested_sums[-1]
                
                if growth > best_growth:
                    best_growth = growth
                    best_lev = lev
                    best_window_size = ws

        return best_lev, best_window_size