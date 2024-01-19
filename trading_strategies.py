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
        self.last_tax_buy_value = 1

    def update(self, index, values, dates):
        pass
    
    def calculate_daily_price_change(self, invested_sum, values_i, values_i_1, leverage):
        price_change = (values_i - values_i_1) / values_i_1
        if self.circuit_breakers:
            price_change = self.apply_circuit_breaker(price_change)
        return leverage * invested_sum * price_change

    def calculate_daily_fees(self, invested_sum, fee_factors=[]):
        total_fees = 0
        for fee_factor in fee_factors:
            total_fees += invested_sum * fee_factor / 365.0
        return total_fees
    
    def apply_circuit_breaker(self, change):
        return max(-0.2, change)


class BuyAndHoldStrategy(TradingStrategy):
    def __init__(self, dates, values_close, leverage, ter):
        super().__init__()
        self.dates = dates
        self.values_close = values_close
        self.leverage = leverage
        self.ter = ter

    def update(self, i, invested_sum):
        # apply daily change
        change = self.calculate_daily_price_change(
            invested_sum, self.values_close[i], self.values_close[i - 1], self.leverage)
        invested_sum += change

        # deduct TER
        invested_sum -= self.calculate_daily_fees(invested_sum, [self.ter])

        if self.dates[i].weekday() == 4: # also deduct TER on weekends
            invested_sum -= 2 * self.calculate_daily_fees(invested_sum, [self.ter])
        
        return invested_sum


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

    def update(self, i, invested_sum):
        year = self.dates[i].year

        if year != self.last_year:
            self.last_year = year
            self.high_watermark = invested_sum
        
        # daily change
        if self.bought:
            invested_sum += self.calculate_daily_price_change(
                invested_sum, self.values_open[i], self.values_close[i-1], self.leverage)
            
            invested_sum += self.calculate_daily_price_change(
                invested_sum, self.values_close[i], self.values_open[i], self.leverage)
            
            invested_sum -= self.calculate_daily_fees(
                invested_sum, [self.ter])

        invested_sum -= self.calculate_daily_fees(
                invested_sum, [self.certificate_fee])

        # rotation
        if self.values_close[i] > self.ma[i] and not self.bought:
            self.bought = True
            self.last_tax_buy_value = invested_sum
            invested_sum -= self.spread * invested_sum

        elif self.values_close[i] < self.ma[i] and self.bought:
            self.bought = False
            if self.tax_at_rotation:
                if invested_sum > self.last_tax_buy_value:
                    tax = (invested_sum - self.last_tax_buy_value) * 0.26375
                    if tax > self.losses:
                        tax -= self.losses
                        self.losses = 0
                    else:
                        self.losses -= tax
                        tax = 0
                    invested_sum -= tax
                else:
                    self.losses += self.last_tax_buy_value - invested_sum
            invested_sum -= self.spread * invested_sum
        
        if invested_sum > self.high_watermark:
            new_high_watermark = invested_sum
            invested_sum -= (invested_sum - self.high_watermark) * self.performance_fee
            self.high_watermark = new_high_watermark

        # also deduct fees on weekends
        if self.dates[i].weekday() == 4:
            if self.bought:
                invested_sum -= 2 * self.calculate_daily_fees(
                invested_sum, [self.ter])
        
        return invested_sum

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