# File: subtitle_generator.py

import logging

class SubtitleGenerator:
    def generate(self, response, transcript_file):
        try:
            with open(transcript_file, 'w') as f:
                f.write(response)

            logging.info(f"Transcript saved to: {transcript_file}")
        except Exception as e:
            logging.error(f"Failed to generate transcript: {e}")
            raise
