import streamlit as st
import openai
import configparser
import os 
import json 
from utils import get_api_key_from_config


class OpenAICompletion:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

    def get_completion(self, prompt, temperature=0):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message["content"]
    

class OpenAIApp:
    def __init__(self):
        self.completion_api = None

    def get_openai_api_key(self):
        if "api_key" not in st.session_state:
            api_key_from_config = get_api_key_from_config()
            if api_key_from_config:
                st.session_state.api_key = api_key_from_config
            else:
                st.session_state.api_key = ""

        return st.sidebar.text_input(
            "Enter your OpenAI API key:",
            value=st.session_state.api_key,
            placeholder="Your OpenAI API Key",
            type="password",
        )

    def display_tactic(self, tactic):
            with st.expander(tactic["title"]):
                st.markdown(tactic["description"])

                text = st.text_area(
                    tactic["text_input_label"],
                    value=tactic["preset_text"],
                    placeholder="Your text",
                    key=f"{tactic['title']}_text_input",
                    height=200,
                )

                preset_prompt = tactic["preset_prompt"].format(text=text)

                prompt = st.text_area(
                    f"{tactic['title']} prompt:",
                    value=preset_prompt,
                    key=f"{tactic['title']}_prompt_input",
                    height=200,
                )

                if st.button(tactic["button_label"]):
                    with st.spinner("Running..."):
                        response = self.completion_api.get_completion(prompt)
                        st.subheader("Response")
                        st.markdown(f'<span style="color: #00008B;">{response}</span>', unsafe_allow_html=True)

    def display_examples(self):
        st.subheader("Examples")

        with open('tactics.json', 'r') as f:
            tactics = json.load(f)

        for tactic in tactics:
            self.display_tactic(tactic)



    def main(self):
        st.title("Prompt Engineering - Essential Tactics") 

        openai_api_key = self.get_openai_api_key()

        if openai_api_key:
            self.completion_api = OpenAICompletion(openai_api_key)
            self.display_examples()

        else:
            st.error("Please enter your OpenAI API key in the sidebar.")


if __name__ == "__main__":
    app = OpenAIApp()
    app.main()
