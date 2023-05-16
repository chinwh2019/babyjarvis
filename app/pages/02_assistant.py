#!/usr/bin/env python3
# coding: utf-8

import streamlit as st
import openai
import pandas as pd 
from utils import get_api_key_from_config

# Constants
MODEL_NAME = "gpt-3.5-turbo"
MAX_TOKENS = 3000
APP_TITLE = "🤖 Personal A.I. Assistant"

# Set the API Key
openai.api_key = get_api_key_from_config()

# Function to generate text
def generate_text(prompt: str, temperature: float, top_p: float, max_tokens: int) -> str:
    messages = st.session_state["messages"]
    messages.append({"role": "user", "content": prompt})
    print(messages)

    # Truncate the conversation history if it exceeds the max tokens limit
    while sum(len(m["content"]) for m in messages) > max_tokens:
        print("Truncating conversation history...")
        messages.pop(0)

    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while generating text."

    content = response["choices"][0]["message"]["content"]
    total_tokens = response["usage"]["total_tokens"]
    messages.append({"role": "assistant", "content": content})

    return content

def display_conversation(prompts, contents):
    for p, c in zip(prompts, contents):
        st.success(p)
        st.info(c)

def main():
    st.title(APP_TITLE)

    # Initialize 'prompt' in session state
    if "prompt" not in st.session_state:
        st.session_state.prompt = ""

    # Upload CSV file
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")

    # If no file is uploaded, use the preset file
    if uploaded_file is None:
        data = pd.read_csv('assets/EnglishPrompts.csv')
    else:
        data = pd.read_csv(uploaded_file)
    
    # Get the first column name of the CSV file
    first_column_name = data.columns[0]

    # Select a role for AI
    selected_value = st.sidebar.selectbox("Select a role for AI (Optional)", options=data[first_column_name])

    # Add a 'New Conversation' button
    new_conversation = st.sidebar.button('New Conversation')

    if new_conversation:
        st.session_state["messages"] = []
        st.session_state["prompts"] = []
        st.session_state["contents"] = []

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Update the system message based on the selected role
    if not st.session_state["messages"] or st.session_state["messages"][0]["role"] == "system":
        if selected_value == '':
            st.session_state["messages"] = [{"role": "system", "content": "You are a friendly and helpful AI assistant."}] + st.session_state["messages"][1:]
        else:
            selected_row = data[data[first_column_name] == selected_value].iloc[0]
            st.session_state["messages"] = [{"role": "system", "content": selected_row['prompt']}] + st.session_state["messages"][1:]

    st.sidebar.title("Tuning Options")
    
    # Temperature
    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Controls the randomness of the AI's output."
    )

    # Top P
    top_p = st.sidebar.slider(
        "Top P",
        min_value=0.0,
        max_value=1.0,
        value=1.0,
        step=0.1,
        help="Nucleus sampling: the model will choose from a subset of tokens whose cumulative probability exceeds this value."
    )

    # Max Tokens
    max_tokens = st.sidebar.slider(
        "Max Tokens",
        min_value=50,
        max_value=4096,
        value=3000,
        step=100,
        help="The maximum length of the model's output."
    )

    if "prompts" not in st.session_state:
        st.session_state["prompts"] = []
    if "contents" not in st.session_state:
        st.session_state["contents"] = []
        
    display_conversation(st.session_state["prompts"], st.session_state["contents"])

    if "input_prompt" not in st.session_state:
        st.session_state["input_prompt"] = ""

    def call_generate_text():
        prompt = st.session_state.prompt.strip()

        if prompt:
            st.session_state["prompts"].append(prompt)
            content = generate_text(prompt, temperature, top_p, max_tokens)
            st.session_state["contents"].append(content)
            st.session_state.prompt = ""

    prompt = st.text_area("Prompt", value=st.session_state.prompt, key="prompt")

    st.button("SEND", on_click=call_generate_text)


if __name__ == "__main__":
    main()
