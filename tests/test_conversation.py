from chatbot.conversation import call_llm

def test_call_llm_basic():
    response, _ = call_llm("Hello!", [])
    assert isinstance(response, str)
    assert len(response) > 0
