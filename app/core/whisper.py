import os
import openai
import tempfile

def speech_to_text(audio_file):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio_file:
        temp_audio_file.write(audio_file.read())

    with open(temp_audio_file.name, "rb") as file_to_transcribe:
        transcript = openai.Audio.transcribe("whisper-1", file_to_transcribe)

    os.remove(temp_audio_file.name)

    text = transcript.get("text")
    return text
