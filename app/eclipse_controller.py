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

    def set_lens_tint(self, percent: int):
        if isinstance(percent, bool) or not isinstance(percent, int):
            raise ValueError(
                "Lens tint percentage must be an integer."
            )
        
        if not 0 <= percent <= 100:
            raise ValueError(
                "Lens tint percentage must be between 0 and 100."
            )

        self.state.lens_tint_percent = percent

        self.state.auto_tint_enabled = False

        return {
            "success": True,
            "tint_percent": percent,
            "message": f"Lens tint set to {percent}%."
        }

        