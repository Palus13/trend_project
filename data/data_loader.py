# data_loader.py

import pandas as pd


def load_csv_data(file_path):

    # Lê CSV separado por TAB
    df = pd.read_csv(file_path, sep="\t")

    # Padroniza nomes removendo < >
    df.columns = [col.replace("<", "").replace(">", "") for col in df.columns]

    # Converte data + hora
    df["datetime"] = pd.to_datetime(df["DATE"] + " " + df["TIME"])
    df = df.set_index("datetime")

    # Renomeia colunas para padrão
    df.rename(columns={
        "OPEN": "open",
        "HIGH": "high",
        "LOW": "low",
        "CLOSE": "close",
        "VOL": "volume"
    }, inplace=True)

    # Mantém apenas colunas importantes
    df = df[["open", "high", "low", "close", "volume"]]

    df = df.sort_index()

    print("Colunas padronizadas:", df.columns)

    return df