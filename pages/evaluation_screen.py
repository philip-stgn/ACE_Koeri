import streamlit as st

st.title("Evaluation Screen")
# Large text area
st.markdown("<h1 style='text-align: center;'>Final Score</h1>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="
        background-color:#90D5FF;
        border-radius:20px;
        padding:20px;
        height:200px;
        display:flex;
        justify-content:center;
        align-items:center;
        font-size:60px;
        text-align:center;
    ">
        {"<span font-weight:bold;> 6/10 </span>"}    
    </div>
    """,
    unsafe_allow_html=True
)

#st.text("Einfacher Text")
#st.markdown("**Fett**, *kursiv*, `Code`")

#st.header("🔘 Auswahl-Elemente")
#option = st.selectbox("Wähle eine Option", ["Option A", "Option B", "Option C"])
#multi_option = st.multiselect("Mehrfachauswahl", ["A", "B", "C", "D"])

#st.header("📸 Bilder")
#st.image("https://placekitten.com/300/200", caption="Ein süßes Kätzchen")

st.header("Analyse")
import pandas as pd
import numpy as np

data = pd.DataFrame(np.random.randn(10, 2), columns=["A", "B"])
st.line_chart(data)
st.bar_chart(data)
