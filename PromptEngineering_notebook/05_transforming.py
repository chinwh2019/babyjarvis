#!/usr/bin/env python3
# coding: utf-8

# We explore how to use LLMs for text transformation tasks such as language translation, spelling and grammar checking, tone adjustment, and format conversion. 

# %% 
import openai
import os 

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")
# %%
def get_completion(prompt, model="gpt-3.5-turbo"): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

# %%
# Translation 
# ChatGPT is trained with sources in many languages. 
# This gives the model the ability to do trnslation. 
# HEre are some examples of hwo to use this capability. 

prompt = f"""
Translate the following English text to Japanese: \ 
'''Hi, I would like to order a blender.'''
"""

response = get_completion(prompt)
print(response)
# %%
prompt = f"""
Tell me which language this is: 
'''Combien coûte le lampadaire?'''
"""

response = get_completion(prompt)
print(response)

# %%
prompt = f"""
Translate the following text to French and Japanese and English pirate: \ 
'''I want to order a basketball'''
"""

response = get_completion(prompt)
print(response)

# %%
prompt = f"""
Translate the following text to Japanese in both the \ 
formal and informal forms:
'Would you like to order a pillow?'
"""

response = get_completion(prompt)
print(response)

# %%
# Universal Translator 
# Imagine you are in charge of IT at a large multinational e-commerce company. 
# Users are messaging you with IT issues in all their native languages. 
# You staff is from all over the world and speaks only their native languages. 
# You need a universal translator! 

user_messages = [
  "La performance du système est plus lente que d'habitude.",  # System performance is slower than normal         
  "Mi monitor tiene píxeles que no se iluminan.",              # My monitor has pixels that are not lighting
  "Il mio mouse non funziona",                                 # My mouse is not working
  "私のキーボードのコントロールキーが壊れています",                                      # My keyboard has a broken control key
  "我的屏幕在闪烁" 
] 
# %%
for issue in user_messages:
    prompt = f"Tell me what language this is: '''{issue}'''"
    language = get_completion(prompt)
    print(f"Original message {language}: {issue}")

    prompt = f"""
    Translate the following text to English \ 
    and Malay: '''{issue}'''
    """
    response = get_completion(prompt)
    print(response, '\n')
# %%
# Tone Transformation 
# Writing can vary based on the intended audience. ChatGPT can produce different tones. 

prompt = f"""
Translate the following from slang to a business letter:
'Dude, This is Joe, check out this spec on this standing lamp.'
"""

response = get_completion(prompt)
print(response)

# %%
# Format Conversion
# ChatGPT can convert text from one format to another.
# The prompt should describe the inptu and output formats.

data_json = { "resturant employees" :[ 
    {"name":"Shyam", "email":"shyamjaiswal@gmail.com"},
    {"name":"Bob", "email":"bob32@gmail.com"},
    {"name":"Jai", "email":"jai87@gmail.com"}
]}

prompt = f"""
Translate the following python dictionary from JSON to HTML \ 
table with column headers and title: {data_json}
"""

response = get_completion(prompt)
print(response)

# %%
# Spellcheck/ Grammar check 
# Here are some examples of common grammar and spelling problems and the LLM's response.
# To signal to the LLM that you want it to proofread your text, you instruct the model to 'proofread' or 'proofread and correct'. 

text = [ 
  "The girl with the black and white puppies have a ball.",  # The girl has a ball.
  "Yolanda has her notebook.", # ok
  "Its going to be a long day. Does the car need it’s oil changed?",  # Homonyms
  "Their goes my freedom. There going to bring they’re suitcases.",  # Homonyms
  "Your going to need you’re notebook.",  # Homonyms
  "That medicine effects my ability to sleep. Have you heard of the butterfly affect?", # Homonyms
  "This phrase is to cherck chatGPT for speling abilitty"  # spelling
]

for t in text:
    prompt = f"""Proofread and correct the following text
    and rewrite the corrected version. If you don't find
    and errors, just say "No errors found". Don't use 
    any punctuation around the text:
    ```{t}```"""
    response = get_completion(prompt)
    print(response)
