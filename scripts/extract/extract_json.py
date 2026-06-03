import pandas as pd

def extract_historico(path: str) -> pd.DataFrame:
    """
    Extrai histórico clínico.
    """

    return pd.read_json(
        path,
        orient="records",
        lines=True
    )