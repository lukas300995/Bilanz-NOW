
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bilanz App", layout="wide")

# --- Dummy-Daten ---
dummy_data = {
    "Jahr": [2021, 2022, 2023],
    "Eigenkapital": [50000, 60000, 70000],
    "Fremdkapital": [75000, 80000, 85000],
    "Liquide Mittel": [20000, 25000, 30000],
    "kurzfr. Verbindlichkeiten": [15000, 20000, 25000],
    "kurzfr. Forderungen": [10000, 12000, 15000],
    "Anlagevermögen": [70000, 75000, 80000]
}

# --- Demo-Login ---
users = {
    "kunde": "kunde123",
    "berater": "berater123",
    "bank": "bank123"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

st.title("📊 Bilanz App (Demo)")

if not st.session_state.logged_in:
    st.subheader("Login")
    user = st.text_input("Benutzername")
    pw = st.text_input("Passwort", type="password")
    if st.button("Login"):
        if user in users and users[user] == pw:
            st.session_state.logged_in = True
            st.session_state.role = user
            st.success(f"Willkommen, {user}!")
        else:
            st.error("Ungültige Zugangsdaten.")
else:
    st.sidebar.write(f"👤 Eingeloggt als: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.experimental_rerun()

    role = st.session_state.role

    if role == "kunde":
        st.header("📂 Upload oder Dummy-Daten nutzen")
        choice = st.radio("Bitte wählen:", ["Dummy-Daten verwenden", "Eigene Datei hochladen"])

        if choice == "Dummy-Daten verwenden":
            df = pd.DataFrame(dummy_data)
            st.success("Dummy-Daten geladen.")
        else:
            uploaded = st.file_uploader("Bilanzdatei hochladen", type=["csv","xlsx","xml","pdf"])
            if uploaded:
                if uploaded.name.endswith(".csv"):
                    df = pd.read_csv(uploaded, sep=";")
                elif uploaded.name.endswith(".xlsx"):
                    df = pd.read_excel(uploaded)
                elif uploaded.name.endswith(".xml"):
                    st.info("XML-Datei wurde hochgeladen (Parsing folgt später).")
                    df = None
                elif uploaded.name.endswith(".pdf"):
                    st.info("PDF-Datei wurde hochgeladen (Auswertung folgt später).")
                    df = None
                else:
                    st.error("Dateiformat nicht unterstützt.")
                    df = None
                if df is not None:
                    st.success(f"Datei {uploaded.name} wurde geladen.")
            else:
                df = None

        if df is not None:
            st.subheader("📊 Originaldaten")
            st.dataframe(df)

            # Kennzahlen berechnen
            df_calc = pd.DataFrame()
            df_calc["Jahr"] = df["Jahr"]
            df_calc["Eigenkapitalquote"] = df["Eigenkapital"] / (df["Eigenkapital"] + df["Fremdkapital"])
            df_calc["Verschuldungsgrad"] = df["Fremdkapital"] / df["Eigenkapital"]
            df_calc["Liquidität 1. Grades"] = df["Liquide Mittel"] / df["kurzfr. Verbindlichkeiten"]
            df_calc["Liquidität 2. Grades"] = (df["Liquide Mittel"] + df["kurzfr. Forderungen"]) / df["kurzfr. Verbindlichkeiten"]
            df_calc["Liquidität 3. Grades"] = df_calc["Liquidität 2. Grades"]
            df_calc["Anlagendeckungsgrad II"] = df["Eigenkapital"] / df["Anlagevermögen"]

            st.subheader("📈 Kennzahlen")
            st.dataframe(df_calc.style.format("{:.2f}"))

            # Diagramm
            st.subheader("📉 Diagramm")
            fig, ax = plt.subplots()
            ax.plot(df_calc["Jahr"], df_calc["Eigenkapitalquote"], marker="o", label="Eigenkapitalquote")
            ax.plot(df_calc["Jahr"], df_calc["Verschuldungsgrad"], marker="o", label="Verschuldungsgrad")
            ax.set_xlabel("Jahr")
            ax.legend()
            st.pyplot(fig)

    elif role == "berater":
        st.header("👨‍💼 Steuerberater-Bereich")
        st.info("Hier erscheinen die Daten der freigegebenen Kunden.")
    elif role == "bank":
        st.header("🏦 Bank-Bereich")
        st.info("Hier erscheinen die Daten der freigegebenen Kunden.")
