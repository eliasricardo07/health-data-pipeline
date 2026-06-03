import pandas as pd

def extract_pacientes(path: str) -> pd.DataFrame:
    """
    Extrai dados do sistema de pacientes.
    """

    return pd.read_csv(path)