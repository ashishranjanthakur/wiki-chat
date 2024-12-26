# Wiki Chat Application

A Flask-based web application that allows users to chat with Wikipedia content using a natural language interface.

## Features
- Interactive chat interface
- Wikipedia content search and retrieval
- Natural language processing for better understanding
- Real-time responses

## Tech Stack
- Python 3.9
- Flask 3.0.0
- Wikipedia-API
- BeautifulSoup4
- Gunicorn (for production deployment)

## Local Development
1. Clone the repository:
```bash
git clone https://github.com/ashishranjanthakur/wiki-chat.git
cd wiki-chat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
python app.py
```

## Production Deployment
This application is configured for deployment on Render.com. The necessary configuration files (`render.yaml`, `Procfile`, and `gunicorn_config.py`) are included in the repository.

## License
MIT License
