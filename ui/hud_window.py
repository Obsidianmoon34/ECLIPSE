from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from models.system_state import EclipseState, HUDState


class HUDWindow(QMainWindow):
    def __init__(self, eclipse_state: EclipseState):
        super().__init__()

        self.eclipse_state = eclipse_state

        self.home_timeout_ms = 10_000

        self.home_timeout = QTimer(self)
        self.home_timeout.setSingleShot(True)
        self.home_timeout.timeout.connect(self.enter_idle)

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

        if state.phone.call.active:
            self.show_call()

        elif state.phone.message.active:
            self.show_message()

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

    def enter_home(self):
        if not self.eclipse_state.is_worn:
            return

        self.eclipse_state.hud_state = HUDState.HOME
        self.home_timeout.start(self.home_timeout_ms)
        self.update_hud()

    def enter_idle(self):
        if not self.eclipse_state.is_worn:
            return

        self.eclipse_state.hud_state = HUDState.IDLE
        self.home_timeout.stop()
        self.update_hud()

    def enter_sleep(self):
        self.eclipse_state.is_worn = False
        self.eclipse_state.hud_state = HUDState.SLEEP

        self.home_timeout.stop()
        self.update_hud()

    def glasses_put_on(self):
        self.eclipse_state.is_worn = True
        self.enter_home()

    def wake_eclipse(self):
        if not self.eclipse_state.is_worn:
            return

        self.home_timeout.stop()
        self.eclipse_state.hud_state = HUDState.LISTENING
        self.update_hud()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()

        # G = simulate putting the glasses on
        if key == Qt.Key_G:
            self.glasses_put_on()

        # R = simulate removing the glasses
        elif key == Qt.Key_R:
            self.enter_sleep()

        # T = simulate double-tapping the temple
        elif key == Qt.Key_T:
            self.enter_home()

        # W = simulate saying "Hey Eclipse"
        elif key == Qt.Key_W:
            self.wake_eclipse()

        # P = simulate music playing/stopping on the phone
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

            self.enter_home()

        # M = simulate an incoming message
        elif key == Qt.Key_M:
            self.eclipse_state.phone.connected = True

            self.eclipse_state.phone.message.active = True
            self.eclipse_state.phone.message.sender = "Alex"
            self.eclipse_state.phone.message.text = "Are you almost here?"

        # C = simulate an incoming phone call
        elif key == Qt.Key_C:
            self.eclipse_state.phone.connected = True

            self.eclipse_state.phone.call.active = True
            self.eclipse_state.phone.call.caller_name = "Alex"
            self.eclipse_state.phone.call.caller_number = "(555) 123-4567"

        self.update_hud()