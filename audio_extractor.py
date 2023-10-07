# File: audio_extractor.py

import logging
from pydub import AudioSegment

class AudioExtractor:
    def extract(self, video_file, audio_file):
        try:
            video = AudioSegment.from_file(video_file)
            video.export(audio_file, format='mp3')
            logging.info(f"Audio extracted to: {audio_file}")
        except Exception as e:
            logging.error(f"Failed to extract audio: {e}")
            raise
