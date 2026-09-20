from tools.tool_registry import ToolRegistry


class AssistantRouter:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def handle_tool_call(
        self,
        name: str,
        arguments: dict,
    ):
        try:
            result = self.registry.execute_tool(
                name,
                **arguments,
            )

            return {
                "type": "tool_result",
                "tool_name": name,
                "result": result,
            }

        except (ValueError, TypeError) as error:
            return {
                "type": "error",
                "message": str(error),
            }

    def handle_text_response(self, text: str):
        return {
            "type": "text_response",
            "message": text,
        }