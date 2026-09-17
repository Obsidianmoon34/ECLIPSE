import sys

from PySide6.QtWidgets import QApplication

from models.system_state import EclipseState
from ui.hud_window import HUDWindow

from app.eclipse_controller import EclipseController
from services.notification_manager import NotificationManager


def main():
    
    app = QApplication(sys.argv)

    eclipse = EclipseState()

    controller = EclipseController(eclipse)
    notifications = NotificationManager(eclipse)


    window = HUDWindow(
        eclipse,
        controller,
        notifications,
    )
    
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()