import sys

from PySide6.QtWidgets import QApplication

from models.system_state import EclipseState
from ui.hud_window import HUDWindow


def main():
    
    app = QApplication(sys.argv)

    eclipse = EclipseState()

    window = HUDWindow(eclipse)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()