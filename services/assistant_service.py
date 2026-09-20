from models.system_state import EclipseState, HUDState
from tools.tool_registry import ToolRegistry
from services.assistant_router import AssistantRouter
from services.ai_service import AIService


class AssistantService:
    def __init__(
        self, 
        state: EclipseState,
        registry: ToolRegistry,
        ai_service: AIService | None = None,
    ):
        self.state = state
        self.registry = registry

        self.router = AssistantRouter(registry)
        self.ai_service = ai_service

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


    def execute_tool(self, name: str, **kwargs):
        if not self.state.is_worn:
            return {
                "success": False,
                "message": "ECLIPSE is not being worn."
            }

        try:
            result = self.registry.execute_tool(
                name,
                **kwargs,
            )

            return result
        
        except (ValueError, TypeError) as error:
            return {
                "success": False,
                "message": str(error),
            }


    def process_assistant_output(self, output: dict):
        output_type = output.get("type")

        if output_type == "tool_call":
            if not self.state.is_worn:
                return {
                    "type": "error",
                    "message": "ECLIPSE is not being worn.",
                }

            name = output.get("name")
            arguments = output.get("arguments")

            if not isinstance(name, str) or not isinstance(
                arguments, dict
            ):

                return {
                    "type": "error",
                    "message": "Invalid tool request.",
                }

            return self.router.handle_tool_call(
                name=name,
                arguments=arguments,
            )

        elif output_type == "text_response":
            text = output.get("message")

            if not isinstance(text, str):
                return {
                    "type": "error",
                    "message": "Invalid assistant response.",
                }

            return self.router.handle_text_response(text)

        return {
            "type": "error",
            "message": "Unknown assistant output type.",
        }

    def generate_ai_response(self, user_message: str) -> str:
        if self.ai_service is None:
            raise RuntimeError(
                "ECLIPSE AI service is not configured."
            )

        if not self.state.is_worn:
            raise RuntimeError(
                "ECLIPSE is not being worn."
            )

        return self.ai_service.generate_response(user_message)