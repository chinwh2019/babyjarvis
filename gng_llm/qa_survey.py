import streamlit as st

# Create a dictionary to collect responses
responses = {}

# Introduction text
st.title("Self-Efficacy Questionnaire")
st.sidebar.title("About this survey:")
st.sidebar.write("This is a self-efficacy questionnaire aimed at understanding "
                 "how you perceive your ability to handle various life situations. "
                 "Your responses will remain anonymous and be used for research purposes only. "
                 "Please answer the questions honestly.")

st.sidebar.subheader("Please enter your demographic information:")
age = st.sidebar.number_input("Age", min_value=1, max_value=120)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Prefer not to say", "Other"])
test_type = st.sidebar.selectbox("Test Type", ["Pretest", "Posttest"])

st.write("Please rate the following statements on a scale of 1 (Not at all true) to 5 (Completely true).")

# List of questions
questions = [
    "I am confident in my ability to handle problems that arise in my life.",
    "I can overcome challenges when I put my mind to it.",
    "When I encounter difficulties, I know how to find solutions.",
    "I am able to achieve goals that I set for myself.",
    "I can stick to my plans, even when things get tough.",
    "I am confident in my ability to deal with unexpected events.",
    "I am capable of making decisions that benefit my well-being.",
    "I can find different ways to achieve my goals when faced with obstacles.",
    "I can keep going when faced with difficult situations.",
    "I am confident in my ability to manage stress and maintain overall well-being.",
]

# Loop through the questions to display them and collect responses
for i, question in enumerate(questions):
    responses[question] = st.slider(question, 1, 5)

# Submit button to finalize and display the responses
if st.button("Submit"):
    st.title("Your Responses:")
    with open(f'responses_{age}_{gender}_{test_type}.txt', 'w') as file:
        file.write(f"Age: {age}\nGender: {gender}\n")
        for question, response in responses.items():
            file.write(f"{question}: {response}\n")
            st.write(f"{question}: {response}")
    st.write("Your responses have been saved.")
