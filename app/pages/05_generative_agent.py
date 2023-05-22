import streamlit as st
from langchain.experimental.generative_agents import GenerativeAgent, GenerativeAgentMemory
from langchain.chat_models import ChatOpenAI
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain.vectorstores import FAISS
import openai 
import os 
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
import math
import faiss

_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

observations = [
    "Tommie wakes up to the sound of a noisy construction site outside his window.",
    "Tommie gets out of bed and heads to the kitchen to make himself some coffee.",
    "Tommie realizes he forgot to buy coffee filters and starts rummaging through his moving boxes to find some.",
    "Tommie finally finds the filters and makes himself a cup of coffee.",
    "The coffee tastes bitter, and Tommie regrets not buying a better brand.",
    "Tommie checks his email and sees that he has no job offers yet.",
    "Tommie spends some time updating his resume and cover letter.",
    "Tommie heads out to explore the city and look for job openings.",
    "Tommie sees a sign for a job fair and decides to attend.",
    "The line to get in is long, and Tommie has to wait for an hour.",
    "Tommie meets several potential employers at the job fair but doesn't receive any offers.",
    "Tommie leaves the job fair feeling disappointed.",
    "Tommie stops by a local diner to grab some lunch.",
    "The service is slow, and Tommie has to wait for 30 minutes to get his food.",
    "Tommie overhears a conversation at the next table about a job opening.",
    "Tommie asks the diners about the job opening and gets some information about the company.",
    "Tommie decides to apply for the job and sends his resume and cover letter.",
    "Tommie continues his search for job openings and drops off his resume at several local businesses.",
    "Tommie takes a break from his job search to go for a walk in a nearby park.",
    "A dog approaches and licks Tommie's feet, and he pets it for a few minutes.",
    "Tommie sees a group of people playing frisbee and decides to join in.",
    "Tommie has fun playing frisbee but gets hit in the face with the frisbee and hurts his nose.",
    "Tommie goes back to his apartment to rest for a bit.",
    "A raccoon tore open the trash bag outside his apartment, and the garbage is all over the floor.",
    "Tommie starts to feel frustrated with his job search.",
    "Tommie calls his best friend to vent about his struggles.",
    "Tommie's friend offers some words of encouragement and tells him to keep trying.",
    "Tommie feels slightly better after talking to his friend.",
]

def relevance_score_fn(score: float) -> float:
    """Return a similarity score on a scale [0, 1]."""
    # This will differ depending on a few things:
    # - the distance / similarity metric used by the VectorStore
    # - the scale of your embeddings (OpenAI's are unit norm. Many others are not!)
    # This function converts the euclidean norm of normalized embeddings
    # (0 is most similar, sqrt(2) most dissimilar)
    # to a similarity function (0 to 1)
    return 1.0 - score / math.sqrt(2)

def create_new_memory_retriever():
        embeddings_model = OpenAIEmbeddings()
        embedding_size = 1536
        index = faiss.IndexFlatL2(embedding_size)
        vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {}, relevance_score_fn=relevance_score_fn)
        return TimeWeightedVectorStoreRetriever(vectorstore=vectorstore, other_score_keys=["importance"], k=15)    

def main():
    st.title("Simulation Agent")

    try:
        st.image("assets/simulation.png", use_column_width=True)
        st.caption("Credit to [https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)")
    except FileNotFoundError:
        pass

    try:
        st.image("assets/memory.png", use_column_width=True)
        # st.caption("Credit to [https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)")
    except FileNotFoundError:
        pass

    USER_NAME = st.text_input("Enter your name", "Jayden Chin")
    LLM = ChatOpenAI(max_tokens=1500)

    

    tommies_memory = GenerativeAgentMemory(
        llm=LLM,
        memory_retriever=create_new_memory_retriever(),
        verbose=False,
        reflection_threshold=8 
    )

    tommie = GenerativeAgent(name="Tommie", 
                  age=25,
                  traits="anxious, likes design, talkative",
                  status="looking for a job",
                  memory_retriever=create_new_memory_retriever(),
                  llm=LLM,
                  memory=tommies_memory
                 )

    input_text = st.text_input("Ask Tommie a question:")
    if st.button('Submit'):
        new_message = f"{USER_NAME} says {input_text}"
        with st.spinner('Waiting agent response...'):
            response = tommie.generate_dialogue_response(new_message)[1]
            st.write(response)
    st.write("---")

    # observation_text = st.text_input("Add an observation for Tommie:")
    observation_text = st.selectbox("Choose an observation for Tommie:", observations)
    st.write(observation_text)
    st.write("---")
    if st.button('Add Observation'):
        with st.spinner('Observation added, waiting agent response...'):
            _, reaction = tommie.generate_reaction(observation_text)
            st.write(f"Tommie's reaction: {reaction}")

if __name__ == "__main__":
    main()
