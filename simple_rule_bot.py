import json
import random
from datetime import datetime
from typing import Dict, List

class RuleBasedChatbot:
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
                    "patterns": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"],
                    "responses": ["Hello! How can I assist you today?", "Hi there! What can I help you with?"]
                },
                "goodbye": {
                    "patterns": ["bye", "goodbye", "see you", "farewell"],
                    "responses": ["Goodbye! Have a great day!", "Thank you for chatting with us. Goodbye!"]
                },
                "help": {
                    "patterns": ["help", "support", "assistance"],
                    "responses": ["I can help you with general inquiries, product information, and more."]
                },
                "thanks": {
                    "patterns": ["thank", "thanks", "appreciate"],
                    "responses": ["You're welcome!", "Happy to help!"]
                },
                "about": {
                    "patterns": ["who are you", "what are you", "your name"],
                    "responses": ["I'm a rule-based chatbot designed to help answer your questions."]
                },
                "default": {
                    "responses": [
                        "I'm not sure I understand. Could you rephrase that?",
                        "I don't have enough information to answer that. Could you provide more details?",
                        "I'm still learning. Could you ask me something else?"
                    ]
                }
            }
    
    def get_response(self, user_input: str) -> str:
        """Generate a response to user input."""
        # Add user input to conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Convert input to lowercase for matching
        user_input_lower = user_input.lower()
        
        # Check for matches in FAQ
        for intent, data in self.faq.items():
            if intent == 'default':
                continue
                
            # Check patterns
            if 'patterns' in data:
                for pattern in data['patterns']:
                    if pattern.lower() in user_input_lower:
                        response = random.choice(data['responses'])
                        self._add_to_history('assistant', response)
                        return response
            
            # Check keywords
            if 'keywords' in data:
                for keyword in data['keywords']:
                    if keyword in user_input_lower:
                        response = random.choice(data['responses'])
                        self._add_to_history('assistant', response)
                        return response
        
        # Default response if no match found
        response = random.choice(self.faq.get('default', {}).get('responses', ["I'm not sure how to respond to that."]))
        self._add_to_history('assistant', response)
        return response
    
    def _add_to_history(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })

def main():
    print("Simple Rule-Based Chatbot: Hello! I'm here to help. Type 'quit' to exit.")
    chatbot = RuleBasedChatbot()
    
    try:
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Chatbot: Goodbye! Have a great day!")
                break
                
            response = chatbot.get_response(user_input)
            print(f"Chatbot: {response}")
            
    except KeyboardInterrupt:
        print("\nChatbot: Goodbye! Have a great day!")

if __name__ == "__main__":
    main()
