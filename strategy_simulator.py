import math
import numpy as np
from visualization import InvestmentGrowthGraph
from utils import factor_to_percentage, floor2

class StrategySimulator:
    @staticmethod
    def simulate(trading_strategy):
        invested_sum = 1
        invested_sums = [invested_sum]

        for i in range(1, len(trading_strategy.dates)):
            trading_strategy.update(i)
            invested_sums.append(trading_strategy.invested_sum)
        
        return invested_sums
    
    @staticmethod
    def simulate_print_and_plot(dates, trading_strategies, labels, log_scale=False):
        graph = InvestmentGrowthGraph('Different strategies over time', log_scale=log_scale)
        for i, trading_strategy in enumerate(trading_strategies):
            investment_values = StrategySimulator.simulate(trading_strategy)
            last_tax = (investment_values[-1] - trading_strategy.last_tax_buy_value) * 0.26375
            if hasattr(trading_strategy, 'losses'):
                last_tax -= min(last_tax, trading_strategy.losses)
            final_investment_value = investment_values[-1] - last_tax
            years = (dates[-1] - dates[0]).days / 365
            cagr = StrategySimulator.calculate_cagr(final_investment_value, years)
            max_drawdown = StrategySimulator.calculate_max_drawdown(investment_values)
            graph.add_curve(dates, investment_values, labels[i])
            print(labels[i] + ' growth: x' + str(floor2(final_investment_value)))
            print(labels[i] + ' CAGR: ' + factor_to_percentage(cagr))
            print(labels[i] + ' max drawdown: ' + factor_to_percentage(max_drawdown))
        
        graph.show()

    @staticmethod
    def calculate_cagr(growth, years):
        return pow(growth, 1 / years)

    @staticmethod
    def calculate_max_drawdown(values):
        return np.min(np.array([np.min(np.array(values[i:]) / values[i - 1]) for i in range(1, len(values))]))
