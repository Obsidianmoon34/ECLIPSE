from PySide6.QtCore import QObject, Signal, Slot

from services.assistant_service import AssistantService


import json

class AIWorker(QObject):
    response_ready = Signal(int, str)
    error_occurred = Signal(int, str)
    tool_calls_ready = Signal(int, object)
    finished = Signal()

    def __init__(
        self,
        assistant: AssistantService,
        interaction_id: int,
        user_message: str,
    ):
        super().__init__()

        self.assistant = assistant
        self.interaction_id = interaction_id
        self.user_message = user_message

    @Slot()
    def run(self):
        try:
            ai = self.assistant.ai_service

            if ai is None:
                raise RuntimeError(
                    "ECLIPSE AI service is not configured."
                )

            response = ai.generate_with_tools(
                self.user_message,
                self.assistant.registry,
            )

            tool_calls = []

            for item in response.output:
                if item.type != "function_call":
                    continue

                tool_calls.append({
                    "name": item.name,
                    "arguments": json.loads(item.arguments),
                })

            if tool_calls:
                self.tool_calls_ready.emit(
                    self.interaction_id,
                    tool_calls,
                )

            else:
                self.response_ready.emit(
                    self.interaction_id,
                    response.output_text,
                )

        except Exception as error:
            self.error_occurred.emit(
                self.interaction_id,
                str(error),
            )

        finally:
            self.finished.emit()