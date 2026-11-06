import os
import random

import pandas as pd
import streamlit as st
from google import genai
from google.genai import types

# ---------------- Page setup ----------------
st.set_page_config(page_title="AI Interview Coach", page_icon="🎤", layout="centered")
st.title("🎤 AI Interview Coach")
st.caption("Mock interviews + structured feedback powered by an LLM")

# ---------------- Sidebar: settings ----------------
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input(
        "Gemini API key",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Get a free key from https://aistudio.google.com/apikey",
    )
    model_name = st.text_input("Model name", value="gemini-2.5-flash")
    role = st.selectbox(
        "Target role",
        ["Software Developer", "Data Analyst", "Data Scientist", "AI/ML Engineer", "HR / Behavioural"],
    )
    difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"], value="Medium")
    num_questions = st.slider("Number of questions", 3, 10, 5)

    uploaded_csv = st.file_uploader("Question bank CSV (optional)", type="csv")

    start = st.button("🚀 Start new interview", use_container_width=True)


# ---------------- Helpers ----------------
def load_questions(file):
    """Read the CSV and return a list of questions from the column that looks like 'question'."""
    if file is None:
        return []
    df = pd.read_csv(file)
    q_cols = [c for c in df.columns if "question" in c.lower()]
    if not q_cols:
        st.sidebar.warning("No column with 'question' in its name was found.")
        return []
    return df[q_cols[0]].dropna().astype(str).tolist()


def build_system_prompt(role, difficulty, num_questions, sample_questions):
    prompt = f"""You are a professional interviewer conducting a mock interview for the role of {role}.
Difficulty level: {difficulty}.
Rules:
- Ask exactly ONE question at a time and wait for the candidate's answer.
- After each answer, give a SHORT reaction (1-2 lines) and then ask the next question.
- Ask {num_questions} questions in total, then say the interview is complete.
- Keep a friendly, professional tone."""
    if sample_questions:
        prompt += "\nYou may pick or adapt questions from this question bank:\n- " + "\n- ".join(sample_questions)
    return prompt


def ask_llm(client, model, system_prompt, messages):
    contents = [
        types.Content(role="user" if m["role"] == "user" else "model", parts=[types.Part(text=m["content"])])
        for m in messages
    ]
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    return response.text


# ---------------- Session state ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = ""
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# ---------------- Start interview ----------------
if start:
    if not api_key:
        st.sidebar.error("Please enter your API key first.")
    else:
        questions = load_questions(uploaded_csv)
        sample = random.sample(questions, min(30, len(questions))) if questions else []
        st.session_state.system_prompt = build_system_prompt(role, difficulty, num_questions, sample)
        st.session_state.messages = []
        st.session_state.feedback = ""
        client = genai.Client(api_key=api_key)
        opening = [{"role": "user", "content": "Hello, I am ready. Please start the interview."}]
        with st.spinner("Interviewer is getting ready..."):
            first_q = ask_llm(client, model_name, st.session_state.system_prompt, opening)
        st.session_state.messages = opening + [{"role": "assistant", "content": first_q}]

# ---------------- Chat display ----------------
for i, m in enumerate(st.session_state.messages):
    if i == 0:  # hide the hidden "start" message
        continue
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ---------------- Chat input ----------------
if st.session_state.messages:
    user_answer = st.chat_input("Type your answer here...")
    if user_answer:
        st.session_state.messages.append({"role": "user", "content": user_answer})
        with st.chat_message("user"):
            st.markdown(user_answer)
        client = genai.Client(api_key=api_key)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = ask_llm(client, model_name, st.session_state.system_prompt, st.session_state.messages)
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    # ---------------- Feedback ----------------
    st.divider()
    if st.button("📝 End interview & get feedback"):
        transcript = "\n".join(
            f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages[1:]
        )
        feedback_prompt = f"""Here is a mock interview transcript for the role of {role}.
Give structured feedback in markdown with these sections:
1. Overall score out of 10
2. Strengths
3. Areas to improve
4. Question-by-question comments
5. Communication & confidence tips
6. Suggested topics to practice next

Transcript:
{transcript}"""
        client = genai.Client(api_key=api_key)
        with st.spinner("Preparing your feedback..."):
            st.session_state.feedback = ask_llm(
                client,
                model_name,
                "You are an expert interview coach who gives honest, constructive feedback.",
                [{"role": "user", "content": feedback_prompt}],
            )

    if st.session_state.feedback:
        st.subheader("📊 Your Feedback")
        st.markdown(st.session_state.feedback)
else:
    st.info("👈 In the sidebar, select Settings and click Start new interview")
