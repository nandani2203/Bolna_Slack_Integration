## Problem Statement

Build an integration that sends a Slack alert whenever a Bolna call ends with the following information:
- `id` — Unique call ID
- `agent_id` — ID of the Bolna agent that made the call
- `duration` — Duration of the call in seconds
- `transcript` — Full transcript of the conversation

---

## Requirements

### External Services
- [Bolna Account](https://platform.bolna.ai) — with at least one agent created
- [Slack Workspace](https://slack.com) — with Incoming Webhooks enabled
- [ngrok Account](https://ngrok.com) — for local tunnel

### Python Dependencies

```
fastapi
uvicorn
httpx
python-dotenv

```

---

## Project Structure

```
bolna_assignment/
├── app/
│   ├── __init__.py        
│   ├── main.py            # FastAPI server, webhook endpoint
│   ├── slack.py           # Formats and sends Slack alerts
│   └── config.py          # Builds agent → Slack channel routing map
├── config.json            # Agent IDs grouped by type with indexes
├── .env                   
├── .gitignore
├── requirements.txt
├── test_webhook.py        # Simulates webhook calls for all agents
└── README.md
```

---

## Setup & Installation

### 1. Clone the repository

```
git clone https://github.com/nandani2203/Bolna_Slack_Integration.git
cd Bolna_Slack_Integration

```
### 2. Configure `.env`

Create a `.env` file in the root folder:

```
SLACK_WEBHOOK_ANNOUNCEMENTS=https://hooks.slack.com/services/...
SLACK_WEBHOOK_REMINDERS=https://hooks.slack.com/services/...
SLACK_WEBHOOK_UNKNOWN=https://hooks.slack.com/services/...

```

### 3. Configure `config.json`
Add your Bolna agent IDs grouped by type with indexes:

```
{
    "announcements": {
        "1": "your-announcements-agent-id-1",
        "2": "your-announcements-agent-id-2"
    },
    "reminders": {
        "1": "your-reminders-agent-id-1",
        "2": "your-reminders-agent-id-2"
    }
}

```
To add a new agent — just add a new entry under the correct type. No code changes needed.

---

### How to Run

## Windows

# 1. Create and activate virtual environment
```
python -m venv .venv
.venv\Scripts\activate
```

# 2. Install dependencies
```
& "path\to\.venv\Scripts\python.exe" -m pip install -r requirements.txt
```
# 3. You need 2 terminals running simultaneously.

**Terminal 1 — FastAPI Server:**
```
& "path\to\.venv\Scripts\uvicorn.exe" app.main:app --reload --port 8000
```
**Terminal 2 — ngrok Tunnel:**
```
ngrok http 8000
```
> After starting ngrok, copy the forwarding URL (e.g. `https://abc123.ngrok-free.app/webhook`) and paste it into each Bolna agent's **Analytics Tab** as the webhook URL. Save each agent after updating.

---

## Mac/Linux

# 1. Create and activate virtual environment
```
python -m venv .venv
source .venv/bin/activate
```
# 2. Install dependencies
```
pip install -r requirements.txt
```
# 3. You need 2 terminals running simultaneously.

**Terminal 1 — FastAPI Server:**
```
uvicorn app.main:app --reload --port 8000
```
**Terminal 2 — ngrok Tunnel:**
```
ngrok http 8000
```

> After starting ngrok, copy the forwarding URL (e.g. `https://abc123.ngrok-free.app/webhook`) and paste it into each Bolna agent's **Analytics Tab** as the webhook URL. Save each agent after updating.

---

### Testing

> Before running, update `WEBHOOK_URL` in `test_webhook.py` with your current ngrok forwarding URL.

## Windows
```
& "path\to\.venv\Scripts\python.exe" test_webhook.py
```

## Mac/Linux
```
python test_webhook.py
```

Simulates completed calls for all agents and verifies:
- Correct Slack channel routing per agent type
- Slack alerts delivered to correct channels
- Unknown agent fallback works correctly

---

## How It Works

### Flow
```
Bolna Call Ends
      │
      ▼
POST /webhook (FastAPI)
      │  filters: only "completed" status
      ▼
Route by agent_id
      │
      ├──▶ #announcement-calls
      ├──▶ #reminder-calls
      └──▶ #unknown-calls (fallback for unrecognised agents)
```

> Note: Bolna fires the webhook on every status change (scheduled → queued → in-progress → completed). We only act on `completed` to avoid duplicate alerts.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Webhook receiver — async REST API server |
| httpx | Async HTTP client — sends Slack alerts |
| python-dotenv | Loads secrets from `.env` file |
| ngrok | Local tunnel — exposes localhost to internet |
