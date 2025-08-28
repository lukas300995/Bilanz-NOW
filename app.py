
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bilanz App Extended", layout="wide")

# --- Dummy-Daten erweitert ---
dummy_data = {
    "Jahr": [2021, 2022, 2023],
    "Eigenkapital": [50000, 60000, 70000],
    "Fremdkapital": [75000, 80000, 85000],
    "Liquide Mittel": [20000, 25000, 30000],
    "kurzfr. Verbindlichkeiten": [15000, 20000, 25000],
    "kurzfr. Forderungen": [10000, 12000, 15000],
    "Anlagevermögen": [70000, 75000, 80000],
    "langfr. Fremdkapital": [30000, 35000, 40000],
    "Vorräte": [20000, 21000, 22000],
    "unfertige Erzeugnisse": [5000, 5500, 6000],
    "fertige Erzeugnisse": [7000, 7500, 8000],
    "Materialaufwand": [40000, 42000, 45000],
    "Herstellungskosten": [50000, 52000, 54000],
    "Umsatz": [150000, 160000, 170000],
    "Jahresüberschuss": [10000, 12000, 15000],
    "EBIT": [15000, 18000, 20000],
    "EBITDA": [20000, 23000, 25000],
    "Rohertrag": [60000, 65000, 70000],
    "Personalaufwand": [30000, 32000, 34000],
    "Mitarbeiter": [10, 11, 12],
    "kumulierte Abschreibungen": [20000, 25000, 30000],
    "Anschaffungswerte AV": [90000, 95000, 100000],
    "Firmenwert": [5000, 5500, 6000],
    "Finanzverbindlichkeiten": [40000, 42000, 45000],
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

st.title("📊 Bilanz App – Erweiterte Kennzahlen")

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

            # Basiswerte
            gesamtkapital = df["Eigenkapital"] + df["Fremdkapital"]

            # Kennzahlen
            df_calc = pd.DataFrame()
            df_calc["Jahr"] = df["Jahr"]
            df_calc["Eigenkapitalquote"] = df["Eigenkapital"] / gesamtkapital
            df_calc["Verschuldungsgrad"] = df["Fremdkapital"] / df["Eigenkapital"]
            df_calc["Eigenkapital % Anlagevermögen"] = df["Eigenkapital"] / df["Anlagevermögen"]
            df_calc["Anlagendeckung I"] = df["Eigenkapital"] / df["Anlagevermögen"]
            df_calc["Anlagendeckung II"] = (df["Eigenkapital"] + df["langfr. Fremdkapital"]) / df["Anlagevermögen"]
            df_calc["Lagerdauer Vorräte"] = df["Vorräte"] / df["Materialaufwand"] * 365
            df_calc["Lagerdauer Erzeugnisse"] = (df["unfertige Erzeugnisse"] + df["fertige Erzeugnisse"]) / df["Herstellungskosten"] * 365
            df_calc["Debitorenziel"] = df["kurzfr. Forderungen"] / df["Umsatz"] * 365
            df_calc["Kreditorenziel"] = df["kurzfr. Verbindlichkeiten"] / df["Materialaufwand"] * 365
            df_calc["Kapitalumschlag"] = df["Umsatz"] / gesamtkapital
            df_calc["Umsatzrentabilität"] = df["Jahresüberschuss"] / df["Umsatz"]
            df_calc["Eigenkapitalrentabilität"] = df["Jahresüberschuss"] / df["Eigenkapital"]
            df_calc["Gesamtkapitalrentabilität"] = df["EBIT"] / gesamtkapital
            df_calc["Anlagenabnutzungsgrad"] = df["kumulierte Abschreibungen"] / df["Anschaffungswerte AV"]
            df_calc["Firmenwert % EK"] = df["Firmenwert"] / df["Eigenkapital"]
            df_calc["Net Gearing"] = (df["Finanzverbindlichkeiten"] - df["Liquide Mittel"]) / df["Eigenkapital"]
            df_calc["Nettoverschuldung/EBITDA"] = (df["Finanzverbindlichkeiten"] - df["Liquide Mittel"]) / df["EBITDA"]
            df_calc["Working Capital Ratio"] = (df["Vorräte"] + df["kurzfr. Forderungen"] - df["kurzfr. Verbindlichkeiten"]) / df["Umsatz"]
            df_calc["Produktivität"] = df["Rohertrag"] / df["Personalaufwand"]
            df_calc["Gross Operating Profit"] = df["EBITDA"]
            df_calc["Betriebsleistung/Mitarbeiter"] = df["Umsatz"] / df["Mitarbeiter"]
            df_calc["Personalaufwand/Mitarbeiter"] = df["Personalaufwand"] / df["Mitarbeiter"]

            st.subheader("📈 Kennzahlen (erweitert)")
            st.dataframe(df_calc.style.format("{:.2f}"))

            # Diagramm
            st.subheader("📉 Diagramm (Basiskennzahlen)")
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
