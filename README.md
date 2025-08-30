# AI Chatbot for Customer Support

This repository contains two versions of a Python-based chatbot:
1. **OpenAI-powered Chatbot** - Uses OpenAI's API for advanced responses (requires API key)
2. **Rule-based Chatbot** - Local, offline chatbot with predefined responses (no API key needed)

## 🚀 Features

### 🤖 OpenAI Chatbot
- Powered by OpenAI's GPT models
- Context-aware conversations
- Natural language understanding
- Requires internet connection and API key

### ⚡ Rule-based Chatbot
- Works offline, no API key needed
- Lightning fast responses
- Easy to customize responses
- Comprehensive FAQ knowledge base
- No external dependencies
- Handles 20+ common question categories

## 🚀 Quick Start

### Option 1: Rule-based Chatbot (Recommended)
```bash
# No setup needed, just run:
python simple_rule_bot.py
```

### Option 2: OpenAI Chatbot
```bash
# 1. Get API key from https://platform.openai.com/api-keys
# 2. Create .env file with your API key
# 3. Install requirements
pip install -r requirements.txt
# 4. Run the chatbot
python openai_chatbot.py
```

## 📚 Comprehensive FAQ Categories

The rule-based chatbot comes pre-loaded with responses for these common question types:

### 🔍 Common Inquiries
- Greetings & Basic Info
- Account Management
- Order Status & Tracking
- Payment Methods
- Returns & Refunds
- Shipping & Delivery
- Product Information
- Pricing & Discounts
- Technical Support
- Business Hours
- Contact Information
- Company Information
- Store Locations

## 🛠 Customization

### Editing Responses
Edit `faq_knowledge_base.json` to customize any response. The structure is intuitive:

```json
{
  "intent_name": {
    "patterns": ["list", "of", "example", "phrases"],
    "keywords": ["important", "keywords"],
    "responses": ["Possible", "Responses", "For this intent"]
  }
}
```

### Adding New Intents
1. Add a new entry in `faq_knowledge_base.json`
2. Define patterns and responses
3. The chatbot will automatically include it

## 📂 Files

| File | Description |
|------|-------------|
| `simple_rule_bot.py` | Main rule-based chatbot script |
| `openai_chatbot.py` | OpenAI-powered chatbot (requires API key) |
| `faq_knowledge_base.json` | All chatbot responses and patterns |
| `.env` | Store your OpenAI API key |
| `requirements.txt` | Python dependencies |

## 💡 Example Questions

Try asking:
- "What's your return policy?"
- "How can I track my order?"
- "What payment methods do you accept?"
- "Do you have any current promotions?"
- "What are your business hours?"
- "How do I create an account?"

## 🔧 Troubleshooting

### Common Issues
- **JSON Syntax Errors**: Validate your `faq_knowledge_base.json` using a JSON validator
- **Pattern Matching**: Ensure patterns in JSON match user input (case insensitive)
- **API Issues**: For OpenAI version, check your API key and internet connection

## 📝 License

MIT License - Feel free to use and modify for your needs!
