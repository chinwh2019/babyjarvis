# Import necessary modules
import streamlit as st
import random

# Create a dictionary to collect responses
responses = {}

# Introduction text
st.title("System Usability Scale Survey")
st.sidebar.title("About this survey:")
st.sidebar.write("This is a System Usability Scale  questionnaire aimed at understanding "
                 "how you think about the diary app usage. "
                 "Your responses will remain anonymous and be used for research purposes only. "
                 "Please answer the questions honestly.")

st.sidebar.subheader("Please enter your demographic information:")
age = st.sidebar.number_input("Age", min_value=1, max_value=120)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Prefer not to say", "Other"])
test_type = st.sidebar.selectbox("Test Type", ["Pretest", "Posttest"])

st.write("Please rate the following statements on a scale of 1 (Not at all true) to 5 (Completely true).")

# List of questions
questions = [
    "I think that I would like to use this system frequently.",
    "I found the system unnecessarily complex.",
    "I thought the system was easy to use.",
    "I think that I would need the support of a technical person to be able to use this system.",
    "I found the various functions in this system were well integrated.",
    "I thought there was too much inconsistency in this system.",
    "I would imagine that most people would learn to use this system very quickly.",
    "I found the system very cumbersome to use.",
    "I felt very confident using the system.",
    "I needed to learn a lot of things before I could get going with this system."
]

# Loop through the questions to display them and collect responses
for i, question in enumerate(questions):
    responses[i+1] = st.slider(question, 1, 5, value=3)

# Function to calculate SUS Score
def calculate_sus_score(responses):
    score = 0
    for i, response in responses.items():
        if i % 2 == 0:
            score += 5 - response
        else:
            score += response - 1
    return score * 2.5

# Submit button to finalize and display the responses
if st.button("Submit"):
    sus_score = calculate_sus_score(responses)
    st.title("Your Responses:")
    with open(f'responses_{age}_{gender}_{test_type}.txt', 'w') as file:
        file.write(f"Age: {age}\nGender: {gender}\nTest Type: {test_type}\nSUS Score: {sus_score}\n")
        for i, response in responses.items():
            file.write(f"Question {i}: {response}\n")
            st.write(f"Question {i}: {response}")
    st.write(f"Your SUS Score: {sus_score}")
    st.write("Your responses have been saved.")
