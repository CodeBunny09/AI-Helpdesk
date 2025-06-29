from django.urls import path
from .views import UploadCSVView, NextLeadView, UpdateLeadView, SimulateChatAPIView, csv_upload_form, tts_api, stt_api, gradio_iframe, voice_conversation_api, voice_chat_ui
from .views_outreach import StartOutreachView

app_name = "leads"

urlpatterns = [
    path('upload-form/', csv_upload_form, name='csv-upload-form'),  # UI form
    path('api/tts/', tts_api, name='tts_api'),
    path('api/stt/', stt_api, name='stt_api'),
    path('chatbot/', gradio_iframe, name='gradio_iframe'),
    path("voice-chat/", voice_conversation_api, name="voice_chat_api"),
    path("voice-chat-ui/", voice_chat_ui, name="voice_chat_ui"),
    



    path('simulate-chat/', SimulateChatAPIView.as_view(), name='simulate-chat'),
    path("upload/", UploadCSVView.as_view(), name="upload_csv"),
    path("next-lead/", NextLeadView.as_view(), name="next_lead"),
    path("update/<int:lead_id>/", UpdateLeadView.as_view(), name="update_lead"),
    path("start-outreach/", StartOutreachView.as_view(), name="start_outreach"),

]
