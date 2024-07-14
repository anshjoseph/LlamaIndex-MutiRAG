from .Base import BaseEmbed
from llama_index.embeddings.openai import OpenAIEmbedding
import dotenv
import os
dotenv.load_dotenv()
class OpenAI(BaseEmbed):
    def __init__(self,name:str,model:str) -> None:
        self.name = name
        self.model = model
        if os.getenv("OPENAI_KEY") is None:
            raise "OPENAI KEY IS NOT FOUND"
        self.embeding = OpenAIEmbedding(model=model,api_key=os.getenv("OPENAI_KEY"))
    def get_embeding(self):
        return self.embeding