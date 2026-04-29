import httpx
from dotenv import load_dotenv

load_dotenv()


async def send_slack_alert(call_id: str, agent_id: str, duration: int, transcript: str, slack_url: str):
    duration_str = f"{duration} seconds" if duration else "N/A"
    transcript_str = transcript.strip() if transcript else "No transcript available"

    message = {
        "text": (
            f"🔔 *Bolna Call Ended*\n\n"
            f"*Call ID:* `{call_id}`\n"
            f"*Agent ID:* `{agent_id}`\n"
            f"*Duration:* {duration_str}\n\n"
            f"*Transcript:*\n```{transcript_str}```"
        )
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(slack_url, json=message)
        response.raise_for_status()