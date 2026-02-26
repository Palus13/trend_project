# performance.py

import numpy as np


def calculate_performance(df, trades):

    results = {}

    df["returns"] = df["equity"].pct_change()
    returns = df["returns"].dropna()

    total_return = (df["equity"].iloc[-1] / df["equity"].iloc[0]) - 1

    sharpe = 0
    if returns.std() != 0:
        sharpe = (np.sqrt(252) * returns.mean()) / returns.std()

    max_drawdown = (
        df["equity"] / df["equity"].cummax() - 1
    ).min()

    total_trades = len(trades)

    profits = [t["profit"] for t in trades]

    wins = [p for p in profits if p > 0]
    losses = [p for p in profits if p < 0]

    win_rate = (len(wins) / total_trades) * 100 if total_trades > 0 else 0

    avg_win = np.mean(wins) if wins else 0
    avg_loss = np.mean(losses) if losses else 0

    payoff = abs(avg_win / avg_loss) if avg_loss != 0 else 0
    expectancy = np.mean(profits) if total_trades > 0 else 0

    results["Total Return (%)"] = round(total_return * 100, 2)
    results["Sharpe Ratio"] = round(sharpe, 2)
    results["Max Drawdown (%)"] = round(max_drawdown * 100, 2)

    results["Total Trades"] = total_trades
    results["Win Rate (%)"] = round(win_rate, 2)
    results["Average Win (R$)"] = round(avg_win, 2)
    results["Average Loss (R$)"] = round(avg_loss, 2)
    results["Payoff"] = round(payoff, 2)
    results["Expectancy (R$)"] = round(expectancy, 2)

    return results