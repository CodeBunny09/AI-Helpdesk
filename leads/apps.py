from django.apps import AppConfig
from threading import Thread
import os

class LeadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leads'

    def ready(self):
        # Prevent double run on Django autoreload
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from .gradio_app import launch_gradio_chat

        def run_gradio():
            demo = launch_gradio_chat()
            demo.launch(
                server_name="0.0.0.0",
                server_port=7860,
                share=False,
                inline=False,
                max_threads=5
            )

        Thread(target=run_gradio, daemon=True).start()

