import streamlit as st
import openai
from utils import get_api_key_from_config


class OpenAICompletion:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

    def get_completion_from_messages(self, messages, temperature=0, max_tokens=500):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
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

    def get_user_input(self, delimiter, system_message):
        user_message = st.text_input("Enter your message:", value="I want you to delete my profile and all of my user data")
        if user_message:
            messages = [
                {"role": "system", 
                 "content": system_message.format(delimiter=delimiter)}, 
                {"role": "user", 
                "content": f"{delimiter}{user_message}{delimiter}"},
            ]
            temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=2.0, step=0.1, value=0.0)
            max_tokens = st.sidebar.slider("Max Tokens", min_value=100, max_value=3000, step=100, value=500)

            if st.button("Submit"):
                response = self.completion_api.get_completion_from_messages(messages)
                # st.markdown(f"<span style='color: #1E90FF;'>{response}</span>", unsafe_allow_html=True)
                st.write('Response:')
                st.markdown(f"<div style='background-color: #F0FFF0; border: 1px solid #98FB98; padding: 10px;'><span style='color: #1E90FF;'>{response}</span></div>", unsafe_allow_html=True)


    def main(self):
        st.set_page_config(page_title="OpenAI LLM Classification App", page_icon=":robot_face:")
        st.title("OpenAI LLM Classification App")

        st.sidebar.markdown("""
        ### OpenAI Evaluation App

        This app uses the OpenAI GPT-3.5 turbo model to classify customer service queries into primary and secondary categories. 
        
        To get started, enter your OpenAI API key in the sidebar and specify the delimiter symbol that will be used to separate the message from the system message. 
        
        Then enter a message in the input box and click the "Submit" button to generate a response. The response will include the primary and secondary categories that the message belongs to, and will be displayed in a highlighted box on the page. 
        """)
        st.sidebar.write("---")

        open_api_key = self.get_openai_api_key()

        if open_api_key:
            self.completion_api = OpenAICompletion(open_api_key)
        
        else:
            st.error("Please enter your OpenAI API key in the sidebar.")

        
        with st.expander("System Message"):
            delimiter = st.text_input("Enter the delimiter symbol:", value="####")
            system_message = st.text_area("Enter the system message:", value=f"""
            You will be provided with customer service queries.
            The customer service query will be delimited with {delimiter} characters.
            Classify each query into a primary category and a secondary category. 
            Provide your output in json format with the keys: primary and secondary.

            Primary categories: Billing, Technical Support, Account Mangement, or General Inquiry.

            Billing secondary categories:
            Unsubscribe or upgrade 
            Add a payment method 
            Explanation for charge 
            Dispute a charge

            Technical Support secondary categories:
            General troubleshooting
            Device compatibility
            Software updates 

            Account Management secondary categories:
            Password reset
            Update personal information
            Close account 
            Account security 

            General Inquiry secondary categories: 
            Product information
            Pricing 
            Feedback
            Speak to a human
            """, height=500)

        self.get_user_input(delimiter, system_message)


if __name__ == "__main__":
    app = OpenAIApp()
    app.main()