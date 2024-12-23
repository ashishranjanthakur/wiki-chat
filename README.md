# WikiChat - Intelligent Multi-Personality Chatbot

A Flask-based chatbot that combines Wikipedia knowledge, web search, and multiple personalities to create engaging and informative conversations.

## Features

- **Multiple AI Personalities**:
  - Friendly Guide: Casual and approachable responses
  - Professor: Academic and detailed explanations
  - Personal Assistant: Professional and helpful answers

- **Smart Information Retrieval**:
  - Wikipedia integration for factual queries
  - Web search capabilities for current information
  - Time-based responses and greetings

- **Query Types Supported**:
  - Factual questions (What is, Who was, etc.)
  - Current events and news
  - How-to questions
  - Time queries
  - Greetings

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wiki-chat.git
cd wiki-chat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and go to `http://localhost:5000`

## Usage

1. Select a personality from the available options
2. Type your question in the chat input
3. Examples of questions you can ask:
   - "What is artificial intelligence?"
   - "How does photosynthesis work?"
   - "Latest news in technology"
   - "What time is it?"
   - "How to learn programming?"

## Technologies Used

- **Backend**:
  - Flask (Web Framework)
  - Wikipedia-API (Knowledge Base)
  - BeautifulSoup4 (Web Scraping)
  - Requests (HTTP Client)
  - Pytz (Timezone Handling)

- **Frontend**:
  - HTML/CSS
  - JavaScript
  - Modern responsive design

## Project Structure

- `app.py`: Main application file
- `requirements.txt`: Project dependencies
- `templates/`: HTML templates
- `.env`: Environment variables (not tracked in git)

## Contributing

Feel free to open issues or submit pull requests to improve the project.

## License

MIT License - feel free to use and modify for your own projects!
