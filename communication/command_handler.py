from communication.protocol import (
    PROTOCOL_VERSION,
    create_command_result,
)

from services.assistant_service import AssistantService


class CommandHandler:
    def __init__(
        self,
        assistant: AssistantService,
    ):
        self.assistant = assistant

    def handle_command(self, message: dict) -> dict:
        if not isinstance(message, dict):
            raise TypeError(
                "Command message must be a dictionary."
            )

        request_id = message.get("request_id")
        name = message.get("name")

        if not isinstance(request_id, str) or not request_id:
            raise ValueError(
                "Command request ID is missing or invalid."
            )

        if not isinstance(name, str) or not name:
            raise ValueError(
                "Command name is missing or invalid."
            )

        if message.get("version") != PROTOCOL_VERSION:
            return create_command_result(
                request_id=request_id,
                name=name,
                success=False,
                message="Unsupported protocol version.",
            )

        if message.get("type") != "command":
            return create_command_result(
                request_id=request_id,
                name=name,
                success=False,
                message="Invalid message type.",
            )

        arguments = message.get("arguments")

        if not isinstance(arguments, dict):
            return create_command_result(
                request_id=request_id,
                name=name,
                success=False,
                message="Command arguments must be a dictionary.",
            )

        # Only commands explicitly permitted for phone control.
        allowed_commands = {
            "set_lens_tint",
        }

        if name not in allowed_commands:
            return create_command_result(
                request_id=request_id,
                name=name,
                success=False,
                message="Command is not permitted.",
            )

        result = self.assistant.process_assistant_output({
            "type": "tool_call",
            "name": name,
            "arguments": arguments,
        })

        if result["type"] == "tool_result":
            tool_result = result["result"]

            return create_command_result(
                request_id=request_id,
                name=name,
                success=tool_result["success"],
                message=tool_result["message"],
            )

        return create_command_result(
            request_id=request_id,
            name=name,
            success=False,
            message=result.get(
                "message",
                "Command execution failed.",
            ),
        )