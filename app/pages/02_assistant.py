#!/usr/bin/env python3
# coding: utf-8

import streamlit as st
import openai
import streamlit.components.v1 as components
from utils import get_openai_api_key, get_api_key_from_config

# openai.api_key = get_openai_api_key()
openai.api_key = get_api_key_from_config()


def generate_text(prompt: str) -> str:
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": "You are a friendly and help AI assistant."}]

    messages = st.session_state["messages"]
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    content = response["choices"][0]["message"]["content"]
    total_tokens = response["usage"]["total_tokens"]
    messages.append({"role": "assistant", "content": content})
    if total_tokens > 3000:
        messages.pop(1)
        messages.pop(1)

    return content


# def scroll_to_bottom():
#     js = "window.onload = () => window.scrollTo(0, document.body.scrollHeight);"
#     # js = "window.onload = () => alert('scroll_to_bottom');"
#
#     html = "<script>{}</script>".format(js)
#
#     components.html(
#         html,
#         height=0
#     )


def main():
    # scroll_to_bottom()
    st.title("🤖 A.I. Personal Assistant")

    if "prompts" not in st.session_state:
        st.session_state["prompts"] = []
    if "contents" not in st.session_state:
        st.session_state["contents"] = []
    prompts = st.session_state["prompts"]
    contents = st.session_state["contents"]

    for p, c in zip(prompts, contents):
        st.success(p)
        st.info(c)

    prompt = st.text_area("prompt", key="prompt").strip()

    def call_generate_text():
        if prompt == "":
            return
        prompts.append(prompt)
        content = generate_text(prompt)
        contents.append(content)
        st.session_state["prompt"] = ""

    st.button("SEND", on_click=call_generate_text)


if __name__ == "__main__":
    main()
