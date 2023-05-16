#!/usr/bin/env python3
# coding: utf-8

import os
import streamlit as st
import base64
from config import get_page_config

# Function to load and display the Markdown content of a selected subpage
def load_description(selected_subpage):
    description_path = os.path.join("descriptions", f"{selected_subpage}.md")

    if os.path.exists(description_path):
        with open(description_path, "r") as f:
            md_contents = f.read()
            st.markdown(md_contents)
    else:
        st.error(f"No description found for the selected subpage: {selected_subpage}")

# Main app function
def main():
    # Set page title and favicon
    st.set_page_config(page_title="One-stop NLP Home Page", page_icon=":memo:")

    # Display the main title with an image icon
    icon_path = os.path.join("img", "logo.png")
    icon_base64 = None

    if os.path.exists(icon_path):
        with open(icon_path, "rb") as img_file:
            icon_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        custom_title = f"""
        <div style="display: flex; align-items: center; font-size: 2em; font-weight: bold;">
            <img src="data:img/png;base64,{icon_base64}" style="width: 50px; margin-right: 10px;"/>
            One-stop NLP Home Page
        </div>
        """
        st.markdown(custom_title, unsafe_allow_html=True)
    else:
        st.title("One-stop NLP Home Page")

    # Get the list of subpages from the 'pages' folder
    # subpages = [f[:-3] for f in os.listdir("pages") if f.endswith(".py")]
    subpages = [f[:-3] for f in os.listdir("descriptions") if f.endswith(".md")]

    # Create a sidebar with a title and a selectbox to choose subpages
    st.sidebar.title("Description of Subpages")
    selected_subpage = st.sidebar.selectbox("Choose a subpage:", subpages)

    # Add a divider to separate the sidebar title and the selectbox
    st.sidebar.markdown("---")

    # Load and display the selected subpage's description using a Markdown file
    load_description(selected_subpage)


# Run the app
if __name__ == "__main__":
    main()
