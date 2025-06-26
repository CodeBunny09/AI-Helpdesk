"""
Leads Django app.

⚠️  NOTE
-----
Running Gradio inside Django’s process causes queue/stop_event crashes
with Gradio v4.44+.  The recommended approach is to run Gradio as a
stand-alone service (uvicorn) or simply:

    $ cd backend
    $ python -m leads.gradio_app   # → http://127.0.0.1:7860

Django itself (admin, APIs) stays on http://127.0.0.1:8000.
"""
from django.apps import AppConfig


class LeadsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "leads"

    # No `ready()` override – we no longer start Gradio here.
