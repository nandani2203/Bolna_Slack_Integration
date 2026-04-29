import httpx
import os
import json
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = "https://your-ngrok-url/webhook"

with open("config.json") as f:
    agent_config = json.load(f)


def run_tests():
    print("Starting webhook tests...\n")
    print("=" * 50)

    for agent_type, agents in agent_config.items():
        for index, agent_id in agents.items():
            if not agent_id.strip():
                continue

            print(f"\nTesting: {agent_type.capitalize()} Agent {index}")
            print(f"Agent ID : {agent_id}")

            payload = {
                "id": f"test-{agent_type}-{index}",
                "agent_id": agent_id,
                "status": "completed",
                "transcript": f"{agent_type.capitalize()} Agent {index} call transcript",
                "telephony_data": {"duration": 60}
            }

            response = httpx.post(WEBHOOK_URL, json=payload)
            print(f" Response : {response.json()}")
            print(f" Status : {response.status_code}" if response.status_code == 200 else f" Status : {response.status_code}")

    # Test unknown agent
    print(f"\nTesting: Unknown Agent")
    payload = {
        "id": "test-unknown",
        "agent_id": "random-unknown-id",
        "status": "completed",
        "transcript": "Unknown agent call",
        "telephony_data": {"duration": 20}
    }
    response = httpx.post(WEBHOOK_URL, json=payload)
    print(f"Response : {response.json()}")
    print(f"Status: {response.status_code}" if response.status_code == 200 else f"Status: {response.status_code}")

    print("\n" + "=" * 50)
    print("All tests done! Check your Slack channels:")
    print("   → #announcement-calls")
    print("   → #reminder-calls")
    print("   → #unknown-calls")


if __name__ == "__main__":
    run_tests()
