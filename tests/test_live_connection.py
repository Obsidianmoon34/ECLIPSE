import os

import httpx
from dotenv import load_dotenv


load_dotenv()

BASE_URL = "http://127.0.0.1:8765"

token = os.getenv("ECLIPSE_PHONE_TOKEN")

if not token:
    raise RuntimeError(
        "ECLIPSE_PHONE_TOKEN is missing from .env."
    )

headers = {
    "Authorization": f"Bearer {token}",
}


def test_live_connection():
    response = httpx.get(
        f"{BASE_URL}/api/status",
        params={
            "request_id": "local-status-001",
        },
        headers=headers,
        timeout=10,
    )

    print(f"HTTP status: {response.status_code}")

    response.raise_for_status()

    status = response.json()

    assert status["type"] == "device_status"
    assert status["request_id"] == "local-status-001"

    print("\nECLIPSE DEVICE STATUS")
    print(f"Battery: {status['data']['battery_percent']}%")
    print(f"Lens tint: {status['data']['lens_tint_percent']}%")
    print(f"Auto tint: {status['data']['auto_tint_enabled']}")
    print(f"Glasses worn: {status['data']['is_worn']}")

    print("\nLive connection test passed!")


if __name__ == "__main__":
    test_live_connection()