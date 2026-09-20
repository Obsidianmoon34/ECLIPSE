from copy import deepcopy

class ToolRegistry:
    def __init__(self):
        self.tools = {}
        self.definitions = {}

    def register_tool(self, name: str, function):
        if name in self.tools:
            raise ValueError(
                f"Tool '{name}' is already registered."
            )

        self.tools[name] = function

    def execute_tool(self, name: str, **kwargs):
        if name not in self.tools:
            raise ValueError(
                f"Unknown tool: {name}"
            )

        function = self.tools[name]

        return function(**kwargs)

    def list_tools(self):
        return list(self.tools.keys())

    def register_definition(self, definition: dict):
        name = definition["name"]

        if name not in self.tools:
            raise ValueError(
                f"Cannot define unregistered tool: {name}"
            )

        if name in self.definitions:
            raise ValueError(
                f"Tool definition already exists: {name}"
            )

        self.definitions[name] = deepcopy(definition)


    def get_tool_definitions(self):
        return [
            deepcopy(definition)
            for definition in self.definitions.values()
        ]