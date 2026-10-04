from concurrent.futures import Future

from PySide6.QtCore import QObject, Signal, Slot

from communication.command_handler import CommandHandler
from communication.protocol import create_device_status


class QtCommunicationBridge(QObject):
    request_received = Signal(object)
    phone_event_received = Signal()

    def __init__(self, handler: CommandHandler):
        super().__init__()

        self.handler = handler

        self.request_received.connect(
            self.process_request
        )

    def submit(self, operation: str, payload: dict) -> Future:
        future = Future()

        self.request_received.emit({
            "operation": operation,
            "payload": payload,
            "future": future,
        })

        return future

    @Slot(object)
    def process_request(self, request):
        future = request["future"]

        if future.cancelled():
            return

        try:
            operation = request["operation"]
            payload = request["payload"]

            if operation == "status":
                result = create_device_status(
                    self.handler.assistant.state,
                    request_id=payload["request_id"],
                )

            elif operation == "command":
                result = self.handler.handle_command(
                    payload
                )

            elif operation == "phone_event":
                result = self.handler.handle_phone_event(
                    payload
                )

                if result.get("success"):
                    self.phone_event_received.emit()

            else:
                raise ValueError(
                    "Unsupported communication operation."
                )

            future.set_result(result)

        except Exception as error:
            future.set_exception(error)