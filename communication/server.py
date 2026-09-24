import os
import secrets

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException

from communication.command_handler import CommandHandler
from communication.protocol import create_device_status

from concurrent.futures import TimeoutError as FutureTimeoutError
from communication.qt_bridge import QtCommunicationBridge


load_dotenv()

app = FastAPI(
    title="ECLIPSE Communication Server",
    version="0.1.0",
)

command_handler: CommandHandler | None = None
qt_bridge: QtCommunicationBridge | None = None


def configure_server(
    handler: CommandHandler | None = None,
    bridge: QtCommunicationBridge | None = None,
):
    global command_handler, qt_bridge

    command_handler = handler
    qt_bridge = bridge


def verify_phone_token(
    authorization: str | None = Header(default=None),
):
    expected_token = os.getenv("ECLIPSE_PHONE_TOKEN")

    if not expected_token:
        raise HTTPException(
            status_code=503,
            detail="Phone authentication is not configured.",
        )

    scheme, _, supplied_token = (
        authorization or ""
    ).partition(" ")

    if (
        scheme.lower() != "bearer"
        or not secrets.compare_digest(
            supplied_token,
            expected_token,
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized.",
        )


def get_command_handler() -> CommandHandler:
    if command_handler is None:
        raise HTTPException(
            status_code=503,
            detail="ECLIPSE command handler is not configured.",
        )

    return command_handler


@app.get("/api/status")
def get_status(
    request_id: str,
    _auth=Depends(verify_phone_token),
):
    return dispatch_to_qt(
        "status",
        {"request_id": request_id},
    )


@app.post("/api/command")
def execute_command(
    message: dict,
    _auth=Depends(verify_phone_token),
):
    return dispatch_to_qt(
        "command",
        message,
    )



def dispatch_to_qt(
    operation: str,
    payload: dict,
):
    if qt_bridge is None:
        raise HTTPException(
            status_code=503,
            detail="ECLIPSE Qt bridge is not configured.",
        )

    future = qt_bridge.submit(
        operation,
        payload,
    )

    try:
        return future.result(timeout=5)

    except FutureTimeoutError:
        future.cancel()

        raise HTTPException(
            status_code=504,
            detail="ECLIPSE did not respond in time.",
        )