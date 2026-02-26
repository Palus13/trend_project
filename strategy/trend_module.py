# trend_module.py


def detect_trend(df, idx, params):
    """
    Detecta tendência com base na confirmação de cruzamento
    entre MME e MMA por N candles consecutivos.
    """

    confirmation = params["trend_confirmation"]

    # Evita erro no início do dataframe
    if idx < confirmation:
        return 0

    uptrend = True
    downtrend = True

    for i in range(confirmation):

        if df["MME"].iloc[idx - i] <= df["MMA"].iloc[idx - i]:
            uptrend = False

        if df["MME"].iloc[idx - i] >= df["MMA"].iloc[idx - i]:
            downtrend = False

    if uptrend:
        return 1

    elif downtrend:
        return -1

    else:
        return 0