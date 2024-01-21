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
    'certificate_fee': 0,
    'performance_fee': 0,
    'tax_at_rotation': True,
}

wikifolio_params = {
    'dates': dates,
    'values_open': values_open,
    'values_close': values_close,
    'certificate_fee': 0.0095,
    'performance_fee': 0.05,
    'tax_at_rotation': False,
}


broker_best_lev, broker_best_window_size = RotaryMAStrategy.calculate_best_params(
    **broker_params,
    spread=0.0015,
    ter=0.0075,
    window_sizes=np.arange(10, 300, 10),
    leverages=[3],
)

wikifolio_best_lev, wikifolio_best_window_size = RotaryMAStrategy.calculate_best_params(
    **wikifolio_params,
    spread=0.0015,
    ter=0.0075,
    window_sizes=np.arange(10, 300, 10),
    leverages=[3],
)

assert broker_best_lev == wikifolio_best_lev and broker_best_window_size == wikifolio_best_window_size

best_lev = broker_best_lev
best_window_size = broker_best_window_size

# best_lev = 3
# best_window_size = 200

print('Start date: ' + str(dates[0]))
print('End date: ' + str(dates[-1]))


print('Best params broker: ' + str(best_lev) + ', ' + str(best_window_size))

buy_and_hold_strategy = BuyAndHoldStrategy(
    dates=dates[best_window_size:],
    values_close=values_close[best_window_size:],
    ter=0.002,
    spread=0.0002,
    leverage=1.0,
)

rotary_strategy_broker_3x = RotaryMAStrategy(
    **broker_params,
    leverage=3,
    ter=0.0075,
    spread=0.0015,
    window_size=best_window_size,
)

rotary_strategy_wikifolio_3x = RotaryMAStrategy(
    **wikifolio_params,
    leverage=3,
    ter=0.0075,
    spread=0.0015,
    window_size=best_window_size,
)

rotary_strategy_broker_2x = RotaryMAStrategy(
    **broker_params,
    leverage=2,
    ter=0.006,
    spread=0.0015,
    window_size=best_window_size,
)

rotary_strategy_wikifolio_2x = RotaryMAStrategy(
    **wikifolio_params,
    leverage=2,
    ter=0.006,
    spread=0.0015,
    window_size=best_window_size,
)


StrategySimulator.simulate_print_and_plot(
    dates[best_window_size:],
    [
        buy_and_hold_strategy,
        rotary_strategy_broker_2x,
        rotary_strategy_wikifolio_2x,
        rotary_strategy_broker_3x,
        rotary_strategy_wikifolio_3x,
    ],
    [
        'Buy and Hold',
        'Rotary Broker 2x',
        'Rotary Wikifolio 2x',
        'Rotary Broker 3x',
        'Rotary Wikifolio 3x',
    ],
    log_scale=True,
)