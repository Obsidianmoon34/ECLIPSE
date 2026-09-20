from services.ai_service import AIService


def test_ai_service():
    ai = AIService()

    response = ai.generate_response(
        "What is augmented reality? "
        "Answer in one short sentence."
    )

    assert isinstance(response, str)
    assert response.strip()

    print("\nECLIPSE AI RESPONSE:")
    print(response)

    print("\nAI service test passed!")


if __name__ == "__main__":
    test_ai_service()