from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from models.system_state import EclipseState, HUDState

from app.eclipse_controller import EclipseController
from services.notification_manager import NotificationManager


class HUDWindow(QMainWindow):
    def __init__(
        self, 
        eclipse_state: EclipseState,
        controller: EclipseController,
        notifications: NotificationManager,
    ):

        super().__init__()

        self.eclipse_state = eclipse_state

        self.controller = controller
        self.notifications = notifications

        self.home_timeout_ms = 10_000

        self.home_timeout = QTimer(self)
        self.home_timeout.setSingleShot(True)
        self.home_timeout.timeout.connect(self.handle_home_timeout)

        self.message_timeout_ms = 5_000

        self.message_timeout = QTimer(self)
        self.message_timeout.setSingleShot(True)
        self.message_timeout.timeout.connect(
            self.handle_message_timeout
        )

        self.setWindowTitle("ECLIPSE - AR Monocle Simulator")
        self.resize(800, 500)

        self.setStyleSheet("""
            QMainWindow {
                background-color: black;
            }

            QLabel {
                color: white;
                font-family: Arial;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)

        self.content_label = QLabel()
        self.content_label.setAlignment(Qt.AlignCenter)

        self.layout.addStretch()
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.content_label)
        self.layout.addStretch()

        self.update_hud()

    def update_hud(self):
        state = self.eclipse_state

        if state.hud_state == HUDState.SLEEP:
            self.show_sleep()

        elif state.hud_state == HUDState.IDLE:
            self.show_idle()

        elif state.hud_state == HUDState.HOME:
            self.show_home()

        elif state.hud_state == HUDState.LISTENING:
            self.show_listening()

        elif state.hud_state == HUDState.THINKING:
            self.show_thinking()

        elif state.hud_state == HUDState.RESPONDING:
            self.show_response()

        elif state.hud_state == HUDState.MESSAGE:
            self.show_message()
        
        elif state.hud_state == HUDState.INCOMING_CALL:
            self.show_call()

    def show_sleep(self):
        self.title_label.setText("")
        self.content_label.setText("")

    def show_idle(self):
        self.title_label.setText("")
        self.content_label.setText("")

    def show_home(self):
        state = self.eclipse_state

        phone_status = "●" if state.phone.connected else "○"

        self.title_label.setText("E C L I P S E")

        content = (
            f"Battery: {state.battery_percent}%\n"
            f"Tint: {state.lens_tint_percent}%\n"
            f"Phone: {phone_status}"
        )

        if state.phone.media.playing:
            content += (
                f"\n\n♪ {state.phone.media.title}\n"
                f"{state.phone.media.artist}"
            )

        self.content_label.setText(content)

    def show_listening(self):
        self.title_label.setText("●")
        self.content_label.setText("Listening...")

    def show_thinking(self):
        self.title_label.setText("○")
        self.content_label.setText("Thinking...")

    def show_response(self):
        self.title_label.setText("E C L I P S E")
        self.content_label.setText(
            self.eclipse_state.assistant_response
        )

    def show_message(self):
        message = self.eclipse_state.phone.message

        self.title_label.setText("MESSAGE")

        self.content_label.setText(
            f"{message.sender}\n\n"
            f"{message.text}"
        )

    def show_call(self):
        call = self.eclipse_state.phone.call

        self.title_label.setText("INCOMING CALL")

        caller = call.caller_name or call.caller_number

        self.content_label.setText(caller)

    def handle_home_timeout(self):
        self.controller.enter_idle()
        self.update_hud()

    def start_message_timer(self):
        self.home_timeout.stop()
        self.message_timeout.start(self.message_timeout_ms)


    def handle_message_timeout(self):
        self.notifications.dismiss_message()

        if self.eclipse_state.hud_state == HUDState.HOME:
            self.home_timeout.start(self.home_timeout_ms)

        self.update_hud()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()

        # G = put glasses on
        if key == Qt.Key_G:
            self.controller.glasses_put_on()

            self.home_timeout.start(self.home_timeout_ms)

        # R = remove glasses
        elif key == Qt.Key_R:
            self.controller.glasses_removed()

            self.home_timeout.stop()

        # T = double-tap temple
        elif key == Qt.Key_T:
            self.controller.enter_home()

            if self.eclipse_state.is_worn:
                self.home_timeout.start(self.home_timeout_ms)

        # W = "Hey Eclipse"
        elif key == Qt.Key_W:
            self.controller.wake_eclipse()

            self.home_timeout.stop()

        # P = music starts/stops
        elif key == Qt.Key_P:
            media = self.eclipse_state.phone.media

            media.playing = not media.playing

            if media.playing:
                self.eclipse_state.phone.connected = True
                media.title = "Blinding Lights"
                media.artist = "The Weeknd"

            else:
                media.title = ""
                media.artist = ""

        # M = incoming message
        elif key == Qt.Key_M:
            self.eclipse_state.phone.connected = True

            displayed = self.notifications.show_message(
                sender="Alex",
                text="Are you almost here?",
            )

            if displayed:
                self.start_message_timer()

        # C = incoming call
        elif key == Qt.Key_C:
            self.eclipse_state.phone.connected = True

            self.notifications.show_incoming_call(
                caller_name="Alex",
                caller_number="(555) 123-4567",
            )

        # E = simulate call ending
        elif key == Qt.Key_E:
            self.notifications.dismiss_call()

        self.update_hud()