# indicators.py

import pandas as pd
import numpy as np


def calculate_indicators(df, params):

    df = df.copy()

    # =============================
    # MÉDIAS
    # =============================
    df["MMA"] = df["close"].rolling(params["MMA_period"]).mean()
    df["MME"] = df["close"].ewm(span=params["MME_period"], adjust=False).mean()

    # Inclinação da MME
    df["MME_slope"] = df["MME"].diff()

    # Distância entre médias
    df["MA_distance"] = abs(df["MME"] - df["MMA"])

    # =============================
    # VOLATILIDADE EXPANSÃO
    # =============================
    df["rolling_range"] = df["high"] - df["low"]
    df["range_mean"] = df["rolling_range"].rolling(20).mean()
    df["vol_expansion"] = df["rolling_range"] / df["range_mean"]

    # =============================
    # ADX CORRETO (WILDER)
    # =============================

    high = df["high"]
    low = df["low"]
    close = df["close"]

    plus_dm = high.diff()
    minus_dm = -low.diff()

    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm < 0] = 0

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    period = 14

    atr = tr.ewm(alpha=1 / period, adjust=False).mean()
    plus_di = 100 * (plus_dm.ewm(alpha=1 / period, adjust=False).mean() / atr)
    minus_di = 100 * (minus_dm.ewm(alpha=1 / period, adjust=False).mean() / atr)

    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    df["ADX"] = dx.ewm(alpha=1 / period, adjust=False).mean()

    # =============================
    # BOLLINGER SQUEEZE
    # =============================
    bb_mid = df["close"].rolling(params["bb_period"]).mean()
    bb_std = df["close"].rolling(params["bb_period"]).std()

    df["bb_width"] = (bb_std * params["bb_std"]) / bb_mid

    return df