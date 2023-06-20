#!/usr/bin/env python3
# coding: utf-8

import streamlit as st
import openai
import pandas as pd
from utils import get_api_key_from_config

# Constants
MODEL_NAMES = ["gpt-3.5-turbo", "gpt-3.5-turbo-16k-0613"]
DEFAULT_MODEL = "gpt-3.5-turbo-16k-0613"
MAX_TOKENS = 15000
APP_TITLE = "🤖 Personal A.I. Assistant"
DEFAULT_CSV = 'assets/EnglishPrompts.csv'

# Set the API Key
openai.api_key = get_api_key_from_config()

# Function to generate text
# Function to generate text
def generate_text(prompt: str, temperature: float, top_p: float, max_tokens: int, model: str) -> str:
    messages = st.session_state.get("messages", [])

    # Ensure the new prompt does not exceed the max tokens
    prompt = prompt[:max_tokens] if len(prompt.split()) > max_tokens else prompt

    new_message = {"role": "user", "content": prompt}

    # Calculate the total length of messages (including the new prompt)
    total_length = sum(len(m["content"].split()) for m in messages) + len(new_message["content"].split())

    # Truncate the conversation history if it exceeds the max tokens limit
    while total_length > max_tokens and messages:
        st.write("Truncating conversation history...")
        removed_message = messages.pop(0)
        total_length -= len(removed_message["content"].split())

    messages.append(new_message)

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )
    except Exception as e:  # general Exception to handle all types of exceptions
        st.error(f"Error: {str(e)}")
        return "An error occurred while generating text."

    content = response.choices[0].message["content"]
    total_tokens = response["usage"]["total_tokens"]
    messages.append({"role": "assistant", "content": content})

    return content


def display_conversation(prompts, contents):
    for p, c in zip(prompts, contents):
        st.success(p)
        st.info(c)

def init_session_state():
    st.session_state["messages"] = []
    st.session_state["prompts"] = []
    st.session_state["contents"] = []
    st.session_state["prompt"] = ""

def main():
    st.title(APP_TITLE)
    st.write("Welcome to the Personal A.I. Assistant. Use the sidebar to upload your CSV file and tune the model settings.")

    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is None:
        data = pd.read_csv(DEFAULT_CSV)
    else:
        try:
            data = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error("Error reading CSV file. Please make sure it is correctly formatted.")
            return

    first_column_name = data.columns[0]

    selected_value = st.sidebar.selectbox("Select a role for AI (Optional)", options=data[first_column_name])

    if selected_value:
        selected_row = data[data[first_column_name] == selected_value]
        if not selected_row.empty:
            st.sidebar.markdown(f'**Selected role details:**\n{selected_row.iloc[0].to_string()}')

    new_conversation = st.sidebar.button('New Conversation')

    if new_conversation or "messages" not in st.session_state:
        init_session_state()

    if not st.session_state["messages"] or st.session_state["messages"][0]["role"] == "system":
        if selected_value == '':
            st.session_state["messages"] = [{"role": "system", "content": "You are a friendly and helpful AI assistant."}] + st.session_state["messages"][1:]
        else:
            selected_row = None
            if selected_value:
                selected_row = data[data[first_column_name] == selected_value]
            if selected_row is not None and not selected_row.empty:
                st.session_state["messages"] = [{"role": "system", "content": selected_row.iloc[0]['prompt']}] + st.session_state["messages"][1:]

    st.sidebar.title("Tuning Options")

    # Model selection
    model = st.sidebar.selectbox("Select the model", options=MODEL_NAMES, index=MODEL_NAMES.index(DEFAULT_MODEL))

    # Temperature
    temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=2.0, value=1.0, step=0.1, help="Controls the randomness of the AI's output.")

    # Top P
    top_p = st.sidebar.slider("Top P", min_value=0.0, max_value=1.0, value=1.0, step=0.1, help="Nucleus sampling: the model will choose from a subset of tokens whose cumulative probability exceeds this value.")

    # Max Tokens
    max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=4096, value=MAX_TOKENS, step=100, help="The maximum length of the model's output.")

    display_conversation(st.session_state.get("prompts", []), st.session_state.get("contents", []))

    def call_generate_text():
        prompt = st.session_state.prompt.strip()
        if prompt:
            st.session_state["prompts"].append(prompt)
            with st.spinner("Generating response..."):
                content = generate_text(prompt, temperature, top_p, max_tokens, model or DEFAULT_MODEL)
            st.session_state["contents"].append(content)
            st.session_state.prompt = ""

    st.text_area("Prompt", value=st.session_state.get("prompt", ""), key="prompt", on_change=call_generate_text)

    if st.button('Download Conversation'):
        download_conversation(st.session_state.get("prompts", []), st.session_state.get("contents", []))

    if st.button('Clear Conversation'):
        st.session_state.clear()
        init_session_state()

def download_conversation(prompts, contents):
    conversation = '\n'.join(f'User: {p}\nAI: {c}' for p, c in zip(prompts, contents))
    st.download_button('Download Conversation', data=conversation, file_name='conversation.txt', mime='text/plain')

if __name__ == "__main__":
    main()
