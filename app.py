import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="FitKompas", layout="centered")

# Laad logo
logo = Image.open("logo.png")
st.image(logo, width=200)

st.title("FitKompas Vragenlijst")

# Laad de vragenlijst
@st.cache_data
def load_data():
    import numpy as np
    df = pd.read_excel("vragenlijst.xlsx")
    df = df.dropna(subset=["Unnamed: 1"])
    df = df.rename(columns={
        "Unnamed: 1": "vraag",
        "x-as": "x_as",
        "y-as": "y_as",
        "Unnamed: 4": "richting",
        "Unnamed: 6": "thema"
    df = df[df['vraag'].notna() & (df['vraag'] != '')]
    df = df.replace({np.nan: None})
    })
    return df

df = load_data()

antwoorden = []
st.write("Beantwoord de onderstaande vragen:")

        f"{int(row['# vraag'])}. {row['vraag']} - Thema: {row['thema']}",
    antwoord = st.radio(
        f"{int(row['# vraag'])}. {row['vraag']}  -  Thema: {row['thema']}",
**Thema:** {row['thema']}",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: {
            5: "Helemaal mee eens",
            4: "Mee eens",
            3: "Neutraal",
            2: "Mee oneens",
            1: "Helemaal niet mee eens"
        }[x],
        key=f"vraag_{i}"
    )
    antwoorden.append(antwoord)

if st.button("Verstuur"):
    df["antwoord"] = antwoorden

    # Score op x- en y-as berekenen
    x_score = df[df["x_as"].notna()]["antwoord"].sum()
    y_score = df[df["y_as"].notna()]["antwoord"].sum()

    # Normaliseren
    max_x = len(df[df["x_as"].notna()]) * 5
    max_y = len(df[df["y_as"].notna()]) * 5
    x_norm = round((x_score / max_x) * 100)
    y_norm = round((y_score / max_y) * 100)

    st.subheader("📊 Jouw resultaat")
    st.markdown(f"**Actief-score (x-as):** {x_norm}/100")
    st.markdown(f"**Motivatie-score (y-as):** {y_norm}/100")

    # Bepaal kwadrant
    if x_norm < 50 and y_norm < 50:
        kwadrant = "Niet actief & niet gemotiveerd"
        kleur = "🔴"
    elif x_norm < 50 and y_norm >= 50:
        kwadrant = "Niet actief & wél gemotiveerd"
        kleur = "🟡"
    elif x_norm >= 50 and y_norm < 50:
        kwadrant = "Wél actief & niet gemotiveerd"
        kleur = "🟠"
    else:
        kwadrant = "Wél actief & wél gemotiveerd"
        kleur = "🟢"

    st.markdown(f"**Je valt in het kwadrant:** {kleur} **{kwadrant}**")

    # Visualisatie
    fig, ax = plt.subplots()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Kleuren achtergrond per kwadrant
    ax.axhspan(50, 100, xmin=0.5, xmax=1.0, facecolor='#c8facc')  # Q1
    ax.axhspan(50, 100, xmin=0.0, xmax=0.5, facecolor='#fff9c4')  # Q2
    ax.axhspan(0, 50, xmin=0.0, xmax=0.5, facecolor='#ffcdd2')    # Q3
    ax.axhspan(0, 50, xmin=0.5, xmax=1.0, facecolor='#ffe0b2')    # Q4

    ax.axvline(50, color='black', linestyle='--')
    ax.axhline(50, color='black', linestyle='--')

    ax.plot(x_norm, y_norm, 'ko')  # Stip
    ax.text(x_norm+2, y_norm+2, "Jij", fontsize=12)

    ax.set_xlabel("Actief")
    ax.set_ylabel("Gemotiveerd")
    st.pyplot(fig)

    # Thema-analyse
    st.subheader("📚 Thema-overzicht")
    themas = df.groupby("thema")["antwoord"].mean().sort_values(ascending=False)
    for thema, score in themas.items():
        st.markdown(f"**{thema}**: {round(score, 1)} / 5")