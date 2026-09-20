DEVICE_TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "set_lens_tint",
        "description": (
            "Set the ECLIPSE glasses lens tint to a specific "
            "percentage. A value of 0 means minimum tint, "
            "and 100 means maximum tint. "
            "Use this when the user explicitly requests "
            "a specific lens tint percentage."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "percent": {
                    "type": "integer",
                    "description": (
                        "The requested lens tint percentage, "
                        "from 0 to 100."
                    ),
                    "minimum": 0,
                    "maximum": 100,
                }
            },
            "required": ["percent"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]