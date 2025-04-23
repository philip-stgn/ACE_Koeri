import streamlit as st
import time

#pip install streamlit
#streamlit run ui_mockup.py
#
#

# st.title("🧱 Streamlit UI-Baukasten")
st.title("Melgmir Unicorn finder")

st.header("Uplodad your pitchdeck ...")
file = st.file_uploader("upload a file", type=["txt", "csv", "jpg", "png"])

if st.button("Analyse pitchdeck ..."):
    st.success(" --- Insert sending pitchdeck and analysing ist ---")
    with st.spinner("Bitte warten..."):
        time.sleep(3)  # Simuliere Ladevorgang
st.success("Fertig geladen!")
    

st.header("📋 Text-Elemente")
st.text("Einfacher Text")
st.markdown("**Fett**, *kursiv*, `Code`")
st.code("print('Hallo Welt')", language='python')

st.header("🧑‍💻 Eingabeelemente")
name = st.text_input("Name")
email = st.text_input("E-Mail")
password = st.text_input("Passwort", type="password")
nachricht = st.text_area("Nachricht")

st.header("🔘 Auswahl-Elemente")
option = st.selectbox("Wähle eine Option", ["Option A", "Option B", "Option C"])
multi_option = st.multiselect("Mehrfachauswahl", ["A", "B", "C", "D"])
check = st.checkbox("Ich stimme zu")
radio = st.radio("Wähle eine Farbe", ["Rot", "Grün", "Blau"])
slider = st.slider("Wähle eine Zahl", 0, 100, 50)
range_slider = st.slider("Wähle einen Bereich", 0, 100, (25, 75))

st.header("📅 Datum & Zeit")
datum = st.date_input("Wähle ein Datum")
zeit = st.time_input("Wähle eine Uhrzeit")

st.header("📁 Dateien")
file = st.file_uploader("Lade eine Datei hoch", type=["txt", "csv", "jpg", "png"])

st.header("📸 Bilder")
st.image("https://placekitten.com/300/200", caption="Ein süßes Kätzchen")

st.header("🎛️ Buttons & Aktionen")
if st.button("Klick mich!"):
    st.success("Button wurde geklickt!")

if st.button("Zeige Eingaben"):
    st.info(f"Name: {name}, E-Mail: {email}, Option: {option}")

st.header("📊 Diagramme")
import pandas as pd
import numpy as np

data = pd.DataFrame(np.random.randn(10, 2), columns=["A", "B"])
st.line_chart(data)
st.bar_chart(data)

st.header("🔍 Fortschritt und Status")
st.progress(70)
st.spinner("Wird geladen...")
st.balloons()
