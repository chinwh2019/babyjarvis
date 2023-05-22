import os
import streamlit as st
import openai 
from langchain import OpenAI, PromptTemplate
from utils import get_api_key_from_config


openai.api_key = get_api_key_from_config()

# Create OpenAI object with default temperature and API key from environment variable
llm = OpenAI(temperature=0.5, openai_api_key=openai.api_key)

template = """
Please write a one sentence summary of the following text:
{essay}
"""

prompt = PromptTemplate(
    input_variables=["essay"],
    template=template
)

def load_essay(file):
    return file.read()

def generate_summary(essay, temperature):
    llm.temperature = temperature
    summary_prompt = prompt.format(essay=essay)
    summary = llm(summary_prompt)
    return summary.strip()

# Streamlit app starts here
st.title('OpenAI Text Summarizer')

st.sidebar.title('Settings')
temperature = st.sidebar.slider('Temperature:', min_value=0.0, max_value=2.0, value=1.0, step=0.1)

uploaded_files = st.file_uploader("Upload your essays", type=['txt', 'pdf'], accept_multiple_files=True)

user_text = st.text_area("Or write your text here:")

if st.button('Generate Summaries'):
    if uploaded_files:
        for i, uploaded_file in enumerate(uploaded_files):
            essay = load_essay(uploaded_file)
            summary = generate_summary(essay, temperature)
            st.write(f'Uploaded File Essay #{i+1} Summary: {summary}')
    if user_text:
        with st.spinner('Generating summary...'):
            summary = generate_summary(user_text, temperature)
            st.success(f'User Text Summary: {summary}')



