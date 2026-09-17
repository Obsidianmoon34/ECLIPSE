from models.system_state import EclipseState, HUDState


class AssistantService:
    def __init__(self, state: EclipseState):
        self.state = state

    def start_listening(self):
        if not self.state.is_worn:
            return False

        self.state.transcript = ""
        self.state.assistant_response = ""
        self.state.hud_state = HUDState.LISTENING

        return True

    def update_transcript(self, text: str):
        if self.state.hud_state != HUDState.LISTENING:
            return

        self.state.transcript = text

    def clear_transcript(self):
        self.state.transcript = ""

    def start_thinking(self):
        if not self.state.is_worn:
            return

        self.state.transcript = ""
        self.state.hud_state = HUDState.THINKING

    def start_responding(self):
        if not self.state.is_worn:
            return

        self.state.assistant_response = ""
        self.state.hud_state = HUDState.RESPONDING

    def update_response(self, text: str):
        if self.state.hud_state != HUDState.RESPONDING:
            return

        self.state.assistant_response = text

    def cancel_interaction(self):
        self.state.transcript = ""
        self.state.assistant_response = ""