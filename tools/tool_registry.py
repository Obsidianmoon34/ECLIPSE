class ToolRegistry:
    def __init__(self):
        self.tools = {}

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