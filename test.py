import streamlit as st
n_cols = st.sidebar.selectbox("จำนวนเสา", [2, 3, 4])

columns = []
for i in range(n_cols):
    with st.sidebar.expander(f"ข้อมูลเสา C{i+1}", expanded=True):
        name = st.text_input(f"ชื่อเสา {i+1}", value=f"C{i+1}", key=f"name_{i}")
        x = st.number_input(f"x{i+1} (m)", value=0.0, key=f"x_{i}")
        y = st.number_input(f"y{i+1} (m)", value=0.0, key=f"y_{i}")
        P = st.number_input(f"P{i+1} (kN)", value=500.0, min_value=0.0, key=f"P_{i}")
        Mx = st.number_input(f"Mx{i+1} (kN-m)", value=0.0, key=f"Mx_{i}")
        My = st.number_input(f"My{i+1} (kN-m)", value=0.0, key=f"My_{i}")

        columns.append({
            "Column": name,
            "x": x,
            "y": y,
            "P": P,
            "Mx": Mx,
            "My": My
        })
