import os 
import json 

from app.db import Session, Pizza, Order, Review 
from app.prompts import QA_PROMPT
from app.store import get_vectorstore

from langchain.llms import OpenAI 
from langchain.chains import RetrievalQA


def get_pizza_info(pizza_name: str):
    session = Session()
    pizza = session.query(Pizza).filter(Pizza.name == pizza_name).first()
    session.close()
    if pizza:
        return json.dumps(pizza.to_json())
    else:
        return "Pizza not found."
    

def create_order(pizza_name: str):
    session = Session()
    pizza = session.query(Pizza).filter(Pizza.name == pizza_name).first()
    if pizza:
        order = Order(pizza=pizza)
        session.add(order)
        session.commit()
        session.close()
        return "Order created."
    else:
        session.close()
        return "Pizza not found."
    

def create_review(review_text: str):
    session = Session()
    review = Review(review=review_text)
    session.add(review)
    session.commit()
    session.close()
    return "Review created."


def ask_vector_db(question: str):
    llm = OpenAI(openai_api_key=os.environ.get('OPENAI_API_KEY'))
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=get_vectorstore().as_retriever(),
        chain_type_kwargs={'prompt': QA_PROMPT}
    )
    result = qa.run(question)
    return result 


api_functions = {
    'create_review': create_review,
    'create_order': create_order,
    'get_pizza_info': get_pizza_info,
    'ask_vector_db': ask_vector_db
}


# Initialization 
def create_pizzas():
    session = Session()

    pizzas = {
        'Margherita': 10.99,
        'Pepperoni': 12.99,
        'BBQ Chicken': 13.99,
        'Hawaiian': 11.99,
        'Vegetarian': 11.99,
        'Buffalo': 9.99,
        'Supreme': 14.99,
        'Meat Lovers': 15.99,
        'Taco': 8.99,
        'Seafood': 16.99,
    }

    for name, price in pizzas.items():
        pizza = Pizza(name=name, price=price)
        session.add(pizza)

    session.commit()
    session.close()

