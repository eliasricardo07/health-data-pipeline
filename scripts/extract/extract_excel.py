import pandas as pd

def extract_exames(path: str) -> pd.DataFrame:
    """
    Extrai dados do sistema laboratorial.
    """

    return pd.read_excel(path)