from dotenv import load_dotenv
import os
import asyncio
import io
import numpy as np
import wave
import sounddevice as sd
from scipy.io.wavfile import write
from cloud_llm import CloudLLM
from employee_router import EmployeeRouter


load_dotenv()

class MockLiveKitRoom:
    async def get_audio_stream(self, duration=5, sample_rate=16000):
        """Record real audio from the microphone and return it as a stream."""
        print(f"🎙️ Recording {duration} seconds of real audio...")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished

        # Save to a BytesIO buffer
        audio_bytes = io.BytesIO()
        write(audio_bytes, sample_rate, audio)
        audio_bytes.seek(0)
        print("✅ Audio recorded and ready.")
        return audio_bytes

class MockLiveKitClient:
    async def connect(self, room_name):
        print(f"✅ [Mock] Connected to room: {room_name}")
        return MockLiveKitRoom()

# Imports for STT, TTS, and Assistant
from stt import DeepgramSTT
from tts import SimpleTTS

Assistant = None

def import_assistant():
    global Assistant
    if Assistant is None:
        from assistant import Assistant  # Dynamically import

class LiveKitHandler:
    def __init__(self):
        self.room = None
        self.client = MockLiveKitClient()
        self.stt = DeepgramSTT()
        self.tts = SimpleTTS()
        import_assistant()
        self.assistant = Assistant(self.stt, self.tts,cloud_llm=CloudLLM(),employee_router=EmployeeRouter())

    async def connect_to_room(self, room_name):
        self.room = await self.client.connect(room_name)
        print(f"Connected to room: {room_name}")

    async def handle_audio_stream(self, audio_stream):
        """Transcribe and handle conversation."""
        await self.assistant.handle_conversation(audio_stream)

    async def listen_for_audio(self):
        while True:
            audio_stream = await self.room.get_audio_stream()
            await self.handle_audio_stream(audio_stream)
