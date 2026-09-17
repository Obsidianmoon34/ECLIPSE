from models.system_state import EclipseState, HUDState


class EclipseController:
    def __init__(self, state: EclipseState):
        self.state = state

    def glasses_put_on(self):
        self.state.is_worn = True
        self.state.hud_state = HUDState.HOME

    def glasses_removed(self):
        self.state.is_worn = False
        self.state.hud_state = HUDState.SLEEP

    def enter_home(self):
        if not self.state.is_worn:
            return

        self.state.hud_state = HUDState.HOME

    def enter_idle(self):
        if not self.state.is_worn:
            return

        self.state.hud_state = HUDState.IDLE

    def wake_eclipse(self):
        if not self.state.is_worn:
            return

        self.state.hud_state = HUDState.LISTENING