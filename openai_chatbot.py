import os
import json
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class OpenAIChatbot:
    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.conversation_history: List[Dict] = []
        self.load_conversation_context()
        
    def load_conversation_context(self):
        """Load any existing conversation context."""
        try:
            with open('conversation_context.json', 'r') as f:
                self.conversation_history = json.load(f)
        except FileNotFoundError:
            # Initialize with a system message
            self.conversation_history = [
                {
                    "role": "system",
                    "content": """You are a helpful AI assistant designed for customer support. 
                    Be friendly, professional, and provide accurate information. 
                    If you don't know something, say so rather than making up an answer."""
                }
            ]
    
    def save_conversation_context(self):
        """Save the conversation context to a file."""
        with open('conversation_context.json', 'w') as f:
            json.dump(self.conversation_history, f)
    
    def get_response(self, user_input: str) -> str:
        """Get a response from OpenAI's API."""
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=150
            )
            
            # Extract the assistant's response
            assistant_response = response.choices[0].message.content
            
            # Add assistant's response to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            # Save the updated conversation context
            self.save_conversation_context()
            
            return assistant_response
            
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}"

def main():
    # Check if API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("""
        Error: OPENAI_API_KEY not found.
        Please create a .env file in this directory with your OpenAI API key:
        OPENAI_API_KEY=your_api_key_here
        """)
        return
    
    print("AI Chatbot: Hello! I'm your AI assistant. Type 'quit' to exit.")
    chatbot = OpenAIChatbot()
    
    try:
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("AI Chatbot: Goodbye! Have a great day!")
                break
                
            response = chatbot.get_response(user_input)
            print(f"AI Chatbot: {response}")
            
    except KeyboardInterrupt:
        print("\nAI Chatbot: Goodbye! Have a great day!")
    finally:
        # Save conversation context before exiting
        chatbot.save_conversation_context()

if __name__ == "__main__":
    main()
