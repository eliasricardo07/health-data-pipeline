from scripts.extract.extract_csv import extract_pacientes
from scripts.extract.extract_excel import extract_exames
from scripts.extract.extract_json import extract_historico

pacientes = extract_pacientes(
    "data/processed/pacientes.csv"
)

exames = extract_exames(
    "data/processed/exames.xlsx"
)

historico = extract_historico(
    "data/processed/historico.json"
)

print(pacientes.head())
print(exames.head())
print(historico.head())

# Aqui, o código importa as funções de extração dos arquivos CSV, Excel e JSON, e as utiliza para ler os dados processados.
#  Em seguida, imprime as primeiras linhas de cada DataFrame para verificar se os dados foram carregados corretamente. 

print("\n Informações de Idade Convertida: \n")

#após a execução eu consegui identificar que a coluna age estava em dias, então dividi por 365 para converter para anos.

pacientes["age"] = round(pacientes["age"] / 365, 0).astype(int) 
#aqui usei o round para arredondar a idade para o número inteiro mais 
#próximo, e depois converti para int para garantir que a coluna seja do tipo inteiro.  

print(pacientes.head())

#após rodar novamente, consegui identificar novos pontos importantes onde eu devo corrigir os dados;
print(exames["ap_hi"].describe())
print(exames["ap_lo"].describe())

print(
    exames["cholesterol"]
    .value_counts()
)

print(
    exames["gluc"]
    .value_counts()
)

print(
    pacientes["gender"]
    .value_counts()
)
print("\n Verificando valores anômalos em ap_hi e ap_lo: \n")

print(
    exames[
        (exames["ap_hi"] <= 0)
        |
        (exames["ap_hi"] > 300)
    ]
    .head(10)
)

print(
    exames[
        (exames["ap_lo"] <= 0)
        |
        (exames["ap_lo"] > 200)
    ]
    .head(10)
)

print(
    exames[
        exames["ap_hi"] < exames["ap_lo"]
    ]
    .shape
)

#aqui nessas análises, podemos identificar dados incorretos, como pressão arterial sistólica (ap_hi) menor que a pressão arterial 
# diastólica (ap_lo), ou valores de pressão arterial fora dos limites fisiológicos plausíveis.  
# ao total 1234 pacientes com esses erros nos seus dados de preossão arterial.

# como também descobrimos regras de negócio como:
# A pressão sistólica não pode ser negativa ou zero. 
# A pressão diastólica não pode ser negativa ou zero. 
# A pressão sistólica deve ser maior que a diastólica.

# Com base nessas regras, podemos criar uma nova coluna "registro_valido" para indicar se cada registro de exame é válido ou não.

exames["registro_valido"] = (
    (exames["ap_hi"] > 0)
    & (exames["ap_lo"] > 0)
    & (exames["ap_hi"] > exames["ap_lo"])
    & (exames["ap_hi"] <= 300)
    & (exames["ap_lo"] <= 200)
)

print(exames.head(10))

# agora vamos trabalhar com calculos de IMC e identificar pacientes com obesidade, que é um fator de risco importante para doenças cardiovasculares.    
# O IMC é calculado como peso (kg) dividido pela altura (m) ao quadrado.

pacientes["imc"] =  round(
    pacientes["weight"]
    /
    (pacientes["height"] / 100) ** 2, 2
    )

def classificar_imc(imc):

    if imc < 18.5:
        return "Baixo peso"

    elif imc < 25:
        return "Normal"

    elif imc < 30:
        return "Sobrepeso"

    else:
        return "Obesidade"
    
pacientes["classificacao_imc"] = (
    pacientes["imc"]
    .apply(classificar_imc)
)

print("\n Classificação do IMC: \n")

print(pacientes[["id", "weight", "height", "imc", "classificacao_imc"]].head(10))

print("\n Anáilse de registros com pressão arterial anômala: \n")

print(
    exames["registro_valido"].value_counts()
)

exames_validos = exames[
    exames["registro_valido"]
].copy()

#após mais uma análise descobrimos que tem pesos e alturas anômalas, como peso de 0 kg ou altura de 0 cm, o que é impossível.
#então vamos criar uma nova coluna "dados_validos" para indicar se os dados de peso e altura são válidos ou não,
# usando regras de negócio como:
# 120 cm <= altura <= 220 cm --Altura muito improvável para um adulto.
# 30 kg <= peso <= 180 kg --Peso muito improvável para um adulto.

pacientes["registro_antropometrico_valido"] = (
    (pacientes["height"] >= 120)
    & (pacientes["height"] <= 220)
    & (pacientes["weight"] >= 30)
    & (pacientes["weight"] <= 180)
)

print(
    pacientes["registro_antropometrico_valido"]
    .value_counts()
)

total = len(pacientes)

invalidos = (
    pacientes["registro_antropometrico_valido"] == False
).sum()

print(f"Total: {total}")
print(f"Inválidos: {invalidos}")
print(f"Percentual inválido: {invalidos/total:.2%}")

print("\n Exibindo registros com dados antropométricos inválidos: \n")

print(
    pacientes[
        pacientes["registro_antropometrico_valido"] == False
    ]
    .head(20)
)

print(
    pacientes.sort_values(
        by="imc",
        ascending=False
    )
    .head(20)
)

print(pacientes["imc"].describe())


# descobri que temos registros na coluna IMC inválidos, que ajuda a identificar que a altura foi registrada errada.
pacientes["registro_imc_valido"] = (
    (pacientes["imc"] >= 10)
    &
    (pacientes["imc"] <= 70)
)

print(
    pacientes["registro_imc_valido"]
    .value_counts()
)


from scripts.transform.merge_data import merge_datasets

dataset = merge_datasets(
    pacientes,
    exames,
    historico
)

print("\n Dataset final após merge: \n")
print(dataset.head(10))
print(dataset.info())
print(dataset.shape)

dataset["registro_geral_valido"] = (
    dataset["registro_antropometrico_valido"]
    &
    dataset["registro_imc_valido"]
    &
    dataset["registro_valido"]
)

print(
    dataset["registro_geral_valido"]
    .value_counts()
)

print(dataset.isnull().sum())

dataset_valido = dataset[
    dataset["registro_geral_valido"]
].copy()

dataset_invalido = dataset[
    ~dataset["registro_geral_valido"]
].copy()

dataset_valido.to_csv(
    "data/processed/dataset_final.csv",
    index=False
)

from database.load_sqlite import load_to_sqlite

print(dataset_valido.shape)

print("Iniciando carga no SQLite...")

load_to_sqlite(
    dataset_valido,
    "database/health_data.db",
    "pacientes"
)

print("Dados carregados no SQLite com sucesso!")