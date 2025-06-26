import csv
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.utils import timezone
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Lead, ChatHistory
from .serializers import CSVUploadSerializer
from .tts_stt_utils import generate_tts, transcribe_stt
from .services.chatbot import get_next_lead, simulate_chat_with_lead
from threading import Thread
from .gradio_app import launch_gradio_chat


def gradio_iframe(request):
    return render(request, 'gradio_embed.html')




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
                Lead.objects.create(name=name, phone_number=phone_number, status='pending')
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
                "phone_number": lead.phone_number,
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
