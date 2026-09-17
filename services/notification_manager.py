from models.system_state import EclipseState, HUDState


class NotificationManager:
    def __init__(self, state: EclipseState):
        self.state = state
        self.previous_hud_state = None

    def can_display_notification(self):
        return (
            self.state.is_worn
            and self.state.hud_state != HUDState.SLEEP
        )

    def save_previous_state(self):
        if self.previous_hud_state is None:
            self.previous_hud_state = self.state.hud_state

    def restore_previous_state(self):
        if self.previous_hud_state is None:
            return

        previous = self.previous_hud_state
        self.previous_hud_state = None

        if not self.state.is_worn:
            self.state.hud_state = HUDState.SLEEP
            return

        if previous == HUDState.SLEEP:
            self.state.hud_state = HUDState.IDLE
        else:
            self.state.hud_state = previous


    def show_message(self, sender: str, text: str):
        if not self.can_display_notification():
            return False

        self.save_previous_state()

        message = self.state.phone.message

        message.active = True
        message.sender = sender
        message.text = text

        self.state.hud_state = HUDState.MESSAGE

        return True

    def dismiss_message(self):
        message = self.state.phone.message

        message.active = False
        message.sender = ""
        message.text = ""

        self.restore_previous_state()

    def show_incoming_call(
        self,
        caller_name: str,
        caller_number: str = "",
    ):
        if not self.can_display_notification():
            return False

        self.save_previous_state()

        call = self.state.phone.call

        call.active = True
        call.caller_name = caller_name
        call.caller_number = caller_number

        self.state.hud_state = HUDState.INCOMING_CALL

        return True

    def dismiss_call(self):
        call = self.state.phone.call

        call.active = False
        call.caller_name = ""
        call.caller_number = ""

        self.restore_previous_state()