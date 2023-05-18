import openai


class OpenAiClient:
    MAX_TOKENS = 200
    MODEL = "text-davinci-003"
    def __init__(self, api_key):
        openai.api_key = api_key
        self._max_tokens = 200
        self._model = "text-davinci-003"
