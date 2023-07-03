import os
import pickle
import logging
import numpy as np
from dotenv import load_dotenv, find_dotenv
from sklearn.neighbors import KNeighborsClassifier
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import MinMaxScaler
import umap.umap_ as umap
import openai
import torch 
import time 
from transformers import AutoTokenizer, RobertaForSequenceClassification


class EmotionDetector:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-emotion")
        self.model = RobertaForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-emotion")

    def get_emotion(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**inputs).logits
        predicted_class_id = logits.argmax().item()
        return self.model.config.id2label[predicted_class_id]

# The rest of your code starts here...
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ... truncated for brevity ...
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

class AdvancedMemoryManager:
    def __init__(self, learning_rate=0.5, similarity_threshold=0.8, decay_rate=0.1):
        self.nodes = []
        self.learning_rate = learning_rate
        self.similarity_threshold = similarity_threshold
        self.decay_rate = decay_rate

    def add_to_memory(self, feature_vector, message):
        similar_node = self.find_similar_node(feature_vector)
        if similar_node:
            self.update_node(similar_node, feature_vector, message)
        else:
            self.create_new_node(feature_vector, message)

    def find_similar_node(self, feature_vector):
        most_similar_node = None
        highest_similarity = -1

        for node in self.nodes:
            similarity = self.calculate_similarity(feature_vector, node['feature_vector'])
            if similarity > highest_similarity:
                highest_similarity = similarity
                most_similar_node = node

        return most_similar_node

    def calculate_similarity(self, node_feature_vector, feature_vector):
        return np.dot(node_feature_vector, feature_vector) / (np.linalg.norm(node_feature_vector) * np.linalg.norm(feature_vector))

    def update_node(self, node, feature_vector, message):
        node['feature_vector'] = (1 - self.learning_rate) * node['feature_vector'] + self.learning_rate * feature_vector
        if len(node['messages']) >= 5:
            node['messages'].pop(0)
        node['messages'].append({"role": "user", "content": message})
        node['update_time'] = time.time()  # Add a timestamp for when the node was last updated

    def create_new_node(self, feature_vector, message):
        self.nodes.append({'feature_vector': feature_vector, 
                           'messages': [{"role": "user", "content": message}],
                           'update_time': time.time()})  # Add a timestamp for when the node was created
        
    def decay_memory(self):
        # Apply a decay to all node feature vectors based on their last update time
        current_time = time.time()
        for node in self.nodes:
            time_diff = current_time - node['update_time']
            decay_factor = np.exp(-self.decay_rate * time_diff)
            node['feature_vector'] *= decay_factor    

class ChatBot:
    def __init__(self, memory_manager, model_manager, emotion_detector):
        self.memory_manager = memory_manager
        self.model_manager = model_manager
        self.emotion_detector = emotion_detector
        self.moods = {0: "neutral", 1: "happy", 2: "anxious", 3: "curious", 4: "sad"}

    def chat_with_gpt(self, message, user):
        feature_vector = self.model_manager.model.encode([message])[0]
        self.memory_manager.add_to_memory(feature_vector, message)
        mood = self.emotion_detector.get_emotion(message)
        system_message = self.generate_system_message(mood)
        messages = self.generate_messages(message, system_message)
        print("TEST: ", messages)

        # ... truncated for brevity ...
        try:
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            return response.choices[0].message['content']
        except Exception as e:
            logger.error(f"Failed to get response from GPT-3. Error: {str(e)}")
    
    @staticmethod
    def generate_system_message(mood):
        system_message = f"You are a helpful assistant. The user seems {mood}, help user to increase their self efficacy."
        return system_message

    def generate_messages(self, message, system_message):
        feature_vector = self.model_manager.model.encode([message])[0]
        similar_node = self.memory_manager.find_similar_node(feature_vector)

        past_messages_text = ''
        if similar_node is not None:
            past_user_messages = similar_node['messages'][-5:]
            past_messages = [msg["content"] for msg in past_user_messages]
            past_messages_text = ', '.join(past_messages)

        system_message = f"{system_message} They have previously talked about: {past_messages_text}."

        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": message}]

        return messages

class FeedbackManager:
    def __init__(self, emotion_detector):
        self.gpt_responses = []
        self.feedback_scores = []
        self.emotion_detector = emotion_detector

    def generate_responses(self, diary_entries, user, chat_bot, model_manager):
        embeddings, scaled_embeddings = self._get_scaled_embeddings(diary_entries, model_manager)

        for i, entry in enumerate(diary_entries):
            self._generate_response(i, entry, user, chat_bot, model_manager, scaled_embeddings)
            
        self._print_responses_and_feedback(diary_entries)

    def _get_scaled_embeddings(self, diary_entries, model_manager):
        embeddings = [model_manager.model.encode([entry])[0] for entry in diary_entries]
        scaled_embeddings = model_manager.scaler.fit_transform(embeddings)
        return embeddings, scaled_embeddings

    def _generate_response(self, i, entry, user, chat_bot, model_manager, scaled_embeddings):
        response = chat_bot.chat_with_gpt(entry, user)

        logger.info(f"Diary Entry {i+1}: {entry}")
        logger.info(f"GPT-3 Response {i+1}: {response}")

        feedback_score = int(input("Rate the response from 1 (not helpful) to 5 (very helpful):\n"))
        while feedback_score <= 2:
            logger.info("I'm sorry you didn't find my response helpful. Let me try again.")
            response = chat_bot.chat_with_gpt(entry + " The previous response was not helpful.", user)
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
    memory_manager = AdvancedMemoryManager()
    emotion_detector = EmotionDetector()
    chat_bot = ChatBot(memory_manager, model_manager, emotion_detector)
    feedback_manager = FeedbackManager(emotion_detector)

    # ... truncated for brevity ...
    diary_entries = [
        "I used to love gardening but I stopped because I'm afraid of falling.",
        "I watched a gardening show today and felt good.",
        "I wish I could garden again but don't know where to start."
        #"I've always wanted to write a novel, but I feel like I'm not creative enough.",
        #"I wish I could lose weight but I struggle to stick to a diet.",
        #"I'd like to learn to play the guitar, but it seems so difficult.",
        #"I dream of running a marathon but can't imagine having the discipline to train for it.",
        #"I want to learn a new language, but I always find it too hard.",
        #"I'd love to change my career path, but I'm scared of failure and rejection."
    ]
    user = "user1"

    feedback_manager.generate_responses(diary_entries, user, chat_bot, model_manager)
