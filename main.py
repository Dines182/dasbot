import streamlit as st
from visual import visual
from statis import statis
from prediction import about_us

# Set page config
st.set_page_config(page_title="Student Enrolment and Attendance Analysis", layout="wide")
st.markdown("""
    <style>
    .main > div:first-child {
        padding-top: 0rem;
    }

    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');

    .custom-title {
        margin-bottom: 0rem;
    }

    .custom-title h1 {
        margin: 0;
        padding: 0;
        font-family: 'Poppins', sans-serif;
        font-size: 2.8rem;
        background: linear-gradient(to right, #1abc9c, #16a085);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        text-shadow:
            2px 2px 6px rgba(255, 255, 255, 0.2),
            -1px -1px 2px rgba(0, 0, 0, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="custom-title">
        <h1> VISUAL :) </h1>
    </div>
""", unsafe_allow_html=True)



# Define pages
pages = {
    "📊 Statistics": statis,
    "📈 Visualisation": visual,
    "ℹ️ Prediction": about_us
}

# Apply custom style to make the radio button look like a navbar
st.markdown("""
    <style>
    div[data-baseweb="radio"] > div {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    label[data-testid="stRadioOption"] {
        background-color: #2c3e50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    label[data-testid="stRadioOption"]:hover {
        background-color: #1abc9c;
        color: black;
    }
    input[type="radio"]:checked + div {
        color: Green !important;
    }
    </style>
""", unsafe_allow_html=True)

# Render navbar using st.radio
selected = st.radio("Navigation", list(pages.keys()), horizontal=True, label_visibility="collapsed")

# Render selected page
pages[selected]()
