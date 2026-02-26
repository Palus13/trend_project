import os
import numpy as np
import pandas as pd

from config import get_default_parameters
from data.data_loader import load_csv_data
from strategy.indicators import calculate_indicators
from strategy.execution_engine import ExecutionEngine
from analytics.performance import calculate_performance


def main():

    print("=== BACKTEST INTRADAY COM META DIÁRIA ===")

    current_dir = os.path.dirname(os.path.abspath(__file__))

    data_path = os.path.join(
        current_dir,
        "data",
        "market_data",
        "Mini_Indice_5M_10A.csv"
    )

    market_df = load_csv_data(data_path)

    params = get_default_parameters()
    params["trend_confirmation"] = 11

    market_df = calculate_indicators(market_df, params)

    engine = ExecutionEngine(market_df, params)
    df_result, trades, daily_results = engine.run()

    trades_df = pd.DataFrame(trades)
    trades_df.to_csv("trade_analysis.csv", index=False)
    print("\nArquivo trade_analysis.csv gerado para análise.")

    results = calculate_performance(df_result, trades)

    print("\n=== RESULTADOS GERAIS ===")
    for key, value in results.items():
        print(f"{key}: {value}")

    print("\n=== ESTATÍSTICA DIÁRIA ===")

    days = len(daily_results)
    wins = len([d for d in daily_results if d >= params["daily_target"]])
    losses = len([d for d in daily_results if d <= -params["daily_stop"]])
    neutral = days - wins - losses

    avg_daily = np.mean(daily_results)

    print(f"Total de dias: {days}")
    print(f"Dias que bateram meta: {wins} ({round(wins/days*100,2)}%)")
    print(f"Dias que bateram stop: {losses} ({round(losses/days*100,2)}%)")
    print(f"Dias intermediários: {neutral} ({round(neutral/days*100,2)}%)")
    print(f"Média de lucro por dia: R$ {round(avg_daily,2)}")

    print("\n=== FIM ===")

    print("\n====================")
    print("ANÁLISE DAS PRIMEIRAS ENTRADAS DO DIA")
    print("====================\n")

    trades_df = pd.read_csv("trade_analysis.csv")

    # identificar dias de stop
    daily_result = trades_df.groupby("date")["profit"].sum()
    stop_days = daily_result[daily_result <= -params["daily_stop"]].index
    trades_df["stop_day"] = trades_df["date"].isin(stop_days).astype(int)

    # pegar apenas primeira entrada do dia
    first_trades = trades_df[trades_df["trade_number_in_day"] == 1].copy()

    print("Total primeiras entradas:", len(first_trades))

    print("\n--- MÉDIAS PRIMEIRA ENTRADA (Dias Normais) ---")
    normal_first = first_trades[first_trades["stop_day"] == 0]
    print(normal_first[[
        "entry_adx",
        "entry_slope",
        "entry_ma_distance",
        "entry_vol_exp",
        "entry_bb_width"
    ]].mean())

    print("\n--- MÉDIAS PRIMEIRA ENTRADA (Dias STOP) ---")
    stop_first = first_trades[first_trades["stop_day"] == 1]
    print(stop_first[[
        "entry_adx",
        "entry_slope",
        "entry_ma_distance",
        "entry_vol_exp",
        "entry_bb_width"
    ]].mean())

    print("\n--- DISTRIBUIÇÃO DE HORÁRIOS (Dias STOP) ---")
    print(stop_first["entry_hour"].value_counts().sort_index())

if __name__ == "__main__":
    main()