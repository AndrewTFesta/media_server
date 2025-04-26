"""
@title

@description

"""

import ollama

SYSTEM_MESSAGE = """You are a discord bot that enjoys engaging in riveting conversations with users. You match the energy and style of who you are speaking with.
"""

class OllamaServer:

    OLLAMA_SERVER_URL = 'http://localhost:11434'

    def __init__(self, model_name):
        self.client = ollama.Client(host=self.OLLAMA_SERVER_URL)
        self.model_name = model_name

        self.__load_model()
        return

    def __load_model(self):
        client_models = [each_model.model for each_model in self.client.list().models]
        if not self.model_name in client_models:
            self.client.pull(self.model_name, stream=True)
        return

    def embed_text(self, query):
        raise NotImplemented

    def gen_text(self, query):
        if isinstance(query, str):
            query = [{'role': 'user', 'content': query}]
        first_message = query[0]
        if first_message['role'] != 'system':
            query.insert(0, {'role': 'system', 'content': SYSTEM_MESSAGE})

        response = self.client.chat(
            model=self.model_name,
            messages=query
        )
        return response.message.content