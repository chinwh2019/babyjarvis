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

class AdvancedMemoryManager:
    def __init__(self, learning_rate=0.5, similarity_threshold=0.8):
        self.nodes = []
        self.learning_rate = learning_rate
        self.similarity_threshold = similarity_threshold

    def add_to_memory(self, feature_vector, message):
        similar_node = self.find_similar_node(feature_vector)
        if similar_node:
            self.update_node(similar_node, feature_vector, message)
        else:
            self.create_new_node(feature_vector, message)

    def find_similar_node(self, feature_vector):
        most_similar_node = None
        highest_similarity = -1

        for node in self.nodes:  # Change this line
            similarity = self.calculate_similarity(feature_vector, node['feature_vector'])
            if similarity > highest_similarity:
                highest_similarity = similarity
                most_similar_node = node

        return most_similar_node

    def calculate_similarity(self, node_feature_vector, feature_vector):
        return np.dot(node_feature_vector, feature_vector) / (np.linalg.norm(node_feature_vector) * np.linalg.norm(feature_vector))

    # def update_node(self, node, feature_vector, message):
    #     node['feature_vector'] = (1 - self.learning_rate) * node['feature_vector'] + self.learning_rate * feature_vector
    #     if len(node['messages']) >= 5:
    #         node['messages'].pop(0)
    #     node['messages'].append(message)

    # def create_new_node(self, feature_vector, message):
    #     self.nodes.append({'feature_vector': feature_vector, 'messages': [message]})

    # Inside the update_node function
    def update_node(self, node, feature_vector, message):
        node['feature_vector'] = (1 - self.learning_rate) * node['feature_vector'] + self.learning_rate * feature_vector
        if len(node['messages']) >= 5:
            node['messages'].pop(0)
        node['messages'].append({"role": "assistant", "content": message})  # Append a dictionary, not just a string

    # And when creating a new node
    def create_new_node(self, feature_vector, message):
        self.nodes.append({'feature_vector': feature_vector, 'messages': [{"role": "assistant", "content": message}]})  # Append a dictionary, not just a string


# class AdvancedMemoryManager:
#     def __init__(self, learning_rate=0.5, similarity_threshold=0.8):
#         self.nodes = []
#         self.learning_rate = learning_rate
#         self.similarity_threshold = similarity_threshold

#     def add_to_memory(self, feature_vector, message):
#         similar_node = self.find_similar_node(feature_vector)
#         if similar_node:
#             self.update_node(similar_node, feature_vector, message)
#         else:
#             self.create_new_node(feature_vector, message)

#     # def find_similar_node(self, feature_vector):
#     #     for node in self.nodes:
#     #         similarity = self.calculate_similarity(node['feature_vector'], feature_vector)
#     #         if similarity >= self.similarity_threshold:
#     #             return node
#     #     return None

#     def find_similar_node(self, feature_vector):
#         most_similar_node = None
#         highest_similarity = -1

#         for node in self.memory.values():
#             similarity = self.calculate_similarity(feature_vector, node['feature_vector'])
#             if similarity > highest_similarity:
#                 highest_similarity = similarity
#                 most_similar_node = node

#         return most_similar_node


#     def calculate_similarity(self, node_feature_vector, feature_vector):
#         return np.dot(node_feature_vector, feature_vector) / (np.linalg.norm(node_feature_vector) * np.linalg.norm(feature_vector))

#     def update_node(self, node, feature_vector, message):
#         node['feature_vector'] = (1 - self.learning_rate) * node['feature_vector'] + self.learning_rate * feature_vector
#         if len(node['messages']) >= 5:
#             node['messages'].pop(0)
#         node['messages'].append(message)

#     def create_new_node(self, feature_vector, message):
#         self.nodes.append({'feature_vector': feature_vector, 'messages': [message]})

class ChatBot:
    def __init__(self, memory_manager, model_manager):
        self.memory_manager = memory_manager
        self.model_manager = model_manager
        self.moods = {0: "neutral", 1: "happy", 2: "anxious", 3: "curious", 4: "sad"}

    def chat_with_gpt(self, message, mood, user):
        feature_vector = self.model_manager.model.encode([message])[0]
        self.memory_manager.add_to_memory(feature_vector, message)
        system_message = self.generate_system_message(mood)
        messages = self.generate_messages(message, system_message)
        print("TEST TEST TEST: ", messages)
        try:
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            return response.choices[0].message['content']
        except Exception as e:
            logger.error(f"Failed to get response from GPT-3. Error: {str(e)}")

    @staticmethod
    def generate_system_message(mood):
        system_message = f"You are a helpful assistant. The user seems {mood}."
        return system_message

    # def generate_messages(self, message, system_message):
    #     messages = [{"role": "system", "content": system_message}, {"role": "user", "content": message}]
    #     # Adding last 5 messages related to the current topic
    #     messages.extend([{"role": "user", "content": msg} for msg in self.memory_manager.nodes[-1]['messages']])
    #     return messages
    
    # def generate_messages(self, message, system_message):
    #     # Get the feature vector for the current message
    #     feature_vector = self.model_manager.model.encode([message])[0]

    #     # Find the most similar node
    #     similar_node = self.memory_manager.find_similar_node(feature_vector)

    #     messages = [{"role": "system", "content": system_message}, {"role": "user", "content": message}]
        
    #     # If a similar node was found, add its messages to the list
    #     if similar_node is not None:
    #         messages.extend([{"role": "user", "content": msg} for msg in similar_node['messages']])
    #     else:
    #         print("No similar node found.")

    #     return messages

    # def generate_messages(self, message, system_message):
    #     # Get the feature vector for the current message
    #     feature_vector = self.model_manager.model.encode([message])[0]

    #     # Find the most similar node
    #     similar_node = self.memory_manager.find_similar_node(feature_vector)

    #     messages = [{"role": "system", "content": system_message}, {"role": "user", "content": message}]

    #     # If a similar node was found, add its messages to the list
    #     if similar_node is not None:
    #         messages.extend(similar_node['messages'][-5:])  # Fetch the last 5 messages from the similar node

    #     return messages
    
    # def generate_messages(self, message, system_message):
    #     # Get the feature vector for the current message
    #     feature_vector = self.model_manager.model.encode([message])[0]

    #     # Find the most similar node
    #     similar_node = self.memory_manager.find_similar_node(feature_vector)
    #     #print(f"TEST TEST TEST: {similar_node['messages']}")

    #     messages = [{"role": "system", "content": system_message}, {"role": "user", "content": message}]

    #     # If a similar node was found, add its messages to the list
    #     if similar_node is not None:
    #         messages.extend([{"role": "assistant", "content": msg} for msg in similar_node['messages'][-5:]])  # Fetch the last 5 messages from the similar node
    #         # for msg in similar_node['messages'][-2:]:
    #         #     print(f"TEST TEST TEST: {msg}")
    #     return messages
    
    def generate_messages(self, message, system_message):
        # Get the feature vector for the current message
        feature_vector = self.model_manager.model.encode([message])[0]

        # Find the most similar node
        similar_node = self.memory_manager.find_similar_node(feature_vector)

        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": message}]

        # If a similar node was found, add its messages to the list
        if similar_node is not None:
            # Fetch the last 5 user messages from the similar node
            past_user_messages = [msg for msg in similar_node['messages'][-5:] if msg['role'] == 'user']
            print(f"TEST TEST TEST: {past_user_messages}")
            messages.extend(past_user_messages)

        return messages





class FeedbackManager:
    def __init__(self):
        self.gpt_responses = []
        self.feedback_scores = []

    def generate_responses(self, diary_entries, user, chat_bot, model_manager):
        embeddings, scaled_embeddings = self._get_scaled_embeddings(diary_entries, model_manager)
        model_manager.knn.fit(scaled_embeddings, [i % len(chat_bot.moods) for i in range(len(scaled_embeddings))])

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
    memory_manager = AdvancedMemoryManager()
    chat_bot = ChatBot(memory_manager, model_manager)
    feedback_manager = FeedbackManager()

    diary_entries = [
        "I used to love gardening but I stopped because I'm afraid of falling.", 
        "I watched a gardening show today and felt good.", 
        "I wish I could garden again but don't know where to start."
    ]
    user = "user1"

    feedback_manager.generate_responses(diary_entries, user, chat_bot, model_manager)
