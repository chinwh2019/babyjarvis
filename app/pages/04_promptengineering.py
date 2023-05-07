import streamlit as st
import openai
import configparser
import os 
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

    def display_examples(self):
        st.subheader("Examples")
        with st.expander("Tactic 1: Use delimiters to clearly indicate distinct parts of the input"):
            st.markdown("""
            In this example, we use delimiters (triple backticks) to clearly indicate distinct parts of the input.
            The model is instructed to summarize the text within the delimiters into a single sentence.
            """)
            
            preset_text = """
            You should express what you want a model to do by 
            providing instructions that are as clear and 
            specific as you can possibly make them. 
            This will guide the model towards the desired output, 
            and reduce the chances of receiving irrelevant 
            or incorrect responses. Don't confuse writing a 
            clear prompt with writing a short prompt. 
            In many cases, longer prompts provide more clarity 
            and context for the model, which can lead to 
            more detailed and relevant outputs. 
            """
            text = st.text_area(
                "Enter text for Tactic 1:",
                value=preset_text,
                placeholder="Your text",
                key="tactic1_text_input",
                height=200,
            )

            preset_prompt = f"""Summarize the text delimited by triple backticks into a single sentence.
            ```{text}```"""

            prompt = st.text_area(
                "Tactic 1 prompt:",
                value=preset_prompt,
                key="tactic1_prompt_input",
                height=200,
            )

            if st.button("Run Tactic 1 Example"):
                with st.spinner("Running..."):
                    response = self.completion_api.get_completion(prompt)
                    st.subheader("Response")
                    # st.write(response)
                    st.markdown(f'<strong>{response}</strong>', unsafe_allow_html=True)
                    # st.markdown(f'<div style="color: blue;">{response}</div>', unsafe_allow_html=True)


        # Other examples can be added as expanders in a similar fashion

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
