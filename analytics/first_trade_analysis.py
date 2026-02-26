def analyze_first_entries(trades_df, daily_stop):
    """
    Analisa apenas a primeira entrada de cada dia e separa dias normais x dias de stop.
    """
    if trades_df.empty:
        return {
            "total_first_trades": 0,
            "normal_means": {},
            "stop_means": {},
            "stop_hour_distribution": {},
        }

    analysis_df = trades_df.copy()

    daily_result = analysis_df.groupby("date")["profit"].sum()
    stop_days = daily_result[daily_result <= -daily_stop].index
    analysis_df["stop_day"] = analysis_df["date"].isin(stop_days).astype(int)

    first_trades = analysis_df[analysis_df["trade_number_in_day"] == 1].copy()

    metric_cols = [
        "entry_adx",
        "entry_slope",
        "entry_ma_distance",
        "entry_vol_exp",
        "entry_bb_width",
    ]

    normal_first = first_trades[first_trades["stop_day"] == 0]
    stop_first = first_trades[first_trades["stop_day"] == 1]

    normal_means = normal_first[metric_cols].mean().to_dict() if not normal_first.empty else {}
    stop_means = stop_first[metric_cols].mean().to_dict() if not stop_first.empty else {}

    stop_hour_distribution = (
        stop_first["entry_hour"].value_counts().sort_index().to_dict()
        if not stop_first.empty
        else {}
    )

    return {
        "total_first_trades": len(first_trades),
        "normal_means": normal_means,
        "stop_means": stop_means,
        "stop_hour_distribution": stop_hour_distribution,
    }


def print_first_entry_analysis(analysis_result):
    print("\n====================")
    print("ANÁLISE DAS PRIMEIRAS ENTRADAS DO DIA")
    print("====================\n")

    print("Total primeiras entradas:", analysis_result["total_first_trades"])

    print("\n--- MÉDIAS PRIMEIRA ENTRADA (Dias Normais) ---")
    print(analysis_result["normal_means"])

    print("\n--- MÉDIAS PRIMEIRA ENTRADA (Dias STOP) ---")
    print(analysis_result["stop_means"])

    print("\n--- DISTRIBUIÇÃO DE HORÁRIOS (Dias STOP) ---")
    print(analysis_result["stop_hour_distribution"])
