import os

import httpx
from dotenv import load_dotenv

from communication.protocol import create_command


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


def test_live_command():
    command = create_command(
        request_id="local-command-001",
        name="set_lens_tint",
        arguments={
            "percent": 65,
        },
    )

    response = httpx.post(
        f"{BASE_URL}/api/command",
        json=command,
        headers=headers,
        timeout=10,
    )

    print(f"HTTP status: {response.status_code}")

    response.raise_for_status()

    result = response.json()

    assert result["type"] == "command_result"
    assert result["request_id"] == "local-command-001"
    assert result["success"] is True

    print(f"Result: {result['message']}")

    # Read the device state back from the running simulator.
    status_response = httpx.get(
        f"{BASE_URL}/api/status",
        params={
            "request_id": "local-status-002",
        },
        headers=headers,
        timeout=10,
    )

    status_response.raise_for_status()

    status = status_response.json()

    assert status["data"]["lens_tint_percent"] == 65

    print(
        f"Verified lens tint: "
        f"{status['data']['lens_tint_percent']}%"
    )

    print("\nLive command test passed!")


if __name__ == "__main__":
    test_live_command()