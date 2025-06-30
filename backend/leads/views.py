import csv
import io
import tempfile
from threading import Thread
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .models import Lead, Conversation, Text
from .serializers import CSVUploadSerializer
from .services.chatbot import get_next_lead, simulate_chat_with_lead
from .openai_utils import transcribe_with_openai, synthesize_with_openai
from .openai_chatbot import get_openai_response
from .gradio_app import launch_gradio_chat


def gradio_iframe(request):
    return render(request, 'gradio_embed.html')


def voice_chat_ui(request):
    return render(request, "voice_test.html")


class SimulateChatAPIView(APIView):
    def post(self, request):
        lead = get_next_lead()
        if lead:
            simulate_chat_with_lead(lead)
            return Response({"message": "Chat simulated successfully."})
        return Response({"message": "No leads available."}, status=404)


class UploadCSVView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        return redirect('leads:csv-upload-form')

    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)
        if serializer.is_valid():
            csv_file = serializer.validated_data['file']
            decoded_file = csv_file.read().decode('utf-8')
            reader = csv.reader(io.StringIO(decoded_file))
            next(reader)
            for row in reader:
                name, phone_number = row
                Lead.objects.create(name=name, phone=phone_number, status='pending')
            return Response({"message": "Leads uploaded successfully."})
        return Response(serializer.errors, status=400)


def csv_upload_form(request):
    return render(request, 'upload.html')


class NextLeadView(APIView):
    def get(self, request):
        lead = Lead.objects.filter(status='pending').first()
        if lead:
            return Response({
                "id": lead.id,
                "name": lead.name,
                "phone": lead.phone,
                "status": lead.status
            })
        return Response({"message": "No leads left."})


class UpdateLeadView(APIView):
    def post(self, request, lead_id):
        status_value = request.data.get("status")
        if not status_value:
            return Response({"error": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lead = Lead.objects.get(id=lead_id)
        except Lead.DoesNotExist:
            raise Http404("Lead not found")

        lead.status = status_value
        lead.save()
        return Response({"message": "Lead updated"})


@csrf_exempt
def tts_api(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        audio_file = generate_tts(text)
        return JsonResponse({'audio_file': audio_file})
    return JsonResponse({'error': 'Only POST allowed'}, status=405)


@csrf_exempt
def stt_api(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio_file')
        if audio_file:
            transcript = transcribe_stt(audio_file)
            return JsonResponse({'transcript': transcript})
        return JsonResponse({'error': 'No audio file uploaded'}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)


@csrf_exempt
def voice_conversation_api(request):
    """
    Accepts a recorded voice message, transcribes it with OpenAI STT,
    responds using OpenAI TTS, and returns the audio.
    """
    if request.method == 'POST':
        audio_file = request.FILES.get("audio")
        lead_id = request.POST.get("lead_id")
        tts_model = request.POST.get("model", "tts-1-hd")
        tts_voice = request.POST.get("voice", "nova")

        if not audio_file or not lead_id:
            return JsonResponse({"error": "Missing audio or lead_id"}, status=400)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name

        user_text = transcribe_with_openai(tmp_path)

        try:
            lead = Lead.objects.get(id=lead_id)
        except Lead.DoesNotExist:
            return JsonResponse({"error": "Lead not found"}, status=404)

        bot_text = get_openai_response(user_text)

        # Create conversation and message turns
        conversation = Conversation.objects.create(
            lead=lead,
            is_inbound=True,
            conversation_type="call"
        )
        Text.objects.create(conversation=conversation, sender="user", content=user_text)
        Text.objects.create(conversation=conversation, sender="bot", content=bot_text)

        # Synthesize audio
        tts_path = f"/tmp/tts_{lead.id}.wav"
        synthesize_with_openai(bot_text, tts_path, model=tts_model, voice=tts_voice)

        # Return audio file inline for streaming
        with open(tts_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="audio/wav")
            response["Content-Disposition"] = "inline"
            response["Accept-Ranges"] = "bytes"
            return response

    return JsonResponse({"error": "Only POST allowed"}, status=405)