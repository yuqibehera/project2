import streamlit as st
import re
st.set_page_config(
    page_title="Smart Math Mistake Analyzer",
    page_icon="🧠",
    layout="centered"
)


st.markdown(
    """
    <h1 style="text-align:center;"> Smart Math Mistake Analyzer</h1>
    <p style="text-align:center; color:gray;">
    Understand <b>why</b> a math answer is wrong — not just that it is wrong.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


st.subheader(" Math Question")
question = st.text_input(
    "Enter a percentage-based question",
    placeholder="Example: Find 20% of 150"
)

st.subheader(" Student Solution")
student_solution = st.text_area(
    "Enter the student's working / steps",
    placeholder="Example: 20% × 150 = 20 × 150 = 3000"
)

analyze_btn = st.button(" Analyze Thinking")


def analyze_percentage_solution(question, solution):
    solution_lower = solution.lower()

    if "%" in solution_lower and re.search(r"\b\d+\s*[x×*]\s*\d+", solution_lower):
        return {
            "mistake": "Percentage not converted to fraction",
            "explanation": (
                "The student treated the percentage as a whole number instead of "
                "converting it into a fraction or decimal."
            ),
            "correction": (
                "Percent means 'per hundred'. So 20% should be written as 20/100 or 0.2 "
                "before multiplying."
            ),
            "tip": "Always convert percentages before calculating."
        }

    if "%" in question.lower() and "of" in question.lower():
        if "100" not in solution_lower and "0." not in solution_lower:
            return {
                "mistake": "Incorrect understanding of base value",
                "explanation": (
                    "The student did not clearly identify the base value on which the "
                    "percentage should be applied."
                ),
                "correction": (
                    "When a question says 'X% of Y', the base value is Y. "
                    "The percentage must always be applied to that base."
                ),
                "tip": "First identify the base value before calculating percentages."
            }
  if "0." in solution_lower or "/100" in solution_lower:
        return {
            "mistake": "Calculation error after correct setup",
            "explanation": (
                "The student used the correct percentage form but made an arithmetic "
                "mistake during calculation."
            ),
            "correction": (
                "Re-check multiplication and division steps carefully after setting "
                "up the correct expression."
            ),
            "tip": "Slow down during calculations — small arithmetic errors are common."
        }


    return {
        "mistake": "Unclear or mixed reasoning error",
        "explanation": (
            "The student's reasoning does not follow a clear percentage-solving method."
        ),
        "correction": (
            "A clear step-by-step approach is needed: convert percentage, identify base, "
            "then calculate."
        ),
        "tip": "Write each step clearly to avoid logical confusion."
    }

if analyze_btn:
    if not question or not student_solution:
        st.warning("Please enter both the question and the student's solution.")
    else:
        result = analyze_percentage_solution(question, student_solution)

        st.subheader(" Detected Issue")
        st.error(result["mistake"])

        st.subheader(" Why this happened")
        st.write(result["explanation"])

        st.subheader(" Correct Approach")
        st.write(result["correction"])

        st.subheader(" Learning Tip")
        st.success(result["tip"])

        st.caption("Focus is on understanding thinking, not memorizing formulas.")


st.divider()
st.caption(
    "Hackathon project focused on mathematical reasoning and learning clarity."
)
