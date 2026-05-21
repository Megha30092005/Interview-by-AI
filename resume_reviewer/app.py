import streamlit as st
from services.question_generator import generate_mcqs
from services.evaluator import evaluate_mcq

st.set_page_config(page_title="AI Interview System")

# SESSION
if "stage" not in st.session_state:
    st.session_state.stage = "home"
    st.session_state.questions = []

# ---------------- HOME ----------------
if st.session_state.stage == "home":
    st.title("AI Resume Interview System")

    jd = st.text_area("Paste Job Description")
    resume = st.file_uploader("Upload Resume")

    if st.button("Start"):
        if jd and resume:
            st.session_state.jd = jd
            resume_text = resume.read().decode("utf-8", errors="ignore")
            st.session_state.resume_text = resume_text

            st.session_state.stage = "aptitude"
            st.session_state.questions = []
            st.rerun()

# ---------------- APTITUDE ----------------
elif st.session_state.stage == "aptitude":
    st.title("Aptitude Round")

    if not st.session_state.get("questions"):
        st.session_state.questions = generate_mcqs(f"""
You are an aptitude test generator.

Generate 10 MCQ questions strictly for aptitude.

Sections to include:
- Logical reasoning
- Quantitative aptitude
- Verbal ability
- Data interpretation

STRICT RULES:
- Questions must be clear and correct
- Avoid ambiguous or wrong options
- Each question must have exactly 4 options
- One correct answer must be present in options
- Do NOT generate inconsistent questions

Difficulty:
- Mix of easy and medium

Output MUST be valid JSON only.

Format:
[
  {{
    "question": "text",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]
""")

    if not isinstance(st.session_state.questions, list):
        st.session_state.questions = []

    user_answers = []

    for i, q in enumerate(st.session_state.questions):
        ans = st.radio(q["question"], q["options"], key=i)
        user_answers.append(ans)

    # ✅ FIX: score >= 1
    if st.button("Submit"):
        score = evaluate_mcq(user_answers, st.session_state.questions)

        if score >= 1:
            st.session_state.stage = "technical"
            st.session_state.questions = []
        else:
            st.session_state.stage = "fail"

        st.rerun()
# ---------------- TECHNICAL ----------------
# ---------------- TECHNICAL ----------------
elif st.session_state.stage == "technical":
    st.title("Technical Round")

    if not st.session_state.get("questions"):
        resume_text = st.session_state.get("resume_text", "")
        jd = st.session_state.get("jd", "")

        topic = f"""
You are a technical interviewer.

Candidate Resume:
{resume_text[:300]}

Job Description:
{jd[:200]}

Generate 10 TECHNICAL MCQ questions strictly from:
- programming
- coding concepts
- databases
- software concepts

DO NOT generate aptitude or math questions.

Ensure:
- Questions are skill-based
- Include correct answers
STRICT RULES:
- Questions must be technical (coding, CS concepts)
- NO math or aptitude questions
- 4 options per question
- One correct answer
- Output MUST be valid JSON

Format:
[
  {{
    "question": "text",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

"""

        st.session_state.questions = generate_mcqs(topic)

    if not isinstance(st.session_state.questions, list):
        st.session_state.questions = []

    user_answers = []

    for i, q in enumerate(st.session_state.questions):
        ans = st.radio(q["question"], q["options"], key=f"tech_{i}")
        user_answers.append(ans)

    # ✅ FIX: score >= 1
    if st.button("Submit"):
        score = evaluate_mcq(user_answers, st.session_state.questions)

        if score >= 1:
            st.session_state.stage = "hr"
            st.session_state.questions = []
        else:
            st.session_state.stage = "fail"

        st.rerun()
# ---------------- HR ----------------
elif st.session_state.stage == "hr":
    st.title("HR Round")

    q1 = st.text_input("Tell me about yourself")
    q2 = st.text_input("Why should we hire you?")
    q3 = st.text_input("How do you handle pressure?")

    # ✅ PASS ALWAYS IF FILLED
    if st.button("Submit"):
        if q1 and q2 and q3:
            st.session_state.stage = "success"
        else:
            st.session_state.stage = "fail"

        st.rerun()
# ---------------- SUCCESS ----------------
elif st.session_state.stage == "success":
    st.success("🎉 Congratulations! You are selected!")

    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()


# ---------------- FAIL ----------------
elif st.session_state.stage == "fail":
    st.error("❌ Better luck next time!")

    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()