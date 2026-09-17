from dataclasses import dataclass
from enum import Enum
from models.phone_state import PhoneState

class HUDState(Enum):
    IDLE = "idle"
    HOME = "home"
    LISTENING = "listening"
    THINKING = "thinking"
    RESPONDING = "responding"
    NAVIGATION = "navigation"


@dataclass
class EclipseState:
    hud_state: HUDState = HUDState.HOME

    battery_percent: int = 100

    lens_tint_percent: int = 0
    auto_tint_enabled: bool = True
    night_mode_enabled: bool = False

    transcript: str = ""
    assistant_response: str = ""

    phone: PhoneState = None

    def __post_init__(self):
        if self.phone is None:
            self.phone = PhoneState()