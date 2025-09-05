import json
from sentence_transformers import SentenceTransformer, util
import torch

class Chatbot:
    def __init__(self, intents_file):
        # The new model is better for question-answering tasks
        self.model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
        
        with open(intents_file, 'r') as f:
            self.intents = json.load(f)
            
        self.patterns = []
        self.pattern_to_tag = {}
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                self.patterns.append(pattern)
                self.pattern_to_tag[pattern] = intent['tag']
        
        self.pattern_embeddings = self.model.encode(self.patterns, convert_to_tensor=True)

    def get_response(self, user_message):
        # Encode the user's message into a vector
        message_embedding = self.model.encode(user_message, convert_to_tensor=True)
        
        # Compute cosine similarity
        similarities = util.pytorch_cos_sim(message_embedding, self.pattern_embeddings)[0]
        
        # Find the index and score of the most similar pattern
        best_match_idx = torch.argmax(similarities).item()
        score = similarities[best_match_idx]
        
        # Get the pattern that was the best match
        matched_pattern = self.patterns[best_match_idx]

        # This is the debug print statement to show the score in your terminal
        print(f"User Message: '{user_message}'")
        print(f"Best Match: '{matched_pattern}' with score: {score:.4f}")

        # Check if the confidence score is high enough for a match
        if score > 0.6:
            tag = self.pattern_to_tag[matched_pattern]
            for intent in self.intents['intents']:
                if intent['tag'] == tag:
                    import random
                    return random.choice(intent['responses'])
        else:
            # If the score is too low, return the fallback response
            return "I'm sorry, I don't have an answer for that. I can help with topics like: Greetings, Shipping, Returns, and Payments."