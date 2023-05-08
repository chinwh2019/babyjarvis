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
                    st.markdown(f'<strong>{response}</strong>', unsafe_allow_html=True)


        # Other examples can be added as expanders in a similar fashion
        with st.expander("Tactic 2: Ask for a structured output - JSON, HTML"):
            st.markdown("""In this example, we can ask the model to output a structured response, such as JSON or HTML.""")
            
            preset_prompt = f"""Generate a list of three made-up book titles along with their authors and genres. 
            Provide them in JSON format with the following keys: book_id, title, author, genre."""

            prompt = st.text_area(
                "Tactic 2 prompt:",
                value=preset_prompt,
                key="tactic2_prompt_input",
                height=200,
            )

            if st.button("Run Tactic 2 Example"):
                with st.spinner("Running..."):
                    response = self.completion_api.get_completion(prompt)
                    st.subheader("Response")
                    st.markdown(f'<strong>{response}</strong>', unsafe_allow_html=True)

        with st.expander("Tactic 3: Ask the model to check wether conditions are satisfied"):
            st.markdown("""In this example, we can ask the model to check wether conditions are satisfied.""")

            preset_text = """Making a cup of tea is easy! First, you need to get some 
            water boiling. While that's happening, 
            grab a cup and put a tea bag in it. Once the water is 
            hot enough, just pour it over the tea bag.  
            Let it sit for a bit so the tea can steep. After a  
            few minutes, take out the tea bag. If you  
            like, you can add some sugar or milk to taste.  
            And that's it! You've got yourself a delicious  
            cup of tea to enjoy."""

            text = st.text_area(
                "Enter text for Tactic 3:",
                value=preset_text,
                placeholder="Your text",
                key="tactic3_text_input",
                height=200,
            )

            preset_prompt = f"""
            You will be provided with text delimited by triple quotes. 
            If it contains a sequence of instructions, 
            re-write those instructions in the following format:

            Step 1 - ...
            Step 2 - ...
            ...
            Step N - ...

            If the text does not contain a sequence of instructions, 
            then simply write \"No steps provided.\"

            '''{text}'''
            """

            prompt = st.text_area(
                "Tactic 3 prompt:",
                value=preset_prompt,
                key="tactic3_prompt_input",
                height=200,
            )

            if st.button("Run Tactic 3 Example"):
                with st.spinner("Running..."):
                    response = self.completion_api.get_completion(prompt)
                    st.subheader("Response")
                    st.markdown(f'<strong>{response}</strong>', unsafe_allow_html=True)

        with st.expander("Tactic 4: 'Few shot' prompting"):
            st.markdown("""In this example, we give some examples of the desired output to the model, and ask it to generalize to new examples.""")

            preset_prompt = f"""
            Your task is to answer in a consistent style. 

            <child>: Teach me about patience. 

            <grandparent>: The river that carves the deepest valley fllows from a modest spring; the grandest symphony originates from a single note; 
            the most intricate tapestry begines with a solitary thread. 

            <child>: Teach me about resilience.
            """
            
            prompt = st.text_area(
                "Tactic 4 prompt:",
                value=preset_prompt,
                key="tactic4_prompt_input",
                height=200,
            )

            if st.button("Run Tactic 4 Example"):
                with st.spinner("Running..."):
                    response = self.completion_api.get_completion(prompt)
                    st.subheader("Response")
                    st.markdown(f'<strong>{response}</strong>', unsafe_allow_html=True)

        
        with st.expander("Tactic 5: Give the model time to 'think'"):
            st.markdown("""In example 1, we specify the steps required to complete a task to guide the model towards the desired output.
            In example 2, we ask the model to perform a series of actions, and then output a JSON object containing the results.""")

            preset_text = """In a charming village, siblings Jack and Jill set out on
            a quest to fetch water from a hilltop
            well. As the climbed, singing joyfully, misfortune 
            struck-Jack tripped on a stone and tumbled 
            down the hill, with Jill following suit. 
            Though slightly battered, the pair returned home to 
            comforting embraces. Despite the mishap, 
            their adventurous spirits remained undimeed, and they 
            continued exploring with delight. 
            """

            text = st.text_area(
                "Enter text for Tactic 5:",
                value=preset_text,
                placeholder="Your text",
                key="tactic5_text_input",
                height=200,
            )

            preset_prompt = f"""
            Perform the following actions:
            1 - Summarize the following text delimited by triple backticks with 1 sentence 
            2 - Translate the summary into Japanese 
            3 - List each name in the Japanese summary. 
            4 - Output a json object that contains the following keys: japanese_summary, num_names 

            Seperate your answers with line breaks. 

            Text: 
            ```{text}```
            """

            prompt = st.text_area(
                "Tactic 5 prompt 1:",
                value=preset_prompt,
                key="tactic5_prompt_input",
                height=200,
            )

            preset_prompt_2 = f"""
            You task is to perform the following actions: 
            1 - Summarize the following text delimited by <> with 1 sentence. 
            2 - Translate the summary into French. 
            3 - List each name in the French summary. 
            4 - Output a json object that contains the following keys: french_summary, num_names.


            Use the following format: 
            Text: <text to summarize> line breaks
            Summary: <summary> line breaks
            Translation: <summary translation> line breaks
            Names: <list of names in Italian summary> line breaks
            Output JSON: <json with summary and num_names> line breaks

            Text: <{text}>
            """

            prompt_2 = st.text_area(
                "Tactic 5 prompt 2:",
                value=preset_prompt_2,
                key="tactic5_prompt_input_2",
                height=200,
            )

            if st.button("Run Tactic 5 Example 1"):
                with st.spinner("Running..."):
                    response = self.completion_api.get_completion(prompt)
                    st.subheader("Response")
                    st.markdown(f'<strong>{response}</strong>', unsafe_allow_html=True)

            if st.button("Run Tactic 5 Example 2"):
                with st.spinner("Running..."):
                    response = self.completion_api.get_completion(preset_prompt_2)
                    st.subheader("Response")
                    st.markdown(f'<strong>{response}</strong>', unsafe_allow_html=True)

        with st.expander("Tactic 6: Instruct the model to work out its own solution"):
            st.markdown("""In first example, we ask the model generate answer right away which is wrong answer (failed case). 
            In second example, we instruct the model to work out its own solution before rushing to a conclusion.""")

            preset_prompt = f"""
            Determine if the student's solution is correct or not. 

            Question: 
            I'm building a solar power installation and I need 
            help working out the financials. 
            - Land costs $100 / square foot
            - I can buy solar panels for $250 / square foot
            - I negotiated a contract for maintenance that will cost 
            me a flat $100k per year, and an additional $10 / square 
            foot
            What is the total cost for the first year of operations 
            as a function of the number of square feet.

            Student's Solution:
            Let x be the size of the installation in square feet.
            Costs:
            1. Land cost: 100x
            2. Solar panel cost: 250x
            3. Maintenance cost: 100,000 + 100x
            Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
            """

            prompt = st.text_area(
                "Tactic 6 prompt 1:",
                value=preset_prompt,
                key="tactic6_prompt_input",
                height=500,
            )

            preset_prompt_2 = f"""
            Your task is to determine if the student's solution is correct or not.
            To solve the problem do the following:
            - First, work out your own solution to the problem. 
            - Then compare your solution to the student's solution and evaluate if the student's solution is correct or not. 
            Don't decide if the student's solution is correct until you have done the problem yourself.

            Use the following format:
            Question:
            ```
            question here
            ```
            Student's solution:
            ```
            student's solution here
            ```
            Actual solution:
            ```
            steps to work out the solution and your solution here
            ```
            Is the student's solution the same as actual solution just calculated:
            ```
            yes or no
            ```
            Student grade:
            ```
            correct or incorrect
            ```

            Question:
            ```
            I'm building a solar power installation and I need help working out the financials. 
            - Land costs $100 / square foot
            - I can buy solar panels for $250 / square foot
            - I negotiated a contract for maintenance that will cost me a flat $100k per year, and an additional $10 / square foot
            What is the total cost for the first year of operations as a function of the number of square feet.
            ``` 
            Student's solution:
            ```
            Let x be the size of the installation in square feet.
            Costs:
            1. Land cost: 100x
            2. Solar panel cost: 250x
            3. Maintenance cost: 100,000 + 100x
            Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
            ```
            Actual solution:
            """

            prompt_2 = st.text_area(
                "Tactic 6 prompt 2:",
                value=preset_prompt_2,
                key="tactic6_prompt_input_2",
                height=500,
            )

            if st.button("Run Tactic 6 Example 1"):
                with st.spinner("Running..."):
                    response = self.completion_api.get_completion(prompt)
                    st.subheader("Response")
                    st.markdown(f'<strong>{response}</strong>', unsafe_allow_html=True)

            if st.button("Run Tactic 6 Example 2"):
                with st.spinner("Running..."):
                    response = self.completion_api.get_completion(prompt_2)
                    st.subheader("Response")
                    st.markdown(f'<strong>{response}</strong>', unsafe_allow_html=True)
    
    
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
