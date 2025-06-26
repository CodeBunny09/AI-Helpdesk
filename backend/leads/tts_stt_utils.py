def generate_tts(text):
    """
    Dummy Text-to-Speech generation.
    
    Args:
        text (str): Text input for TTS
    
    Returns:
        str: Path or name of dummy audio file
    """
    print(f"TTS requested for text: {text}")
    return "dummy_tts_output.mp3"


def transcribe_stt(audio_file):
    """
    Dummy Speech-to-Text transcription.
    
    Args:
        audio_file (UploadedFile): Uploaded audio file
    
    Returns:
        str: Dummy transcript
    """
    print(f"STT requested for audio file: {audio_file.name}")
    return "This is a dummy transcription of your audio."
