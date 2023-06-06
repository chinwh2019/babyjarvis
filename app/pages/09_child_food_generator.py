import streamlit as st 
import openai
from utils import * 

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
    
    def save_first_words(self, response):
        words = response.split()  # split the response into a list of words
        extracted_words = words[:7]  # select the first 50 words
        new_response = ' '.join(extracted_words)  # join the first 50 words back into a string
        return new_response

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
                short_response = self.save_first_words(response)
            with st.spinner("Generating food image:"):
                print(short_response)
                response = openai.Image.create(
                prompt="Reality magazine "+"food photography: "+ f"{short_response}",
                n=1,
                size="512x512"
                )
                image_url = response['data'][0]['url']
                st.image(image_url, width = 512)


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
        # description = """
        # The Kid Food Generator is an AI-powered tool that creates personalized, nutritious recipes based on a child's specific information like age, allergies, and preferences. 
        # Utilizing advanced algorithms and feedback learning, it tailors meal plans that promote healthy eating habits and joy of food from a young age. 
        # Please note, the generated recipes are for reference only, use them at your own discretion, and always consult with a healthcare provider for dietary advice.
        # """
        # st.markdown(description, unsafe_allow_html=True)

        # Displaying Sub-header
        st.subheader('Personalized Nutrition for Kids')

        # Displaying the Information
        st.markdown('The Kid Food Generator is a cutting-edge tool that leverages AI technology to:')
        st.write('- Craft **customized** recipes based on a child\'s unique data (age, allergies, preferences)')
        st.write('- Facilitate **healthy eating habits**')
        st.write('- Promote the **joy of food** from a young age')

        # Displaying the working mechanism
        st.subheader('How does it work?')
        st.markdown('The Kid Food Generator uses advanced algorithms and feedback learning mechanisms to tailor meal plans that both satisfy taste buds and provide nutritional balance.')

        # Displaying the disclaimer
        st.info('Disclaimer: The generated recipes are for reference only. Always use them at your own discretion and consult with a healthcare provider for dietary advice.')
        st.write("---")
        
        open_api_key = self.get_openai_api_key()

        if open_api_key:
            self.completion_api = OpenAICompletion(open_api_key)
        else:
            st.error("Please enter your OpenAI API key in the sidebar.")


        temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=2.0, step=0.1, value=1.0)
        max_tokens = st.sidebar.slider("Max Tokens", min_value=10, max_value=3000, step=1, value=1000)
        
        # define system messages and predefined inputs 
        system_messages = load_text_file("assets/food_generator_system_message3.txt")
        child_age = st.slider("Enter the child age:", 1, 99, 1)
        child_preference = st.text_input("Enter the child preference:", value="Any", max_chars=100)
        child_allergy = st.text_input("Enter the child allergy:", value=None, max_chars=100)
        regional_cuisine = st.text_input("Enter the regional cuisine:", "Any", max_chars=50)
        regional_cuisine = st.multiselect("Enter the regional cuisine:", options=["American", "Chinese", "French", "Indian", "Italian", "Japanese", "Korean", "Mexican", "Middle Eastern", "Thai", "Vietnamese", "Indonesia", "Malaysia"], default=["American", "Japanese"])
        request = st.text_input("Enter the special request:", value=None, max_chars=100)
        meal_type = st.selectbox("Enter the meal type:", options=["breakfast", "lunch", "dinner", "snack"])
        
        predefined_input = f"""
        The child age is {child_age} years old, 
        their preferences are {child_preference}, 
        and allergy is {child_allergy}, 
        The food recipe preference region is {regional_cuisine}, 
        Parent special request is {request},
        The recipe of the meal is for {meal_type}"""
        print(predefined_input)
        
        child_generator = System("Child Food Generator", system_messages, predefined_input)
        child_generator.render(self.completion_api, temperature, max_tokens)
        

if __name__ == "__main__":
    app = OpenAIApp()
    app.main()

            



    

