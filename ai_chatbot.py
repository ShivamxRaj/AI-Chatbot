import json
from datetime import datetime
from typing import Dict, List, Optional
import random
from textblob import TextBlob
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AIChatbot:
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.faq = self._load_faq()
        self.user_context = {}
        
    def _load_faq(self) -> Dict:
        """Load FAQ knowledge base from JSON file."""
        try:
            with open('faq_knowledge_base.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning("FAQ knowledge base not found. Using default FAQs.")
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
    
    def analyze_sentiment(self, text: str) -> float:
        """Analyze the sentiment of the input text."""
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
    
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
    
    def _check_faq(self, user_input: str) -> Optional[str]:
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
        
        return None
    
    def _is_unclear_query(self, user_input: str) -> bool:
        """Determine if the user's query is unclear or vague."""
        # Simple check for very short or generic queries
        if len(user_input.split()) < 3:
            return True
            
        # Check for common vague phrases
        vague_phrases = ["help", "what is", "how to", "can you", "i need"]
        return any(phrase in user_input.lower() for phrase in vague_phrases)
    
    def _handle_unclear_query(self) -> str:
        """Generate a response for unclear queries."""
        suggestions = [
            "Could you please provide more details about what you're looking for?",
            "I want to make sure I understand correctly. Could you rephrase your question?",
            "I'd be happy to help! Could you tell me more about what you need?"
        ]
        return random.choice(suggestions)
    
    def _format_response(self, response: str, sentiment: float) -> str:
        """Format the response based on sentiment and context."""
        # Add empathetic response for negative sentiment
        if sentiment < -0.3:
            empathy = ["I'm sorry to hear that. ", "I understand this might be frustrating. ", "I apologize for the inconvenience. "]
            response = random.choice(empathy) + response
        
        return response
    
    def _generate_default_response(self, sentiment: float) -> str:
        """Generate a default response when no specific answer is found."""
        default_responses = [
            "I'm not entirely sure about that. Could you provide more details?",
            "That's an interesting question. Let me find out more information for you.",
            "I'd be happy to help with that. Could you clarify your question?"
        ]
        
        # Slightly more apologetic response for negative sentiment
        if sentiment < -0.3:
            default_responses = [
                "I apologize for the confusion. Let me help clarify this for you.",
                "I'm sorry I couldn't find a better answer. Let me look into this further.",
                "I want to make sure I get this right. Could you provide more details?"
            ]
            
        return random.choice(default_responses)
    
    def collect_feedback(self, feedback: str, rating: int):
        """Collect and store user feedback."""
        feedback_data = {
            'timestamp': datetime.now().isoformat(),
            'feedback': feedback,
            'rating': rating,
            'conversation': self.conversation_history[-5:]  # Store last 5 interactions
        }
        
        try:
            with open('feedback.json', 'a') as f:
                f.write(json.dumps(feedback_data) + '\n')
            return "Thank you for your valuable feedback!"
        except Exception as e:
            logging.error(f"Error saving feedback: {e}")
            return "We encountered an error saving your feedback. Thank you anyway!"


def main():
    print("AI Chatbot: Hello! I'm your AI assistant. Type 'quit' to exit.")
    chatbot = AIChatbot()
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'quit':
            print("AI Chatbot: Goodbye! Have a great day!")
            break
            
        response = chatbot.get_response(user_input)
        print(f"AI Chatbot: {response}")
        
        # Randomly ask for feedback occasionally
        if random.random() < 0.1:  # 10% chance to ask for feedback
            print("\nAI Chatbot: Was this response helpful? (yes/no)")
            feedback = input("You: ")
            if feedback.lower() in ['yes', 'no']:
                print("AI Chatbot: Thank you for your feedback!")


if __name__ == "__main__":
    main()
