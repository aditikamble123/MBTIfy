import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath('./utils'))
from utils.generate_pdf import create_pdf

# Page Config
st.set_page_config(page_title="MBTIfy 🔮", page_icon="🧠", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        .main {
            background-color: transparent;
            padding: 30px;
        }
        h1, h2, h3, .question-container strong {
            color: #6A0572 !important;
        }
        .question-container {
            padding: 10px 0;
        }
        .stRadio > div {
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

# Questions
questions = [
    {"question": "I prefer to recharge alone rather than with others.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("I", "E")},
    {"question": "I get energy from social gatherings.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("E", "I")},
    {"question": "I focus on facts and details rather than ideas and concepts.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("S", "N")},
    {"question": "I enjoy interpreting meanings and imagining possibilities.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("N", "S")},
    {"question": "I make decisions with logic and consistency.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("T", "F")},
    {"question": "I consider others' feelings when making decisions.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("F", "T")},
    {"question": "I like to have things decided and organized.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("J", "P")},
    {"question": "I prefer to keep my options open.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("P", "J")},
    {"question": "I prefer texting over calling.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("I", "E")},
    {"question": "I often notice the little things around me.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("S", "N")},
    {"question": "I enjoy abstract theories more than hands-on experience.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("N", "S")},
    {"question": "I value empathy over efficiency.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("F", "T")},
    {"question": "I stick to schedules and plans.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("J", "P")},
    {"question": "I love spontaneous adventures.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("P", "J")},
    {"question": "I feel drained after long social events.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("I", "E")},
    {"question": "I trust experience more than inspiration.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("S", "N")},
    {"question": "I speak with logic, not emotion.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("T", "F")},
    {"question": "I like having a clear to-do list.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("J", "P")},
    {"question": "I tend to avoid conflict, even if it means compromising.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("F", "T")},
    {"question": "I often go with the flow rather than planning ahead.", "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], "trait": ("P", "J")}
]

answers = []
st.write("### Answer the following questions:")

for i, q in enumerate(questions):
    st.markdown(f"<div style='color: white; font-weight: 600;'>{i+1}. {q['question']}</div>", unsafe_allow_html=True)
    answer = st.radio("", q["options"], index=None, horizontal=True, key=f"q{i}")
    answers.append(answer)
    st.markdown("<hr style='border-top: 1px solid #ffffff55;'>", unsafe_allow_html=True)

# Button and scoring logic
if st.button("✨ Get My Personality Type"):
    if None in answers:
        st.error("Please answer all questions before continuing.")
    else:
        score = {"I": 0, "E": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        weight_map = {
            "Strongly Agree": 2,
            "Agree": 1,
            "Neutral": 0,
            "Disagree": -1,
            "Strongly Disagree": -2
        }

        for ans, q in zip(answers, questions):
            weight = weight_map[ans]
            score[q["trait"][0]] += weight
            score[q["trait"][1]] -= weight

        mbti_type = "".join([
            "I" if score["I"] >= score["E"] else "E",
            "S" if score["S"] >= score["N"] else "N",
            "T" if score["T"] >= score["F"] else "F",
            "J" if score["J"] >= score["P"] else "P"
        ])

        definition = mbti_df[mbti_df["Type"] == mbti_type]["Definition"].values[0]

        st.markdown(f"""
            <div style='background-color: #ffeaea; padding: 20px; border-radius: 15px;'>
                <h3 style='color: purple;'>Your MBTI Type: {mbti_type} 🌟</h3>
                <p style='color: black;'>{definition}</p>
            </div>
        """, unsafe_allow_html=True)

        pdf_buffer = create_pdf(mbti_type, definition)
        st.download_button("Download Your Report", data=pdf_buffer, file_name=f"{mbti_type}_report.pdf", mime="application/pdf")
