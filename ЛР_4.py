import pandas as pd
from ta.momentum import RSIIndicator
import matplotlib.pyplot as plt
from binance.client import Client

# Створення клієнта для отримання даних з Binance
client = Client()

# Отримання історичних даних про криптовалютні свічки
k_lines = client.get_historical_klines(
    symbol="BTCUSDT",
    interval=Client.KLINE_INTERVAL_1MINUTE,
    start_str="1 day ago UTC"
)

# Визначення колонок для DataFrame
columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
           'quote_asset_volume', 'number_of_trades',
           'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']

# Створення DataFrame та конвертація даних
k_lines_df = pd.DataFrame(k_lines, columns=columns)
k_lines_df = k_lines_df.astype({'open': 'float', 'high': 'float', 'low': 'float',
                                'close': 'float', 'volume': 'float'})
k_lines_df['time'] = pd.to_datetime(k_lines_df['time'], unit='ms')

# Розрахунок показників RSI для різних періодів
periods = [14, 27, 100]
for period in periods:
    k_lines_df[f'RSI_{period}'] = RSIIndicator(k_lines_df['close'], window=period).rsi()

# Візуалізація ціни закриття та індикаторів RSI
fig, axes = plt.subplots(nrows=len(periods) + 1, ncols=1, figsize=(14, 10))

axes[0].plot(k_lines_df['time'], k_lines_df['close'], label='Close Price')
axes[0].set_title('Close Price')
axes[0].legend()

for i, period in enumerate(periods):
    axes[i+1].plot(k_lines_df['time'], k_lines_df[f'RSI_{period}'], label=f'RSI_{period}')
    axes[i+1].set_title(f'RSI_{period}')
    axes[i+1].legend()

plt.tight_layout()
plt.show()
