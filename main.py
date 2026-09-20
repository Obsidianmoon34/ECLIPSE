import sys

from PySide6.QtWidgets import QApplication

from models.system_state import EclipseState
from ui.hud_window import HUDWindow

from app.eclipse_controller import EclipseController
from services.notification_manager import NotificationManager

from services.assistant_service import AssistantService

from tools.tool_registry import ToolRegistry
from tools.device_tools import register_device_tools


def main():
    
    app = QApplication(sys.argv)

    eclipse = EclipseState()

    controller = EclipseController(eclipse)
    notifications = NotificationManager(eclipse)

    controller = EclipseController(eclipse)

    registry = ToolRegistry()

    register_device_tools(
        registry,
        controller,
    )

    notifications = NotificationManager(eclipse)
    assistant = AssistantService(
        eclipse,
        registry,
    )

    window = HUDWindow(
        eclipse,
        controller,
        notifications,
        assistant,
    )

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()