import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Vehicle Dashboard")

df = pd.read_csv("auto-mpg.csv")

fig1 = px.histogram(
    df,
    x="mpg",
    title="MPG Distribution"
)

st.plotly_chart(fig1)

fig2 = px.scatter(
    df,
    x="horsepower",
    y="mpg",
    color="origin",
    title="Horsepower vs MPG"
)

st.plotly_chart(fig2)