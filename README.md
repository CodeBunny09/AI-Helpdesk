# Django Chatbot Backend

This project is a Django-based backend that integrates a chatbot using OpenAI's API, Gradio for UI embedding, and optional Twilio utilities for voice or SMS functionality.

## 📁 Project Structure

```

.
├── backend/                # Django project config (settings, urls, wsgi)
├── leads/                  # App with chatbot logic, APIs, templates
├── manage.py               # Django CLI entry point
├── db.sqlite3              # Default Django SQLite DB
├── leads.db                # Possible separate DB for lead data
├── requirements.txt        # Python dependencies
├── flat.sh                 # Script for flattening project output
├── project\_flattened\_output.txt  # Output from the flattening script

````

## 🚀 Features

- 🤖 OpenAI chatbot integration
- 🎛️ Gradio UI embedding via template
- 🗣️ Text-to-Speech (TTS) and Speech-to-Text (STT) utilities
- ☎️ Twilio integration (SMS/Voice support)
- 📦 REST API using Django REST Framework
- 🧪 Custom management command for simulating chats

## 📦 Installation

### 1. Clone the repository

```bash
git clone git@github.com:CodeBunny09/AI-Helpdesk.git
cd your-repo
````

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

### 6. Access the app

* API endpoints at: `http://127.0.0.1:8000/leads/`
* Gradio embedded UI at: `http://127.0.0.1:8000/leads/gradio/`


## 📁 Notable Files

* `gradio_app.py` – Launches a Gradio interface
* `openai_chatbot.py` – Handles OpenAI API interaction
* `tts_stt_utils.py` – Converts speech to text and vice versa
* `twilio_utils.py` – Manages Twilio-based communication

