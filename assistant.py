import os
import asyncio
from dotenv import load_dotenv
from datetime import datetime
from HelpRequest import create_help_request, update_help_request
from firebase import find_answer, update_knowledge_base
from employee_router import EmployeeRouter

load_dotenv()

class Assistant:
    def __init__(self, stt, tts, cloud_llm=None, employee_router=None):
        self.stt = stt
        self.tts = tts
        self.cloud_llm = cloud_llm
        self.employee_router = employee_router or EmployeeRouter()

    async def handle_conversation(self, audio_stream):
        try:
            print(" Listening to user...")

            # Step 1: Transcribe voice to text
            user_query = await self.stt.transcribe(audio_stream)
            print(f"User said: {user_query}")

            if not user_query:
                self.tts.say("Sorry, I didn't catch that.")
                return

            # Step 2: Try to answer from local knowledge base
            local_answer = find_answer(user_query)
            if local_answer:
                print(" Answer found locally.")
                self.tts.say(local_answer)
                return

            print(" No local answer found. Escalating...")

            # Step 3: Log help request as pending
            query_id = create_help_request(user_query)

            # Step 4: Try to escalate to human employee
            if self.employee_router and self.employee_router.is_available():
                print(" Routing to employee... Waiting up to 120 seconds.")

                try:
                    employee_answer = await asyncio.wait_for(
                        self.employee_router.route_call(user_query, query_id),
                        timeout=120
                    )
                    if employee_answer:
                        print(" Employee responded.")
                        self.tts.say(employee_answer)
                        update_knowledge_base(user_query, employee_answer)
                        update_help_request(query_id, employee_answer)
                        return
                except asyncio.TimeoutError:
                    # Check if employee responded just after timeout
                    future = self.employee_router.pending_requests.get(query_id)
                    if future and future.done():
                        employee_answer = future.result()
                        print(" Employee responded late.")
                        self.tts.say(employee_answer)
                        update_knowledge_base(user_query, employee_answer)
                        update_help_request(query_id, employee_answer)
                        return
                    print(" Employee did not respond in time.")

            # Step 5: Fallback to cloud LLM if employee unavailable
            if self.cloud_llm:
                print(" Using cloud LLM to answer...")
                cloud_response = await self.cloud_llm.answer(user_query)
                self.tts.say(cloud_response)
                update_knowledge_base(user_query, cloud_response)
                update_help_request(query_id, cloud_response)
            else:
                self.tts.say("Sorry, I couldn't find an answer right now.")

        except Exception as e:
            print(f" Error during conversation handling: {e}")
            self.tts.say("An unexpected error occurred.")
