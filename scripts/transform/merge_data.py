import pandas as pd

def merge_datasets(
    pacientes,
    exames,
    historico
):

    dataset = (
        pacientes.merge(
            exames,
            on="id",
            how="inner"
        )
        .merge(
            historico,
            on="id",
            how="inner"
        )
    )

    return dataset