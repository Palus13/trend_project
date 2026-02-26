# filters_module.py


def check_filters(df, idx, params):

    row = df.iloc[idx]

    # =============================
    # Filtro de Força
    # =============================
    if params["use_strength_filter"]:
        if row["MME_slope"] < params["min_slope"]:
            return False
        if row["MA_distance"] < params["min_ma_distance"]:
            return False

    # =============================
    # Filtro de Volatilidade
    # =============================
    if params["use_volatility_filter"]:
        if row["vol_expansion"] < params["min_volatility_expansion"]:
            return False

    # =============================
    # ADX
    # =============================
    if params["use_adx_filter"]:
        if row["ADX"] < params["min_adx"]:
            return False

    # =============================
    # Bollinger Squeeze
    # =============================
    if params["use_squeeze_filter"]:
        if row["bb_width"] > 0.05:
            return False

    return True