import os
import json
from dotenv import load_dotenv

load_dotenv()

with open("config.json") as f:
    agent_config = json.load(f)

SLACK_URLS = {
    "announcements": os.getenv("SLACK_WEBHOOK_ANNOUNCEMENTS"),
    "reminders":     os.getenv("SLACK_WEBHOOK_REMINDERS"),
    "unknown":       os.getenv("SLACK_WEBHOOK_UNKNOWN"),
}

AGENT_CHANNEL_MAP = {}

for agent_type, agents in agent_config.items():
    for index, agent_id in agents.items():
        if agent_id.strip():
            AGENT_CHANNEL_MAP[agent_id.strip()] = SLACK_URLS[agent_type]

UNKNOWN_SLACK_URL = SLACK_URLS["unknown"]