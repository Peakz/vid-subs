# File: transcriber.py

import logging
import openai

class Transcriber:
    def __init__(self, api_key):
        openai.api_key = api_key

    def transcribe(self, audio_file, terms):
        prompt = f"VALORANT gameplay audio. `{terms}`"
        
        try:
            with open(audio_file, 'rb') as audio:
                response = openai.Audio.transcribe("whisper-1", audio, prompt=prompt, response_format="srt", language="en")
            logging.info("Audio transcribed successfully.")
            return response
        except Exception as e:
            logging.error(f"Failed to transcribe audio: {e}")
            raise
