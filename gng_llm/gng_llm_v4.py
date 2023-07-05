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

class ModelManager:
    def __init__(self, model_path='all-MiniLM-L6-v2', openai_key_env="OPENAI_API_KEY", n_neighbors=3):
        load_dotenv(find_dotenv())
        openai.api_key = os.getenv(openai_key_env)
        self.scaler = MinMaxScaler()
        self.knn = KNeighborsClassifier(n_neighbors=n_neighbors)
        self.model = self.load_model(model_path)
        self.reducer = umap.UMAP(random_state=42)
        
    @staticmethod
    def load_model(model_path):
        try:
            model = SentenceTransformer(model_path)
            logger.info("Loaded SentenceTransformer model.")
        except Exception as e:
            logger.error(f"Failed to load SentenceTransformer model. Error: {str(e)}")
            model = None
        return model

class MemoryManager:
    def __init__(self):
        self.memory = {}

    def add_to_memory(self, user, message):
        if user not in self.memory:
            self.memory[user] = []
        self.memory[user].append({"role": "user", "content": message})
        return self.memory[user]

class ChatBot:
    def __init__(self, memory_manager, model_manager):
        self.memory_manager = memory_manager
        self.model_manager = model_manager
        self.moods = {0: "neutral", 1: "happy", 2: "anxious", 3: "curious", 4: "sad"}

    def chat_with_gpt(self, message, mood, user):
        memory = self.memory_manager.add_to_memory(user, message)
        system_message = self.generate_system_message(memory, mood)
        messages = self.generate_messages(memory, message, system_message)
        print("TEST: ", messages)
        try:
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            return response.choices[0].message['content']
        except Exception as e:
            logger.error(f"Failed to get response from GPT-3. Error: {str(e)}")

    @staticmethod
    def generate_system_message(memory, mood):
        if len(memory) > 1:
            past_messages = [mem['content'] for mem in memory[:-1]][-5:]
            system_message = f"You are a helpful assistant. The user seems {mood}. They have previously talked about: {', '.join(past_messages)}."
        else:
            system_message = f"You are a helpful assistant. The user seems {mood}."
        return system_message

    @staticmethod
    def generate_messages(memory, message, system_message):
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": message}]
        messages.extend([{"role": "user", "content": mem['content']} for mem in memory[-5:]])
        return messages

class FeedbackManager:
    def __init__(self):
        self.gpt_responses = []
        self.feedback_scores = []

    def generate_responses(self, diary_entries, user, chat_bot, model_manager):
        embeddings, scaled_embeddings = self._get_scaled_embeddings(diary_entries, model_manager)
        model_manager.knn.fit(scaled_embeddings, [i % len(chat_bot.moods) for i in range(len(scaled_embeddings))])

        with open("features.pkl", "wb") as f:
            pickle.dump(scaled_embeddings, f)

        for i, entry in enumerate(diary_entries):
            self._generate_response(i, entry, user, chat_bot, model_manager, scaled_embeddings)
            
        self._print_responses_and_feedback(diary_entries)

    def _get_scaled_embeddings(self, diary_entries, model_manager):
        embeddings = [model_manager.model.encode([entry])[0] for entry in diary_entries]
        scaled_embeddings = model_manager.scaler.fit_transform(embeddings)
        return embeddings, scaled_embeddings

    def _generate_response(self, i, entry, user, chat_bot, model_manager, scaled_embeddings):
        scaled_entry = scaled_embeddings[i].reshape(1, -1)
        knn_cluster = model_manager.knn.predict(scaled_entry)
        mood = chat_bot.moods[knn_cluster[0]]
        response = chat_bot.chat_with_gpt(entry, mood, user)

        logger.info(f"Diary Entry {i+1}: {entry}")
        logger.info(f"GPT-3 Response {i+1}: {response}")

        feedback_score = int(input("Rate the response from 1 (not helpful) to 5 (very helpful):\n"))
        while feedback_score <= 2:
            logger.info("I'm sorry you didn't find my response helpful. Let me try again.")
            response = chat_bot.chat_with_gpt(entry + " The previous response was not helpful.", mood, user)
            logger.info(f"New GPT-3 Response: {response}")
            feedback_score = int(input("Rate the new response from 1 (not helpful) to 5 (very helpful):\n"))

        self.gpt_responses.append(response)
        self.feedback_scores.append(feedback_score)

    def _print_responses_and_feedback(self, diary_entries):
        for i, (response, score) in enumerate(zip(self.gpt_responses, self.feedback_scores)):
            logger.info(f"Diary Entry {i+1}: {diary_entries[i]}")
            logger.info(f"GPT-3 Response {i+1}: {response}")
            logger.info(f"Feedback Score {i+1}: {score}\n")


if __name__ == "__main__":
    model_manager = ModelManager()
    memory_manager = MemoryManager()
    chat_bot = ChatBot(memory_manager, model_manager)
    feedback_manager = FeedbackManager()

    diary_entries = [
        "I used to love gardening but I stopped because I'm afraid of falling.", 
        "I watched a gardening show today and felt good.", 
        "I wish I could garden again but don't know where to start."
    ]
    user = "user1"

    feedback_manager.generate_responses(diary_entries, user, chat_bot, model_manager)
