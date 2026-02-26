# config.py

def get_default_parameters():
    return {

        # CAPITAL
        "initial_capital": 100000,

        # =============================
        # CONFIRMAÇÃO ESTRUTURAL
        # =============================
        "trend_confirmation": 5,

        # =============================
        # FILTROS (DESLIGADOS)
        # =============================
        "use_strength_filter": False,
        "use_volatility_filter": False,
        "use_adx_filter": True,
        "use_squeeze_filter": False,
        "use_intraday_regime_filter": False,

        # =============================
        # PARÂMETROS DOS FILTROS
        # =============================

        # Força (inclinação mínima)
        "min_slope": 0,

        # Distância mínima entre médias
        "min_ma_distance": 0,

        # Volatilidade mínima (expansão)
        "min_volatility_expansion": 0,

        # ADX mínimo
        "min_adx": 20,

        # Bollinger squeeze
        "bb_period": 20,
        "bb_std": 2,

        # VWAP regime
        "use_vwap_filter": False,

        # =============================
        # MÉDIAS
        # =============================
        "MMA_period": 21,
        "MME_period": 9,

        # =============================
        # MACD / STDDEV
        # =============================
        "MACD_fast": 21,
        "MACD_slow": 9,
        "MACD_signal": 5,
        "StdDev_period": 9,

        # =============================
        # MODELO FINANCEIRO WIN
        # =============================
        "contracts": 1,
        "tick_value": 5,

        # =============================
        # CONTROLE DIÁRIO
        # =============================
        "daily_target": 300,
        "daily_stop": 500,
    }