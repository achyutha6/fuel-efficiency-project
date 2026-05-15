import streamlit as st

st.title("🚘 Car Comparison")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Car A")
    mpg1 = st.number_input(
        "MPG A",
        value=25.0
    )

    fuel1 = st.number_input(
        "Fuel Cost A",
        value=5000.0
    )

with col2:
    st.subheader("Car B")

    mpg2 = st.number_input(
        "MPG B",
        value=30.0
    )

    fuel2 = st.number_input(
        "Fuel Cost B",
        value=4000.0
    )

st.write("### Comparison Result")

if mpg1 > mpg2:
    st.success("Car A has better MPG")
else:
    st.success("Car B has better MPG")

if fuel1 < fuel2:
    st.success("Car A saves more fuel cost")
else:
    st.success("Car B saves more fuel cost")