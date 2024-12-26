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
This application is configured for deployment on PythonAnywhere. Follow these steps to deploy:

1. Create a free account on [PythonAnywhere](https://www.pythonanywhere.com)
2. Go to the "Web" tab and create a new web app
3. Choose "Flask" as your framework
4. Set the Python version to 3.9
5. In the "Code" section:
   ```bash
   git clone https://github.com/ashishranjanthakur/wiki-chat.git
   ```
6. Set your WSGI configuration file to point to the wsgi.py file
7. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
8. Reload your web app

Your application will be available at `yourusername.pythonanywhere.com`

## License
MIT License
