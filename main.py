import sys

from PySide6.QtWidgets import QApplication

from models.system_state import EclipseState
from ui.hud_window import HUDWindow

from app.eclipse_controller import EclipseController
from services.notification_manager import NotificationManager

from services.assistant_service import AssistantService

from tools.tool_registry import ToolRegistry
from tools.device_tools import register_device_tools

from services.ai_service import AIService

from communication.command_handler import CommandHandler
from communication.qt_bridge import QtCommunicationBridge
from communication.server import configure_server
from communication.server_runner import CommunicationServerRunner


def main():
    
    app = QApplication(sys.argv)

    eclipse = EclipseState()

    controller = EclipseController(eclipse)
    notifications = NotificationManager(eclipse)

    registry = ToolRegistry()

    register_device_tools(
        registry,
        controller,
    )

    assistant = AssistantService(
        eclipse,
        registry,
        ai_service=AIService(),
    )

    command_handler = CommandHandler(assistant)

    qt_bridge = QtCommunicationBridge(
        command_handler
    )

    configure_server(
        bridge=qt_bridge
    )

    window = HUDWindow(
        eclipse,
        controller,
        notifications,
        assistant,
    )

    window.show()

    communication_server = CommunicationServerRunner()
    communication_server.start()

    app.aboutToQuit.connect(
        communication_server.stop
    )

    sys.exit(app.exec())


if __name__ == "__main__":
    main()