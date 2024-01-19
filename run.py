import pandas as pd
import numpy as np
from trading_strategies import BuyAndHoldStrategy, RotaryMAStrategy
from strategy_simulator import StrategySimulator
from visualization import InvestmentGrowthGraph



index_data = pd.read_csv('data/NDX.INDX.csv', sep=',', decimal='.')
index_data['date'] = pd.to_datetime(index_data['date'], utc=True)

dates = index_data['date'].tolist()
values_open = index_data['open'].tolist()
values_close = index_data['close'].tolist()

broker_params = {
    'dates': dates,
    'values_open': values_open,
    'values_close': values_close,
    'ter': 0.0075,
    'certificate_fee': 0,
    'spread': 0.001,
    'performance_fee': 0,
    'tax_at_rotation': True,
}

wikifolio_params = {
    'dates': dates,
    'values_open': values_open,
    'values_close': values_close,
    'ter': 0.0075,
    'certificate_fee': 0.0095,
    'spread': 0.001,
    'performance_fee': 0.05,
    'tax_at_rotation': False,
}


broker_best_lev, broker_best_window_size = RotaryMAStrategy.calculate_best_params(
    **broker_params,
    window_sizes=np.arange(10, 300, 10),
    leverages=[3],
)

wikifolio_best_lev, wikifolio_best_window_size = RotaryMAStrategy.calculate_best_params(
    **wikifolio_params,
    window_sizes=np.arange(10, 300, 10),
    leverages=[3],
)

assert broker_best_lev == wikifolio_best_lev and broker_best_window_size == wikifolio_best_window_size

best_lev = broker_best_lev
best_window_size = broker_best_window_size

print('Start date: ' + str(dates[0]))
print('End date: ' + str(dates[-1]))


print('Best params broker: ' + str(best_lev) + ', ' + str(best_window_size))

buy_and_hold_strategy = BuyAndHoldStrategy(
    dates=dates[best_window_size:],
    values_close=values_close[best_window_size:],
    leverage=1.0,
    ter=0.002,
)

rotary_strategy_wikifolio = RotaryMAStrategy(
    **wikifolio_params,
    leverage=best_lev,
    window_size=best_window_size,
)

rotary_strategy_broker = RotaryMAStrategy(
    **broker_params,
    leverage=best_lev,
    window_size=best_window_size,
)



StrategySimulator.simulate_print_and_plot(
    dates[best_window_size:],
    [
        buy_and_hold_strategy,
        rotary_strategy_wikifolio,
        rotary_strategy_broker,
    ],
    [
        'Buy and Hold',
        'Rotary Wikifolio',
        'Rotary Broker',
    ],
    log_scale=True,
)