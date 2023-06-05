import streamlit as st 
import openai
from utils import * 

"""
Assuming the role of a pediatric nutritionist and a skillful cook.
generate a breakfast recipe that caters to the preferences and dietary needs of a 3-4 years old child. 
The child prefers chicken and is allergic to dairy products. 
The recipe should be void of any religious or cultural food restrictions and should be adaptable to any cuisine, whether Asian, Western, or others. The cooking method can be varied, including but not limited to baking, grilling, or steaming. Emphasize the inclusion of key nutrients, such as proteins, vitamins, and fiber, and ensure the recipe is easy to prepare, time-efficient, and suitable for a busy morning routine. In addition to being tasty, make sure the meal is visually appealing and incorporates elements of fun or education to engage the child. The final dish could be creatively named to further attract the child's interest. Provide the recipe in the following format:

Food name
Ingredients
Instructions
Nutritional benefits
Cautions
"""
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
        return response.choices[0].message['content']
    

class System:
    def __init__(self, label, system_message, predefined_input, delimiter="####"):
        self.label = label 
        self.system_message = system_message
        self.predefined_input = predefined_input
        self.delimiter = delimiter
    
    def get_messages(self, system_message, user_message):
        delimiter = self.delimiter
        system_message = system_message.format(delimiter=delimiter)
        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"{delimiter} {user_message} {delimiter}"},
        ]
    
    def render(self, completion_api, temperature, max_tokens):
        # with st.expander(self.label):
            # delimiter = st.text_input("Enter the delimiter symbol", self.delimiter)
            # system_message = st.text_area("Enter the system message:", value=self.system_message.format(delimiter=delimiter), height=200, key=self.label+"_system_message")
        predefined_input = self.predefined_input.replace(self.delimiter, '')
            # user_message = st.text_input("Enter your message:", value=predefined_input, key=self.label+"_message_input")

        messages = self.get_messages(self.system_message, predefined_input)

        if st.button("Generate", key=self.label+"_generate"):
            with st.spinner("Generating..."):
                response = completion_api.get_completion_from_messages(messages, temperature=temperature, max_tokens=max_tokens)
                st.write('Response:')
                st.success(response)
                # st.markdown(f"<div style='background-color: #F0FFF0; border: 1px solid #98FB98; padding: 10px;'><span style='color: #1E90FF;'>{response}</span></div>", unsafe_allow_html=True)


class OpenAIApp:
    def __init__(self):
        self.completion_api = None 

    def get_openai_api_key(self):
        if 'api_key' not in st.session_state:
            api_key_from_config = get_api_key_from_config()
            if api_key_from_config: 
                st.session_state.api_key = api_key_from_config
            else:
                st.session_state.api_key = ""
        
        return st.sidebar.text_input(
            "Enter your OpenAI API key",
            value=st.session_state.api_key,
            placeholder="Enter your OpenAI API key",
            type="password",
        )
    
    def main(self):
        st.title("Kid Food Generator")
        st.write("---")        
        description = """
        This is a AI food generator for kids. 
        Use as your own risk. 
        """
        st.markdown(description, unsafe_allow_html=True)
        st.write("---")

        open_api_key = self.get_openai_api_key()

        if open_api_key:
            self.completion_api = OpenAICompletion(open_api_key)
        else:
            st.error("Please enter your OpenAI API key in the sidebar.")


        temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=2.0, step=0.1, value=1.0)
        max_tokens = st.sidebar.slider("Max Tokens", min_value=10, max_value=3000, step=1, value=1000)
        
        # define system messages and predefined inputs 
        system_messages = load_text_file("assets/food_generator_system_message2.txt")
        child_age = st.text_input("Enter the child age:")
        child_preference = st.text_input("Enter the child preference:", value="Any")
        child_allergy = st.text_input("Enter the child allergy:", value=None)
        regional_cuisine = st.text_input("Enter the regional cuisine:", "Any")
        request = st.text_input("Enter the special request:", value=None)
        meal_type = st.selectbox("Enter the meal type:", options=["breakfast", "lunch", "dinner", "snack"])
        
        predefined_input = f"""
        child age:{child_age}years old, 
        preference:{child_preference}, 
        allergy:{child_allergy}, 
        food region:{regional_cuisine}, 
        special request:{request},
        meal:{meal_type}"""
        print(predefined_input)
        
        child_generator = System("Child Food Generator", system_messages, predefined_input)
        child_generator.render(self.completion_api, temperature, max_tokens)


if __name__ == "__main__":
    app = OpenAIApp()
    app.main()

            



    

