import asyncio
class EmployeeRouter:
    def __init__(self):
        self.pending_requests = {}  # { request_id: asyncio.Future }
        self.early_answers = {}     # Store answers submitted before the future exists

    def is_available(self):
        return True

    async def route_call(self, question, request_id):
        future = asyncio.get_event_loop().create_future()
        print("furture is created")

        # 🔍 Check if answer already exists
        if request_id in self.early_answers:
            answer = self.early_answers.pop(request_id)
            print(f"🕒 Found early answer for {request_id}: {answer}")
            future.set_result(answer)
        else:
            self.pending_requests[request_id] = future
            print(f"🟡 Awaiting employee response for request: {request_id}")

        try:
            answer = await future
            print(f"✅ Got employee response: {answer}")
            return answer
        finally:
            self.pending_requests.pop(request_id, None)
            print("pending request has been poped")

    def submit_employee_answer(self, request_id, answer):
        print(f"📩 Trying to submit answer for: {request_id}")
        future = self.pending_requests.get(request_id)
        if future is None:
            print(f"❌ No future found for {request_id}")
            self.early_answers[request_id] = answer  # 💾 Save it for later
            
        elif future.done():
            print(f"⚠️ Future already done for {request_id}")
        else:
            future.set_result(answer)
        print(f"✅ Answer set for {request_id}")
        return True
