import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta


def get_historical_data(symbol, start_str, end_str):
    client = Client()
    # Використовуємо символ, інтервал і часовий діапазон для отримання історичних даних
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, start_str, end_str)

    # Створюємо DataFrame із отриманих даних, зберігаємо тільки необхідні стовпці
    columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    data = pd.DataFrame(klines, columns=columns + ['close_time', 'quote_asset_volume', 'number_of_trades',
                                                   'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
                                                   'ignore'])[columns]

    # Конвертуємо час із мілісекунд в звичайний формат і змінюємо типи даних для цін і обсягів
    data['time'] = pd.to_datetime(data['time'], unit='ms')
    data[columns[1:]] = data[columns[1:]].apply(pd.to_numeric, errors='coerce')

    return data


def calculate_RSI(df, periods=[14]):
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Ініціалізуємо DataFrame для RSI значень
    rsi_df = pd.DataFrame({'time': df['time']})

    for period in periods:
        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        rsi_df[f'RSI {period}'] = rsi

    return rsi_df


# Використання:
symbol = 'BTCUSDT'
yesterday = datetime.now() - timedelta(days=1)
start_str = yesterday.strftime('%Y-%m-%d %H:%M')
end_str = (yesterday + timedelta(days=1)).strftime('%Y-%m-%d %H:%M')

data = get_historical_data(symbol, start_str, end_str)
rsi_data = calculate_RSI(data, [14, 27, 100])

print(rsi_data)
