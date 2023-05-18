import openai


class OpenAiClient:
    MAX_TOKENS = 200
    MODEL = "text-davinci-003"

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

    def get_slide_explanation(self, slide_txt):
        response = openai.Completion.create(
            model=self.MAX_TOKENS,
            prompt=self._set_prompt(slide_txt),
            max_tokens=self.MODEL)
        return response["choices"][0]["text"]
