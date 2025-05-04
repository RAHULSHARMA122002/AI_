import os
import asyncio
import threading
from dotenv import load_dotenv
from livekit_handler import LiveKitHandler  # Ensure LiveKitHandler is correctly implemented
from flask_app import app  # Import the Flask app from flask_app.py
from employee_router import EmployeeRouter

# Assign router instance
app.router = EmployeeRouter()

# Load environment variables from .env file
load_dotenv()

# Run the Flask dashboard in a background thread
def run_dashboard():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

# Run the assistant system
async def start_assistant():
    livekit_handler = LiveKitHandler()
    await livekit_handler.connect_to_room('phone_room')
    await livekit_handler.listen_for_audio()

# Entry point
if __name__ == "__main__":
    try:
        # Start Flask dashboard thread
        threading.Thread(target=run_dashboard, daemon=True).start()

        # Start assistant (LiveKit + STT + logic)
        asyncio.run(start_assistant())

    except Exception as e:
        print(f"Error during execution: {e}")
