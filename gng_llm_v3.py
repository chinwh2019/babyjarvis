import os
import pickle
import logging
from dotenv import load_dotenv, find_dotenv
from sklearn.neighbors import KNeighborsClassifier
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import MinMaxScaler
import umap.umap_ as umap
import openai
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API key
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up SentenceTransformer for text embeddings
model_path = 'all-MiniLM-L6-v2'
try:
    model = SentenceTransformer(model_path)
    logger.info("Loaded SentenceTransformer model.")
except Exception as e:
    logger.error(f"Failed to load SentenceTransformer model. Error: {str(e)}")

# Preprocessing scaler
scaler = MinMaxScaler()

# Initialize KNN model
knn = KNeighborsClassifier(n_neighbors=3)

# Initialize UMAP reducer
reducer = umap.UMAP(random_state=42)

# Initialize moods dict
moods = {0: "neutral", 1: "happy", 2: "anxious", 3: "curious", 4: "sad"}

# Initialize memory dict
memory = {}

def chat_with_gpt(message, mood, user):
    # Add a new key for the user if they don't exist in memory
    if user not in memory:
        memory[user] = []

    # Add the new message to the user's memory
    memory[user].append({"role": "user", "content": message})

    # Construct system message
    if len(memory[user]) > 1:
        # If the user has past messages, reflect on them in the system message
        past_messages = [mem['content'] for mem in memory[user][:-1]][-5:]  # get the last five messages
        system_message = f"You are a helpful assistant. The user seems {mood}. They have previously talked about: {', '.join(past_messages)}."
    else:
        # If this is the user's first message, the system message is more generic
        system_message = f"You are a helpful assistant. The user seems {mood}."

    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": message}]

    # Add the messages in the user's memory to the messages sent to the LLM
    messages.extend([{"role": "user", "content": mem['content']} for mem in memory[user][-5:]])  # get the last five messages

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=messages
        )
        return response.choices[0].message['content']
    except Exception as e:
        logger.error(f"Failed to get response from GPT-3. Error: {str(e)}")


def generate_responses(diary_entries, user):
    embeddings = []
    gpt_responses = []
    feedback_scores = []

    for entry in diary_entries:
        # Get embedding for the entry
        entry_embedding = model.encode([entry])[0]
        embeddings.append(entry_embedding)

    # Fit the scaler on all embeddings and transform
    scaled_embeddings = scaler.fit_transform(embeddings)

    # Fit the KNN model on all embeddings
    knn.fit(scaled_embeddings, [i % len(moods) for i in range(len(scaled_embeddings))])

    # Save features and embeddings for future use
    with open("features.pkl", "wb") as f:
        pickle.dump(scaled_embeddings, f)

    # Now use the KNN model to predict moods and generate responses
    for i, entry in enumerate(diary_entries):
        scaled_entry = scaled_embeddings[i].reshape(1, -1)  # reshape to 2D as required by KNN

        # Get the closest KNN node (i.e., "mood") for the entry
        knn_cluster = knn.predict(scaled_entry)

        # Use the moods dict to get the mood string
        mood = moods[knn_cluster[0]]

        # Get GPT-3 response with the mood as an input
        response = chat_with_gpt(entry, mood, user)

        # Print the GPT-3 response
        logger.info(f"Diary Entry {i+1}: {entry}")
        logger.info(f"GPT-3 Response {i+1}: {response}")

        # Collect feedback
        feedback_score = int(input("Rate the response from 1 (not helpful) to 5 (very helpful):\n"))

        # If the feedback score is low, generate a new response
        while feedback_score <= 2:  # change the threshold as needed
            logger.info("I'm sorry you didn't find my response helpful. Let me try again.")

            response = chat_with_gpt(entry + " The previous response was not helpful.", mood, user)
            logger.info(f"New GPT-3 Response: {response}")

            feedback_score = int(input("Rate the new response from 1 (not helpful) to 5 (very helpful):\n"))

        gpt_responses.append(response)
        # Collect feedback
        feedback_scores.append(feedback_score)

    # Print the GPT-3 responses and feedback scores
    for i, (response, score) in enumerate(zip(gpt_responses, feedback_scores)):
        logger.info(f"Diary Entry {i+1}: {diary_entries[i]}")
        logger.info(f"GPT-3 Response {i+1}: {response}")
        logger.info(f"Feedback Score {i+1}: {score}\n")

# Save trained models
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
with open("knn.pkl", "wb") as f:
    pickle.dump(knn, f)
with open("sentence_transformer.pkl", "wb") as f:
    pickle.dump(model, f)

# User's diary entries and corresponding GPT-3 responses
diary_entries = [
    "I used to love gardening but I stopped because I'm afraid of falling.", 
    "I watched a gardening show today and felt good.", 
    "I wish I could garden again but don't know where to start."
]
user = "user1"  # replace this with the name or ID of the user

generate_responses(diary_entries, user)
