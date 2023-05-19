import openai


class OpenAiClient:
    MAX_TOKENS = 200
    MODEL = "gpt-3.5-turbo"

    def __init__(self, api_key):
        openai.api_key = api_key

    @classmethod
    def _set_prompt(cls, slide_txt):
        """
        returns a prompt to send to openai based on a given slide tex
        :param slide_txt: the text of the slide
        :return: the prompt
        """

        return f"""
        Here is text extracted from a slide of a lecture presentation.
        explain (and elaborate when needed) the content of each slide in a concise and coherent manner.
        So that even a student who was not in the lecture will be able to understand the topic being discussed.

        The text of the slide:
        {slide_txt}
        
        Explanation of the topic following the text in the slide (6 - 7 sentences):
        """

    async def get_slide_explanation(self, slide_txt):
        response = await openai.ChatCompletion.acreate(
            model=self.MODEL,
            messages=[{"role": "user", "content": self._set_prompt(slide_txt)}],
            max_tokens=self.MAX_TOKENS)
        return response["choices"][0]["message"]["content"]
