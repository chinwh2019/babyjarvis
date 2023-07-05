import streamlit as st
import pandas as pd

# SUS survey questions
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

# initialize data as empty list
data = []

st.title("System Usability Scale Survey")

# collect responses
for q in questions:
    score = st.slider(q, 1, 5, 3)
    data.append(score)

# save responses to dataframe
df = pd.DataFrame(data, index=questions, columns=["score"])

if st.button('Submit Survey'):
    df.to_csv('sus_scores.csv', mode='a')  # append the data to a csv file
    st.success("Survey successfully submitted! Thank you for your participation.")
