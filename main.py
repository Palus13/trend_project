import numpy as np

from app.backtest_runner import run_backtest
from analytics.first_trade_analysis import analyze_first_entries, print_first_entry_analysis


def main():
    print("=== BACKTEST INTRADAY COM META DIÁRIA ===")

    output = run_backtest()

    trades_df = output["trades_df"]
    daily_results = output["daily_results"]
    results = output["performance"]
    params = output["params"]

    # Persistência opcional para análise externa
    trades_df.to_csv("trade_analysis.csv", index=False)
    print("\nArquivo trade_analysis.csv gerado para análise.")

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

    first_trade_stats = analyze_first_entries(trades_df, params["daily_stop"])
    print_first_entry_analysis(first_trade_stats)


if __name__ == "__main__":
    main()
