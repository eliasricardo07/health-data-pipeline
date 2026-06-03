import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

conn = sqlite3.connect("database/health_data.db")
df = pd.read_sql_query("SELECT * FROM pacientes", conn)


print("\n Dados no SQLite: \n")
print(df.head(10))

st.title("Dashboard de Pacientes")
st.metric("Total de Pacientes", len(df))

st.metric(
    "% Cardiopatas", 
    round(df["cardio"].mean() * 100, 2)
)

fig = px.histogram(
    df,
    x="imc",
    nbins=30
)

st.plotly_chart(fig)


fig2 = px.bar(
    df.groupby(
        "classificacao_imc"
    )["cardio"]
    .mean()
    .reset_index(),
    x="classificacao_imc",
    y="cardio"
)

st.plotly_chart(fig2)

df["faixa_etaria"] = pd.cut(
    df["age"],
    bins=[0,30,40,50,60,100],
    labels=[
        "Até 30",
        "31-40",
        "41-50",
        "51-60",
        "60+"
    ]
)

fig = px.bar(
    df.groupby(
        "faixa_etaria"
    )["cardio"]
    .mean()
    .reset_index(),
    x="faixa_etaria",
    y="cardio"
)

st.plotly_chart(fig)

fig = px.pie(
    df,
    names="gender",
    color="cardio"
)

st.plotly_chart(fig)

sexo = st.selectbox(
    "Sexo",
    ["Todos", 1, 2]
)