import sys

from PySide6.QtCore import QCoreApplication, QThread, QTimer

from app.eclipse_controller import EclipseController
from models.system_state import EclipseState
from services.ai_service import AIService
from services.ai_worker import AIWorker
from services.assistant_service import AssistantService
from tools.device_tools import register_device_tools
from tools.tool_registry import ToolRegistry


def test_ai_worker():
    app = QCoreApplication(sys.argv)

    state = EclipseState()
    controller = EclipseController(state)

    registry = ToolRegistry()
    register_device_tools(registry, controller)

    assistant = AssistantService(
        state,
        registry,
        ai_service=AIService(),
    )

    controller.glasses_put_on()

    thread = QThread()

    worker = AIWorker(
        assistant=assistant,
        interaction_id=1,
        user_message=(
            "What is augmented reality? "
            "Answer in one short sentence."
        ),
    )

    worker.moveToThread(thread)

    results = {
        "response": None,
        "error": None,
    }

    def handle_response(interaction_id, response):
        results["response"] = response

        print("\nECLIPSE AI RESPONSE:")
        print(response)

        print(f"\nInteraction ID: {interaction_id}")

    def handle_error(interaction_id, message):
        results["error"] = message

        print(
            f"\nAI request failed "
            f"(interaction {interaction_id}): {message}"
        )

    thread.started.connect(worker.run)

    worker.response_ready.connect(handle_response)
    worker.error_occurred.connect(handle_error)

    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)

    thread.finished.connect(app.quit)

    # Safety timeout: stop waiting if the request takes too long.
    QTimer.singleShot(45000, thread.quit)

    thread.start()

    app.exec()

    # The thread must finish before the test exits.
    if thread.isRunning():
        thread.wait()

    assert results["error"] is None, results["error"]
    assert isinstance(results["response"], str)
    assert results["response"].strip()

    print("\nAI background worker test passed!")


if __name__ == "__main__":
    test_ai_worker()