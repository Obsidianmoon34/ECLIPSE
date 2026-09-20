from PySide6.QtCore import QObject, Signal, Slot

from services.assistant_service import AssistantService


class AIWorker(QObject):
    response_ready = Signal(int, str)
    error_occurred = Signal(int, str)
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
            response = self.assistant.generate_ai_response(
                self.user_message
            )

            self.response_ready.emit(
                self.interaction_id,
                response,
            )

        except Exception as error:
            self.error_occurred.emit(
                self.interaction_id,
                str(error),
            )

        finally:
            self.finished.emit()