from deepgram import Deepgram
import os
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if not DEEPGRAM_API_KEY:
    raise ValueError("Deepgram API Key is missing. Set it in .env")
from deepgram import Deepgram
import os
from dotenv import load_dotenv
import io

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if not DEEPGRAM_API_KEY:
    raise ValueError("Deepgram API Key is missing. Set it in your .env file")

class DeepgramSTT:
    def __init__(self):
        self.client = Deepgram(DEEPGRAM_API_KEY)

    async def transcribe(self, audio_stream: io.BytesIO):
        """Transcribe audio (wav format) using Deepgram SDK v2."""
        try:

            source = {
                'buffer': audio_stream,
                'mimetype': 'audio/wav'
            }

            response = await self.client.transcription.prerecorded(source, {
                'punctuate': True,
                'language': 'en'
            })

            if response and 'results' in response and 'channels' in response['results']:
                transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
                print(transcript)
                return transcript
               
            else:
                print(" No No transcript found in response.")
                return None
                print(transcript)

        except Exception as e:
            print(f" Error during transcription: {e}")
            return None
