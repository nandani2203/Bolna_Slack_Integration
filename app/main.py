from fastapi import FastAPI, Request
from app.slack import send_slack_alert
from app.config import AGENT_CHANNEL_MAP, UNKNOWN_SLACK_URL

app = FastAPI()

TRIGGER_STATUSES = {"completed"}


@app.post("/webhook")
async def bolna_webhook(request: Request):
    payload = await request.json()

    status = payload.get("status", "")
    if status not in TRIGGER_STATUSES:
        return {"message": f"Status '{status}' ignored"}

    call_id    = payload.get("id", "N/A")
    agent_id   = payload.get("agent_id", "N/A")
    duration   = payload.get("telephony_data", {}).get("duration", 0)
    transcript = payload.get("transcript", "")

    slack_url  = AGENT_CHANNEL_MAP.get(agent_id, UNKNOWN_SLACK_URL)

    await send_slack_alert(call_id, agent_id, duration, transcript, slack_url)

    return {"message": f"Alert sent for agent {agent_id}"}


@app.get("/")
async def health_check():
    return {"status": "server is running"}