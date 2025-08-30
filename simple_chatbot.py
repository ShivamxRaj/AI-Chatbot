import json
import random
from datetime import datetime
from typing import Dict, List
import os

class SimpleChatbot:
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.faq = self._load_faq()
        self.user_context = {}
    
    def _load_faq(self) -> Dict:
        """Load FAQ knowledge base from JSON file."""
        try:
            with open('faq_knowledge_base.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("FAQ knowledge base not found. Using default FAQs.")
            return {
                "greetings": {
                    "responses": ["Hello! How can I assist you today?", "Hi there! What can I help you with?"]
                },
                "goodbye": {
                    "responses": ["Goodbye! Have a great day!", "Thank you for chatting with us. Goodbye!"]
                },
                "help": {
                    "responses": ["I can help you with general inquiries, product information, and more. What would you like to know?"]
                }
            }
    
    def analyze_sentiment(self, text: str) -> int:
        """Simple sentiment analysis based on keywords."""
        positive_words = ['good', 'great', 'excellent', 'happy', 'thanks', 'thank you', 'awesome']
        negative_words = ['bad', 'terrible', 'awful', 'angry', 'frustrated', 'unhappy']
        
        text_lower = text.lower()
        positive_count = sum(text_lower.count(word) for word in positive_words)
        negative_count = sum(text_lower.count(word) for word in negative_words)
        
        if positive_count > negative_count:
            return 1  # Positive
        elif negative_count > positive_count:
            return -1  # Negative
        return 0  # Neutral
    
    def get_response(self, user_input: str) -> str:
        """Generate a response to user input."""
        # Add user input to conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Analyze sentiment
        sentiment = self.analyze_sentiment(user_input)
        
        # Check for FAQ matches
        response = self._check_faq(user_input)
        if response:
            return self._format_response(response, sentiment)
        
        # Handle fallback for unclear queries
        if self._is_unclear_query(user_input):
            return self._handle_unclear_query()
        
        # Default response if no FAQ match
        return self._generate_default_response(sentiment)
    
    def _check_faq(self, user_input: str) -> str:
        """Check if user input matches any FAQ questions."""
        user_input = user_input.lower()
        
        # Check for direct matches
        for intent, data in self.faq.items():
            if 'patterns' in data:
                for pattern in data['patterns']:
                    if pattern.lower() in user_input:
                        return random.choice(data['responses'])
        
        # Check for keyword matches
        for intent, data in self.faq.items():
            if 'keywords' in data:
                for keyword in data['keywords']:
                    if keyword in user_input:
                        return random.choice(data['responses'])
        
        return ""
    
    def _is_unclear_query(self, user_input: str) -> bool:
        """Determine if the user's query is unclear or vague."""
        return len(user_input.split()) < 3
    
    def _handle_unclear_query(self) -> str:
        """Generate a response for unclear queries."""
        suggestions = [
            "Could you please provide more details about what you're looking for?",
            "I want to make sure I understand correctly. Could you rephrase your question?",
            "I'd be happy to help! Could you tell me more about what you need?"
        ]
        return random.choice(suggestions)
    
    def _format_response(self, response: str, sentiment: int) -> str:
        """Format the response based on sentiment and context."""
        if sentiment < 0:
            empathy = ["I'm sorry to hear that. ", "I understand this might be frustrating. "]
            response = random.choice(empathy) + response
        return response
    
    def _generate_default_response(self, sentiment: int) -> str:
        """Generate a default response when no specific answer is found."""
        default_responses = [
            "I'm not entirely sure about that. Could you provide more details?",
            "That's an interesting question. Let me find out more information for you.",
            "I'd be happy to help with that. Could you clarify your question?"
        ]
        
        if sentiment < 0:
            default_responses = [
                "I apologize for the confusion. Let me help clarify this for you.",
                "I'm sorry I couldn't find a better answer. Let me look into this further.",
                "I want to make sure I get this right. Could you provide more details?"
            ]
            
        return random.choice(default_responses)

def main():
    print("Simple AI Chatbot: Hello! I'm your AI assistant. Type 'quit' to exit.")
    chatbot = SimpleChatbot()
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'quit':
            print("AI Chatbot: Goodbye! Have a great day!")
            break
            
        response = chatbot.get_response(user_input)
        print(f"AI Chatbot: {response}")

if __name__ == "__main__":
    main()
