def get_chat_model():
    """Returns a dummy chat model for testing"""
    class DummyChatModel:
        def invoke(self, messages):
            class Response:
                content = "Simulated answer from NeoStats AI."
            return Response()
    return DummyChatModel()

