# Django Chatbot Backend

This project is a Django-based backend that integrates a chatbot using OpenAI's API, Gradio for UI embedding, and optional Twilio utilities for voice or SMS functionality.

## 📁 Project Structure

```
.
├── backend/                  # Django backend project
│   ├── backend/             # Django project settings and core files
│   │   ├── settings.py      # Main project configuration
│   │   ├── urls.py          # Root URL declarations
│   │   └── wsgi.py          # WSGI entry point for deployment
│   ├── leads/               # Django app for managing leads and AI chat
│   │   ├── admin.py         # Django admin config for leads
│   │   ├── models.py        # Database models
│   │   ├── serializers.py   # DRF serializers for API
│   │   ├── views.py         # API views and logic
│   │   ├── urls.py          # App-specific routes
│   │   ├── gradio_app.py    # Gradio UI integration
│   │   ├── openai_chatbot.py# OpenAI logic integration
│   │   └── templates/       # HTML templates for embedding Gradio/UI
│   ├── manage.py            # Django management CLI
│   └── requirements.txt     # Backend dependencies
│
├── frontend/                # React frontend (Add React/Vite app here, yet to be added)
│
├── .gitignore               # Specifies untracked files
├── README.md                # Project overview and instructions

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

