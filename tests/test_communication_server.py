import os
import threading

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from PySide6.QtCore import QCoreApplication, QObject, Signal, Slot, Qt

from app.eclipse_controller import EclipseController
from communication.command_handler import CommandHandler
from communication.protocol import create_command
from communication.qt_bridge import QtCommunicationBridge
from communication.server import app, configure_server
from models.system_state import EclipseState
from services.assistant_service import AssistantService
from tools.device_tools import register_device_tools
from tools.tool_registry import ToolRegistry

class TestCompletion(QObject):
    finished = Signal()

    @Slot()
    def stop_event_loop(self):
        QCoreApplication.instance().quit()


def test_communication_server():
    load_dotenv()

    token = os.getenv("ECLIPSE_PHONE_TOKEN")

    assert token, (
        "ECLIPSE_PHONE_TOKEN is missing from .env."
    )

    # Create the Qt application and shared simulator state.
    qt_app = QCoreApplication.instance()

    if qt_app is None:
        qt_app = QCoreApplication([])

    state = EclipseState()
    controller = EclipseController(state)

    registry = ToolRegistry()
    register_device_tools(registry, controller)

    assistant = AssistantService(
        state,
        registry,
    )

    handler = CommandHandler(assistant)

    # Create the bridge on the main Qt thread.
    bridge = QtCommunicationBridge(handler)

    configure_server(bridge=bridge)

    controller.glasses_put_on()

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # HTTP requests run in a background thread.
    # The main thread processes Qt events.
    results = []
    errors = []

    completion = TestCompletion()

    completion.finished.connect(
        completion.stop_event_loop,
        Qt.ConnectionType.QueuedConnection,
    )

    def run_http_tests():
        print("[TEST] HTTP thread started.", flush=True)

        try:
            with TestClient(app) as client:
                print("[TEST] TestClient opened.", flush=True)

                # 1. Reject a request without authentication.
                unauthorized = client.get(
                    "/api/status",
                    params={"request_id": "status-001"},
                )

                assert unauthorized.status_code == 401

                results.append(
                    "Unauthorized request rejection passed!"
                )

                # 2. Retrieve device status with authentication.
                print("[TEST] Sending authenticated status request.", flush=True)
                status_response = client.get(
                    "/api/status",
                    params={"request_id": "status-002"},
                    headers=headers,
                )
                print("[TEST] Status request returned.", flush=True)


                print(
                    f"[TEST] HTTP status: {status_response.status_code}",
                    flush=True,
                )

                print(
                    f"[TEST] Response: {status_response.json()}",
                    flush=True,
                )               

                assert status_response.status_code == 200

                status = status_response.json()

                assert status["type"] == "device_status"
                assert status["request_id"] == "status-002"
                assert status["data"]["is_worn"] is True

                results.append(
                    "Authenticated device status passed!"
                )

                # 3. Execute an approved command.
                command = create_command(
                    request_id="phone-001",
                    name="set_lens_tint",
                    arguments={"percent": 65},
                )

                command_response = client.post(
                    "/api/command",
                    json=command,
                    headers=headers,
                )

                assert command_response.status_code == 200

                result = command_response.json()

                assert result["type"] == "command_result"
                assert result["success"] is True

                results.append(
                    "Authenticated lens tint command passed!"
                )

                # 4. Reject an invalid lens tint percentage.
                invalid_command = create_command(
                    request_id="phone-002",
                    name="set_lens_tint",
                    arguments={"percent": 150},
                )

                invalid_response = client.post(
                    "/api/command",
                    json=invalid_command,
                    headers=headers,
                )

                assert invalid_response.status_code == 200
                assert invalid_response.json()["success"] is False

                results.append(
                    "Invalid lens tint rejection passed!"
                )

                # 5. Reject an unsupported command.
                unsupported_command = create_command(
                    request_id="phone-003",
                    name="delete_everything",
                    arguments={},
                )

                unsupported_response = client.post(
                    "/api/command",
                    json=unsupported_command,
                    headers=headers,
                )

                assert unsupported_response.status_code == 200
                assert unsupported_response.json()["success"] is False

                results.append(
                    "Unsupported command rejection passed!"
                )

                # 6. Verify the device's final state.
                final_status_response = client.get(
                    "/api/status",
                    params={"request_id": "status-003"},
                    headers=headers,
                )

                assert final_status_response.status_code == 200

                final_status = final_status_response.json()

                assert final_status["data"]["lens_tint_percent"] == 65
                assert final_status["data"]["auto_tint_enabled"] is False

                results.append(
                    "Final device state verification passed!"
                )

        except Exception as error:
            print(
                f"[TEST ERROR] {type(error).__name__}: {error}",
                flush=True,
            )

            errors.append(error)

        finally:
            print(
                "[TEST] HTTP thread finished.",
                flush=True,
            )

            completion.finished.emit()

    test_thread = threading.Thread(
        target=run_http_tests,
        name="ECLIPSEServerTest",
    )

    test_thread.start()

    # Process Qt signals while the HTTP tests run.
    qt_app.exec()

    test_thread.join(timeout=5)

    assert not test_thread.is_alive(), (
        "HTTP test thread did not finish."
    )

    if errors:
        raise errors[0]

    for message in results:
        print(message)

    print("\nCommunication server test passed!")


if __name__ == "__main__":
    test_communication_server()