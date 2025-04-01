import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

# Zorg ervoor dat set_page_config als eerste Streamlit-commando wordt aangeroepen!
st.set_page_config(page_title="FitKompas", layout="wide")

# Custom CSS voor een mooie, schermvullende layout
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    h1, h3 {
        font-family: 'Segoe UI', sans-serif;
        color: #2e7d32;
    }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .question-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 80vh;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Laad logo en toon titel
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
        "Unnamed: 6": "thema",
        "# vraag": "# vraag"  # zorg dat deze kolom aanwezig is
    })
    df = df[df['vraag'].notna() & (df['vraag'] != '')]
    df.reset_index(drop=True, inplace=True)
    return df

df = load_data()
total_questions = len(df)

# Initializeer session_state voor huidige vraagindex en antwoorden
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# Toon één vraag per keer
if st.session_state.q_index < total_questions:
    question = df.iloc[st.session_state.q_index]
    with st.container():
        st.markdown(f"### Vraag {st.session_state.q_index + 1} van {total_questions}")
        st.markdown(f"**{int(question['# vraag'])}. {question['vraag']}**")
        st.markdown(f"**Thema:** {question['thema']}")
        
        # Likert-schaal met tekstopties (zonder cijfers)
        options = [
            "Helemaal niet mee eens",
            "Mee oneens",
            "Neutraal",
            "Mee eens",
            "Helemaal mee eens"
        ]
        # Toon de radio buttons horizontaal als scorebalk
        antwoord = st.radio("Selecteer jouw mening:", options, horizontal=True, key=f"vraag_{st.session_state.q_index}")
        
        if st.button("Volgende"):
            st.session_state.answers.append(antwoord)
            st.session_state.q_index += 1
            st.experimental_rerun()
else:
    st.success("Je hebt alle vragen beantwoord!")
    st.markdown("### Jouw antwoorden:")
    for i, ans in enumerate(st.session_state.answers):
        st.markdown(f"**Vraag {i+1}:** {ans}")
    
    if st.button("Opnieuw beginnen"):
        st.session_state.q_index = 0
        st.session_state.answers = []
        st.experimental_rerun()
