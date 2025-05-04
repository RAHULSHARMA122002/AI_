# cloud_llm.py
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mixtral-8x7b-instruct"

class CloudLLM:
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.model = MODEL

    async def answer(self, prompt):
        try:
            print(" Querying cloud LLM (OpenRouter)...")
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}]
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                reply = response.json()["choices"][0]["message"]["content"]
                print(" Response:", reply)
                return reply

        except Exception as e:
            print(f" Error in CloudLLM: {e}")
            return "I'm sorry, I couldn't process that right now."
