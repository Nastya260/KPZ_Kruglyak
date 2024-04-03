import datetime
import pandas as pd
from binance.client import Client
from pandas_ta import rsi, cci, macd


def interpret_signals(row):
    """Функція інтерпретації сигналів для рядка даних."""
    signals = {"RSI": "Невідомий", "CCI": "Невідомий", "MACD": "Невідомий"}

    # RSI
    if row["RSI"] > 70:
        signals["RSI"] = "Ціна буде рости"
    elif row["RSI"] > 30:
        signals["RSI"] = "Невідомий"
    else:
        signals["RSI"] = "Ціна впаде"

    # CCI
    if row["CCI"] > 100:
        signals["CCI"] = "Невідомий"
    elif row["CCI"] > -100:
        signals["CCI"] = "Ціна буде рости"
    else:
        signals["CCI"] = "Ціна впаде"

    # MACD
    if pd.notna(row['MACD_prev']) and pd.notna(row['MACDs_prev']):
        if row['MACD'] > row['MACDs'] and row['MACD_prev'] < row['MACDs_prev']:
            signals["MACD"] = "Ціна буде рости"
        elif row['MACD'] < row['MACDs'] and row['MACD_prev'] > row['MACDs_prev']:
            signals["MACD"] = "Ціна впаде"

    # Вибір кінцевого прогнозу
    final_prediction = next((signal for signal in signals.values() if signal != "Невідомий"), "Невідомий")
    return final_prediction


def main():
    # Встановлення дат
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    try:
        client = Client()
        k_lines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, yesterday, today)

        # Створення DataFrame
        columns = ['time', 'open', 'high', 'low', 'close']
        k_lines_df = pd.DataFrame(k_lines, columns=columns + ['extra'] * (len(k_lines[0]) - 5))
        k_lines_df = k_lines_df[columns].astype({'open': 'float', 'high': 'float', 'low': 'float', 'close': 'float'})
        k_lines_df['time'] = pd.to_datetime(k_lines_df['time'], unit='ms')

        # Розрахунок показників
        k_lines_df['RSI'] = rsi(k_lines_df['close'])
        k_lines_df['CCI'] = cci(k_lines_df['high'], k_lines_df['low'], k_lines_df['close'])
        macd_values = macd(k_lines_df['close'])
        k_lines_df = pd.concat([k_lines_df, macd_values], axis=1)

        k_lines_df[['MACD', 'MACDh', 'MACDs']] = macd_values
        k_lines_df[['MACD_prev', 'MACDs_prev']] = k_lines_df[['MACD', 'MACDs']].shift(1)
        k_lines_df['Prediction'] = k_lines_df.apply(interpret_signals, axis=1)

        k_lines_df[['time', 'RSI', 'CCI', 'MACD', 'MACDs', 'Prediction']].dropna().to_csv('prediction.csv', index=False)
        print("Prediction saved to prediction.csv")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
