from django.urls import path
from .views import UploadCSVView, NextLeadView, UpdateLeadView, SimulateChatAPIView, csv_upload_form, tts_api, stt_api, gradio_iframe

app_name = "leads"

urlpatterns = [
    path('upload-form/', csv_upload_form, name='csv-upload-form'),  # UI form
    path('api/tts/', tts_api, name='tts_api'),
    path('api/stt/', stt_api, name='stt_api'),
    path('chatbot/', gradio_iframe, name='gradio_iframe'),


    path('simulate-chat/', SimulateChatAPIView.as_view(), name='simulate-chat'),
    path("upload/", UploadCSVView.as_view(), name="upload_csv"),
    path("next-lead/", NextLeadView.as_view(), name="next_lead"),
    path("update/<int:lead_id>/", UpdateLeadView.as_view(), name="update_lead"),
]
