from tools.tool_registry import ToolRegistry


def test_tool_registry():

    registry = ToolRegistry()

    def test_function(value):
        return value * 2

    registry.register_tool(
        "double_number",
        test_function
    )

    result = registry.execute_tool(
        "double_number",
        value=5
    )

    assert result == 10

    assert "double_number" in registry.list_tools()

    print("Tool registry test passed!")


if __name__ == "__main__":
    test_tool_registry()