import os
import pandas as pd

from config import get_default_parameters
from data.data_loader import load_csv_data
from strategy.indicators import calculate_indicators
from strategy.execution_engine import ExecutionEngine
from analytics.performance import calculate_performance


def get_default_data_path():
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(current_dir, "data", "market_data", "Mini_Indice_5M_10A.csv")


def run_backtest(data_path=None, custom_params=None):
    """
    Executa o pipeline completo de backtest e retorna todos os artefatos em memória.

    Returns:
        dict com:
            - df_result: dataframe com curva de equity
            - trades: lista de trades
            - trades_df: dataframe de trades
            - daily_results: lista de resultado diário
            - performance: métricas agregadas
            - params: parâmetros finais utilizados
    """
    final_data_path = data_path or get_default_data_path()

    params = get_default_parameters()
    if custom_params:
        params.update(custom_params)

    market_df = load_csv_data(final_data_path)
    market_df = calculate_indicators(market_df, params)

    engine = ExecutionEngine(market_df, params)
    df_result, trades, daily_results = engine.run()

    trades_df = pd.DataFrame(trades)
    performance = calculate_performance(df_result, trades)

    return {
        "df_result": df_result,
        "trades": trades,
        "trades_df": trades_df,
        "daily_results": daily_results,
        "performance": performance,
        "params": params,
    }
