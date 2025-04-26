"""
@title

@description

"""
import os
from collections import defaultdict

from google import genai


class GeminiServer:

    def __init__(self, model_name):
        """
        https://aistudio.google.com/u/2/plan_information
        https://ai.google.dev/gemini-api/docs/text-generation?authuser=2
        https://ai.google.dev/gemini-api/docs/rate-limits#free-tier

        :param model_name:
        """
        gemini_key = os.environ.get('GEMINI_KEY')
        self.client = genai.Client(api_key=gemini_key)
        self.model_name = model_name

        self.history = defaultdict(list)
        return

    def embed_text(self, query, user_id):
        raise NotImplemented

    def gen_text(self, query, user_id, history_length=5):
        response = self.client.models.generate_content(model=self.model_name, contents=query)
        response_text = response.text
        return response_text
