import streamlit as st
from openai import OpenAI
import random

# Load API key
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Sample NYC trivia/history questions
nyc_questions = [
    "Why is the Statue of Liberty considered an important symbol of New York City?",
    "What is Times Square known for?",
    "What was the historical role of Ellis Island in immigration?",
    "Why is Central Park significant to New Yorkers?",
    "How did the subway system transform life in NYC?",
    "What makes the Brooklyn Bridge architecturally or culturally important?",
    "What is the origin of the nickname 'The Big Apple'?",
    "What is Wall Street and why is it important?",
    "How did Harlem become a center for Black culture and the arts?",
    "Why do many people associate New York with opportunity?",
    "What happened on September 11, 2001, in NYC and how did it impact the city?",
    "What makes the New York City skyline unique?",
    "Why is Broadway important to American culture?",
    "How did New York City become one of the most diverse cities in the world?",
    "What is the significance of the Empire State Building?",
    "What is the High Line and why was it turned into a park?",
    "Why do so many TV shows and movies take place in New York?",
    "What is the function of the United Nations headquarters in NYC?",
    "What is the history of Chinatown or Little Italy in Manhattan?",
    "Why is the New York Public Library a cultural landmark?",
    "What was the 1977 NYC blackout and how did the city react?",
    "How do yellow taxis symbolize NYC?",
    "Why is Yankee Stadium iconic in sports history?",
    "What is the New York Marathon and why is it notable?",
    "What is Grand Central Terminal known for?",
    "Why do some people say New York is 'the city that never sleeps'?"
]

# Function to pick a random question
def get_random_question():
    return random.choice(nyc_questions)

# Function to evaluate answer using GPT
def evaluate_answer(question, user_response):
    prompt = f"""
You are a professional historian grading a student's paragraph response to a New York City-related question.

Be a very strict grader. Only give a 5/5 if the answer is factually correct, historically detailed, and contextually rich. Only give a 4/5 in cases where a history major in college would have come up with the answer. Deduct points for:
- Vagueness or generalizations
- Missing key facts (dates, names, context)
- Historical inaccuracies
- Weak structure or lack of relevance

Do NOT award fractional scores. Only score in whole number increments from 1 to 5.

Here is the question and student response:

Question: {question}

Student Response: {user_response}

Provide feedback in the following format:

Score: X / 5  
Feedback: [2–3 sentence explanation justifying the score]
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=250
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"


# Streamlit UI
st.title("🗽 NYC Trivia Challenge")
st.write("Answer a New York City trivia or history question in a short paragraph. Be accurate and detailed for a high score.")

# Generate or reuse question
if "question" not in st.session_state:
    st.session_state.question = get_random_question()

st.subheader("Your Question:")
st.markdown(f"**{st.session_state.question}**")

# User input
user_response = st.text_area("Your Answer (write a short paragraph):", height=200)

# Submit + evaluation
if st.button("Submit Answer"):
    if not user_response.strip():
        st.warning("Please write something before submitting.")
    else:
        st.info("Grading your response...")
        feedback = evaluate_answer(st.session_state.question, user_response)
        st.markdown("---")
        st.markdown(f"### Result\n{feedback}")
        st.markdown("---")
