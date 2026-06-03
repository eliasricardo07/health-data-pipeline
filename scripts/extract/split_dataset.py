import pandas as pd

df = pd.read_csv(
    "data/raw/cardio_train.csv",
    sep=";"
)

pacientes = df[
    ["id", "age", "gender", "height", "weight"]
]

exames = df[
    ["id", "ap_hi", "ap_lo", "cholesterol", "gluc"]
]

historico = df[
    ["id", "smoke", "alco", "active", "cardio"]
]

pacientes.to_csv("data/processed/pacientes.csv", index=False)
exames.to_excel("data/processed/exames.xlsx", index=False)
historico.to_json("data/processed/historico.json", orient="records", lines=True)
 # orient="records" para criar um array de objetos JSON, e lines=True para escrever cada objeto em uma linha separada.  

print("Datasets separados e salvos com sucesso!")

print(pacientes.head())
print(exames.head())
print(historico.head())
