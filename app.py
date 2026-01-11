import streamlit as st
import re
from openai import OpenAI


st.set_page_config(
    page_title="Smart Math Mistake Analyzer",
    page_icon="🧠",
    layout="centered"
)

client = OpenAI(
    api_key="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"
)

st.markdown(
    """
    <h1 style='text-align:center;'> Smart Math Mistake Analyzer</h1>
    <p style='text-align:center; color: gray;'>
    An educational tool that analyzes student thinking — not just answers.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

st.subheader("📘 Problem")
question = st.text_input(
    "Enter a percentage-based math question",
    placeholder="Example: Find 20% of 150"
)

st.subheader(" Student Solution")
student_solution = st.text_area(
    "Enter the student's working / steps",
    placeholder="Example: 20% × 150 = 20 × 150 = 3000"
)

analyze = st.button(" Analyze Thinking")

def analyze_percentage_logic(question, solution):
    solution = solution.lower()

    if "%" in solution and re.search(r"\b\d+\s*[x×*]\s*\d+", solution):
        return {
            "mistake": "Percentage not converted to fraction",
            "confidence": "High"
        }

    if "%" in question.lower() and "of" in question.lower():
        if "100" not in solution and "0." not in solution:
            return {
                "mistake": "Incorrect understanding of percentage base value",
                "confidence": "Medium"
            }

    if "0." in solution or "/100" in solution:
        return {
            "mistake": "Calculation mistake after correct setup",
            "confidence": "Medium"
        }

    return {
        "mistake": "Unclear or mixed reasoning error",
        "confidence": "Low"
    }


def get_ai_feedback(mistake, question, student_solution):
    prompt = f"""
You are a calm and supportive math tutor.

A student attempted this question:
{question}

Their solution:
{student_solution}

Detected issue:
{mistake}

Explain in a friendly and human way:
- Where the reasoning went wrong
- Why this happens
- How to solve it correctly
- One short learning tip

Keep it simple, encouraging, and educational.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful math tutor for students."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content



if analyze:
    if not question or not student_solution:
        st.warning("Please enter both the question and the student's solution.")
    else:
        result = analyze_percentage_logic(question, student_solution)

        st.subheader(" Analysis Result")
        st.error(f"**Detected Issue:** {result['mistake']}")
        st.info(f"**Confidence Level:** {result['confidence']}")

        with st.spinner("Analyzing thinking like a tutor..."):
            feedback = get_ai_feedback(
                result["mistake"],
                question,
                student_solution
            )

        st.subheader("📖 Tutor Feedback")
        st.write(feedback)

        st.success("Analysis complete. Learning > memorization ")


st.divider()
st.caption(
    "Built as an education-focused hackathon project. "
    "Combines logical error detection with AI-assisted explanations."
)
