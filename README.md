# AI_
User —(voice)→ AI Assistant (local LLM) —→
├─[Confident?] → Answer with TTS
├─[Uncertain?] → Trigger Help Request
├─ Employee Available? → Connect employee (LiveKit)
│ └→ Employee responds → Update Local KB
└─ No Employee → Use Cloud LLM → Update Local KB

The system uses two models: one is the local model and the other is the Cloud LLM. The local model is trained with data stored in the knowledge_json file.

The Cloud LLM is powered by Open Router.

Mock LiveKit: Currently, you’re using a mock version of LiveKit for simulating employee interactions, but the functionality can be replaced with actual LiveKit when ready.

Cloud LLM (which can be fine-tuned and retrained with the desired data): This will eventually reduce the need for a human in the loop, providing a more efficient and robust assistant. I haven’t done the fine-tuning yet due to limited resources like GPUs.

To Run 
Run just run main.py
and dashboard will be on /template

also Add env
API Keys
LIVE_KIT_API
LIVE_KIT_SRCRET
LIVE_KIT_URL
OPEN_Router_API
