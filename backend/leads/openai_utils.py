import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_with_openai(audio_file_path: str) -> str:
    with open(audio_file_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript.text


def synthesize_with_openai(text: str, output_path: str, model="tts-1-hd", voice="nova") -> str:
    """
    Uses OpenAI TTS (HD) to generate speech from text and save to output_path.
    """
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )
    response.stream_to_file(output_path)
    return output_path
