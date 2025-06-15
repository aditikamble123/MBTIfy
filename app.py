import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath('./utils'))

from generate_pdf import create_pdf

import io

# Page Config
st.set_page_config(page_title="MBTIfy 🔮", page_icon="🧠", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        .main {
            background-color: transparent;
            padding: 30px;
        }
        h1, h2, h3, .question-container strong, label, .stRadio, .stRadio div, .stRadio span {
            color: white !important;
        }
        .question-container {
            padding: 10px 0;
        }
        .stRadio > div {
            background-color: transparent !important;
            padding: 0;
            margin-bottom: 5px;
            display: flex !important;
            flex-direction: row !important;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }
        .stRadio label {
            background: none !important;
            border: none !important;
            box-shadow: none !important;
            white-space: nowrap;
        }
        .stButton button {
            background-color: #6a0dad;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Load MBTI definitions
mbti_df = pd.read_csv("types.csv")[["Type", "Definition"]]

# Begin app container
st.markdown("<div class='main'>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>MBTIfy 🔮</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Discover your true personality type with our 20-question MBTI quiz.</p>", unsafe_allow_html=True)

# Define 20 MBTI questions
questions = [
    {"question": "I prefer to recharge alone rather than with others.", "options": ["Agree", "Disagree"], "trait": ("I", "E")},
    {"question": "I get energy from social gatherings.", "options": ["Agree", "Disagree"], "trait": ("E", "I")},
    {"question": "I focus on facts and details rather than ideas and concepts.", "options": ["Agree", "Disagree"], "trait": ("S", "N")},
    {"question": "I enjoy interpreting meanings and imagining possibilities.", "options": ["Agree", "Disagree"], "trait": ("N", "S")},
    {"question": "I make decisions with logic and consistency.", "options": ["Agree", "Disagree"], "trait": ("T", "F")},
    {"question": "I consider others' feelings when making decisions.", "options": ["Agree", "Disagree"], "trait": ("F", "T")},
    {"question": "I like to have things decided and organized.", "options": ["Agree", "Disagree"], "trait": ("J", "P")},
    {"question": "I prefer to keep my options open.", "options": ["Agree", "Disagree"], "trait": ("P", "J")},
    {"question": "I prefer texting over calling.", "options": ["Agree", "Disagree"], "trait": ("I", "E")},
    {"question": "I often notice the little things around me.", "options": ["Agree", "Disagree"], "trait": ("S", "N")},
    {"question": "I enjoy abstract theories more than hands-on experience.", "options": ["Agree", "Disagree"], "trait": ("N", "S")},
    {"question": "I value empathy over efficiency.", "options": ["Agree", "Disagree"], "trait": ("F", "T")},
    {"question": "I stick to schedules and plans.", "options": ["Agree", "Disagree"], "trait": ("J", "P")},
    {"question": "I love spontaneous adventures.", "options": ["Agree", "Disagree"], "trait": ("P", "J")},
    {"question": "I feel drained after long social events.", "options": ["Agree", "Disagree"], "trait": ("I", "E")},
    {"question": "I trust experience more than inspiration.", "options": ["Agree", "Disagree"], "trait": ("S", "N")},
    {"question": "I speak with logic, not emotion.", "options": ["Agree", "Disagree"], "trait": ("T", "F")},
    {"question": "I like having a clear to-do list.", "options": ["Agree", "Disagree"], "trait": ("J", "P")},
    {"question": "I tend to avoid conflict, even if it means compromising.", "options": ["Agree", "Disagree"], "trait": ("F", "T")},
    {"question": "I often go with the flow rather than planning ahead.", "options": ["Agree", "Disagree"], "trait": ("P", "J")}
]

# Collect answers
answers = []
st.write("### Answer the following questions:")
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-container'><strong>{i+1}. {q['question']}</strong></div>", unsafe_allow_html=True)
    answer = st.selectbox("Choose your answer:", scale, index=None, key=f"q{i}")
    answers.append(answer)
    st.markdown("<hr>", unsafe_allow_html=True)

# Compute MBTI
if st.button("✨ Get My Personality Type"):
    if None in answers:
        st.error("Please answer all questions before continuing.")
    else:
        score = {"I": 0, "E": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        for ans, q in zip(answers, questions):
            if ans == "Agree":
                score[q["trait"][0]] += 1
            else:
                score[q["trait"][1]] += 1

        mbti = "".join([
            "I" if score["I"] >= score["E"] else "E",
            "S" if score["S"] >= score["N"] else "N",
            "T" if score["T"] >= score["F"] else "F",
            "J" if score["J"] >= score["P"] else "P"
        ])

        definition = mbti_df[mbti_df["Type"] == mbti]["Definition"].values[0]
# ✅ Safe and error-free usage — only after MBTI is computed
st.markdown(f"""
    <div style='background-color: #FFE5EC; padding: 20px; border-radius: 15px; color: #6A0572; font-weight: bold; font-size: 24px; text-align: center;'>
        Your MBTI Type: {mbti} 🌟
        <div style='font-size: 16px; font-weight: normal; margin-top: 10px;'>{definition}</div>
    </div>
""", unsafe_allow_html=True)


        pdf_buffer = create_pdf(mbti, definition)
        st.download_button("Download Your Report", data=pdf_buffer, file_name=f"{mbti}_report.pdf", mime="application/pdf")

# End of container
st.markdown("</div>", unsafe_allow_html=True)
