"""
Push voice analysis to EspoCRM via REST API.
Configure via environment variables.
"""
import requests
import datetime
import os
import base64

ESPO_BASE = os.environ.get("ESPO_BASE", "http://localhost:8080/api/v1")
ESPO_USER = os.environ.get("ESPO_USER", "admin")
ESPO_PASS = os.environ.get("ESPO_PASS", "")

HEADERS = {
    "Authorization": f"Basic {base64.b64encode(f'{ESPO_USER}:{ESPO_PASS}'.encode()).decode()}",
    "Content-Type": "application/json"
}

def push_to_espocrm(result: dict, report: str, entity: str = "Meeting") -> str:
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    duration = result.get("duration", 0)
    audio_file = result.get("audio_file", "audio")
    mins = int(duration // 60)
    secs = int(duration % 60)
    duration_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"

    if entity == "Meeting":
        payload = {
            "name": f"Voice Note — {audio_file} ({duration_str})",
            "status": "Held",
            "dateStart": now,
            "dateEnd": now,
            "description": report,
            "duration": max(1, int(duration // 60)) or 1,
        }
    else:
        payload = {
            "name": f"Voice Note — {audio_file}",
            "post": report,
            "type": "Post",
        }

    url = f"{ESPO_BASE}/{entity}"
    r = requests.post(url, json=payload, headers=HEADERS, timeout=15)

    if r.status_code in (200, 201):
        return r.json().get("id", "unknown")
    else:
        raise Exception(f"EspoCRM error {r.status_code}: {r.text[:200]}")
