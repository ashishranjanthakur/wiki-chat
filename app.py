from flask import Flask, render_template, request, jsonify
import wikipediaapi
import random
from datetime import datetime
import pytz
import requests
from bs4 import BeautifulSoup
import re
import json

app = Flask(__name__)

# Initialize Wikipedia API
wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='WikiChat/1.0'
)

def get_current_time(timezone='Asia/Kolkata'):
    """Get current time in specified timezone"""
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    return current_time.strftime("%I:%M %p, %d %B %Y")

def get_time_based_greeting():
    """Return time-appropriate greeting"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 22:
        return "Good evening"
    else:
        return "Hello"

# Define chat personalities
PERSONALITIES = {
    'friendly': {
        'name': 'Friendly Guide',
        'style': 'friendly and casual',
        'intros': [
            "Hey! Let me help you with that. ",
            "Great question! Here's what I found: ",
            "I'd be happy to help! "
        ],
        'transitions': [
            "Also, here's something interesting: ",
            "You might also want to know that ",
            "Additionally, "
        ],
        'conclusions': [
            "Hope that helps! 😊",
            "Let me know if you need anything else! 🌟",
            "Feel free to ask more questions! 💡"
        ]
    },
    'professor': {
        'name': 'Professor',
        'style': 'academic and detailed',
        'intros': [
            "Let me analyze this query. ",
            "From an analytical perspective, ",
            "Let's examine this systematically. "
        ],
        'transitions': [
            "Furthermore, ",
            "It's important to note that ",
            "Consider also that "
        ],
        'conclusions': [
            "This is based on current research.",
            "These are the key points to consider.",
            "Let me know if you need clarification."
        ]
    },
    'assistant': {
        'name': 'Personal Assistant',
        'style': 'helpful and professional',
        'intros': [
            f"{get_time_based_greeting()}! ",
            "I'm here to assist you. ",
            "Let me help you with that. "
        ],
        'transitions': [
            "I can also tell you that ",
            "Additionally, ",
            "You might find it useful to know that "
        ],
        'conclusions': [
            "Is there anything else you need help with?",
            "Let me know if you need more assistance!",
            "I'm here if you need more information!"
        ]
    }
}

def search_web(query):
    """Search the web for information"""
    try:
        # Try Wikipedia first
        wiki_response = get_wiki_response(query)
        if wiki_response[0]:
            return wiki_response[0]

        # If Wikipedia fails, try a web search
        search_url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(search_url)
        data = json.loads(response.text)
        
        # Check for instant answer
        if data.get('AbstractText'):
            return data['AbstractText']
        
        # Check for related topics
        if data.get('RelatedTopics'):
            topics = []
            for topic in data['RelatedTopics'][:2]:
                if isinstance(topic, dict) and 'Text' in topic:
                    topics.append(topic['Text'])
            if topics:
                return ' '.join(topics)

        # Fallback to simple web search
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        search_url = f"https://html.duckduckgo.com/html/?q={query}"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get search results
        results = []
        for result in soup.select('.result__body')[:2]:
            text = result.get_text().strip()
            if text:
                results.append(text)
        
        if results:
            return ' '.join(results)

    except Exception as e:
        print(f"Search error: {str(e)}")
        return None
    return None

def is_factual_query(query):
    """Check if the query is likely to be answered well by Wikipedia"""
    factual_patterns = [
        r'what (is|are|was|were)',
        r'who (is|was|are|were)',
        r'when (did|was|were)',
        r'where (is|was|are)',
        r'why (is|was|are|were)',
        r'how (does|did|do)',
        r'definition of',
        r'tell me about',
        r'describe',
        r'explain',
        r'history of'
    ]
    return any(re.search(pattern, query.lower()) for pattern in factual_patterns)

def is_time_query(query):
    """Check if query is about time"""
    time_keywords = ['time', 'current time', 'what time', 'tell me the time']
    return any(keyword in query.lower() for keyword in time_keywords)

def is_greeting(query):
    """Check if query is a greeting"""
    greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
    return any(greeting in query.lower() for greeting in greetings)

def handle_time_query():
    """Handle time-related queries"""
    current_time = get_current_time()
    return f"The current time in India is {current_time}."

def handle_greeting():
    """Handle greeting queries"""
    greeting = get_time_based_greeting()
    current_time = get_current_time()
    return f"{greeting}! It's currently {current_time}."

def get_wiki_response(query):
    """Get response from Wikipedia"""
    try:
        page = wiki.page(query)
        if not page.exists():
            return None, None
        
        summary = page.summary.split('. ')
        main_info = '. '.join(summary[:2]) + '.'
        
        if len(summary) > 2:
            additional_info = '. '.join(summary[2:4]) + '.'
            return main_info, additional_info
        
        return main_info, None
    except Exception:
        return None, None

def clean_response(text):
    """Clean and format the response text"""
    if not text:
        return text
    
    # Remove URLs
    text = re.sub(r'http\S+|www.\S+', '', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Ensure the text ends with proper punctuation
    if text and text[-1] not in '.!?':
        text += '.'
    return text

def format_response(query, personality_key):
    """Format response based on query type and personality"""
    personality = PERSONALITIES[personality_key]
    intro = random.choice(personality['intros'])
    conclusion = random.choice(personality['conclusions'])

    # Handle different types of queries
    if is_time_query(query):
        main_response = handle_time_query()
    elif is_greeting(query):
        main_response = handle_greeting()
    else:
        # Try Wikipedia for factual queries
        if is_factual_query(query):
            wiki_main, wiki_additional = get_wiki_response(query)
            if wiki_main:
                response = wiki_main
                if wiki_additional:
                    transition = random.choice(personality['transitions'])
                    response += f" {transition}{wiki_additional}"
                return f"{intro}{response} {conclusion}"

        # Search the web for any type of query
        web_response = search_web(query)
        if web_response:
            response = clean_response(web_response)
            return f"{intro}{response} {conclusion}"
        else:
            suggestions = [
                "Try rephrasing your question.",
                "You can ask me about facts, current events, or general knowledge.",
                "I'm good at answering questions about history, science, and various topics."
            ]
            return f"{intro}I apologize, but I couldn't find specific information about that. {random.choice(suggestions)} {conclusion}"

    return f"{intro}{main_response} {conclusion}"

@app.route('/')
def home():
    return render_template('index.html', personalities=PERSONALITIES)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('message', '')
    personality = data.get('personality', 'friendly')
    
    if not query:
        return jsonify({'response': 'Please ask me something!'})
    
    try:
        response = format_response(query, personality)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f"Sorry, I encountered an error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
