import streamlit as st
import pandas as pd
from PIL import Image

# Custom CSS voor een schermvullende vraagweergave en mooie styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    h1, h3, h4 {
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
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="FitKompas", layout="wide")

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
        "# vraag": "# vraag"
    })
    df = df[df['vraag'].notna() & (df['vraag'] != '')]
    df.reset_index(drop=True, inplace=True)
    return df

df = load_data()
total_questions = len(df)

# Initialiseer session_state voor huidige vraagindex en antwoorden
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# Toon één vraag per keer in een schermvullende container
if st.session_state.q_index < total_questions:
    question = df.iloc[st.session_state.q_index]
    with st.container():
        st.markdown('<div class="question-container">', unsafe_allow_html=True)
        st.markdown(f"### Vraag {st.session_state.q_index + 1} van {total_questions}", unsafe_allow_html=True)
        st.markdown(f"<h3><strong>{int(question['# vraag'])}. {question['vraag']}</strong></h3>", unsafe_allow_html=True)
        st.markdown(f"<h4>Thema: {question['thema']}</h4>", unsafe_allow_html=True)
        
        # Likert-schaal met tekstopties (zonder cijfers)
        options = [
            "Helemaal niet mee eens",
            "Mee oneens",
            "Neutraal",
            "Mee eens",
            "Helemaal mee eens"
        ]
        antwoord = st.radio("Selecteer jouw mening:", options, horizontal=True, key=f"vraag_{st.session_state.q_index}")
        
        if st.button("Volgende"):
            st.session_state.answers.append(antwoord)
            st.session_state.q_index += 1
            st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.success("Je hebt alle vragen beantwoord!")
    st.markdown("### Jouw antwoorden:")
    for i, ans in enumerate(st.session_state.answers):
        st.markdown(f"**Vraag {i+1}:** {ans}")
    
    if st.button("Opnieuw beginnen"):
        st.session_state.q_index = 0
        st.session_state.answers = []
        st.experimental_rerun()
