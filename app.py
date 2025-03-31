import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="FitKompas", layout="centered")

# Laad logo
logo = Image.open("logo.png")
st.image(logo, width=200)

st.title("FitKompas Vragenlijst")

@st.cache_data
def load_data():
    df = pd.read_excel("vragenlijst.xlsx")
    df = df.dropna(subset=["Unnamed: 1"])
    df = df.rename(columns={
        "Unnamed: 1": "vraag",
        "x-as": "x_as",
        "y-as": "y_as",
        "Unnamed: 4": "richting",
        "Unnamed: 6": "thema"
    })
    df = df[df['vraag'].notna() & (df['vraag'] != '')]
    return df

df = load_data()

antwoorden = []
st.write("Beantwoord de onderstaande vragen:")

for i, row in df.iterrows():
    antwoord = st.radio(
        f"{int(row['# vraag'])}. {row['vraag']} - Thema: {row['thema']}",
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

    # Bereken scores voor x-as (actief) en y-as (motivatie)
    x_score = df[df["x_as"].notna()]["antwoord"].sum()
    y_score = df[df["y_as"].notna()]["antwoord"].sum()

    max_x = len(df[df["x_as"].notna()]) * 5
    max_y = len(df[df["y_as"].notna()]) * 5
    x_norm = round((x_score / max_x) * 100)
    y_norm = round((y_score / max_y) * 100)

    st.subheader("📊 Jouw resultaat")
    st.markdown(f"**Actief-score (x-as):** {x_norm}/100")
    st.markdown(f"**Motivatie-score (y-as):** {y_norm}/100")

    # Bepaal kwadrant en geef begeleidende uitleg
    if x_norm < 50 and y_norm < 50:
        kwadrant = "Niet actief & niet gemotiveerd"
        kleur = "🔴"
        uitleg = ("Je hebt zowel een lage actief-score als een lage motivatie-score. "
                 "Het is wellicht tijd om kleine, haalbare doelen te stellen om meer beweging en energie in je leven te brengen.")
    elif x_norm < 50 and y_norm >= 50:
        kwadrant = "Niet actief & wél gemotiveerd"
        kleur = "🟡"
        uitleg = ("Je bent gemotiveerd, maar je actieve gedrag blijft achter. "
                 "Overweeg om te starten met kleine stappen om meer beweging te integreren in je dagelijks leven.")
    elif x_norm >= 50 and y_norm < 50:
        kwadrant = "Wél actief & niet gemotiveerd"
        kleur = "🟠"
        uitleg = ("Je bent actief, maar er ontbreekt nog de motivatie. "
                 "Het kan helpen om doelen te stellen die echt belangrijk voor je zijn, zodat je meer energie en enthousiasme ontwikkelt.")
    else:
        kwadrant = "Wél actief & wél gemotiveerd"
        kleur = "🟢"
        uitleg = ("Je scoort hoog op zowel actief gedrag als motivatie. "
                 "Blijf op deze weg en zoek naar manieren om je gezonde levensstijl nog verder te optimaliseren.")

    st.markdown(f"**Je valt in het kwadrant:** {kleur} **{kwadrant}**")
    st.markdown(uitleg)

    # Visualisatie: 4-kwadranten assenstelsel met een stip voor jouw score
    fig, ax = plt.subplots()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Achtergrondkleuren per kwadrant
    ax.axhspan(50, 100, xmin=0.5, xmax=1.0, facecolor='#c8facc')  # Rechtsboven: wél actief & wél gemotiveerd
    ax.axhspan(50, 100, xmin=0.0, xmax=0.5, facecolor='#fff9c4')  # Linksboven: niet actief & wél gemotiveerd
    ax.axhspan(0, 50, xmin=0.0, xmax=0.5, facecolor='#ffcdd2')    # Linksonder: niet actief & niet gemotiveerd
    ax.axhspan(0, 50, xmin=0.5, xmax=1.0, facecolor='#ffe0b2')    # Rechtsonder: wél actief & niet gemotiveerd

    ax.axvline(50, color='black', linestyle='--')
    ax.axhline(50, color='black', linestyle='--')

    ax.plot(x_norm, y_norm, 'ko')
    ax.text(x_norm + 2, y_norm + 2, "Jij", fontsize=12)
    ax.set_xlabel("Actief")
    ax.set_ylabel("Gemotiveerd")
    st.pyplot(fig)

    # Thema-analyse: gemiddelde score per thema
    st.subheader("📚 Thema-overzicht")
    themas = df.groupby("thema")["antwoord"].mean().sort_values(ascending=False)
    for thema, score in themas.items():
        st.markdown(f"**{thema}**: {round(score, 1)} / 5")
