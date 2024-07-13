from uuid import uuid4
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_parse import LlamaParse

class BaseProvider:
    def __init__(self,provider:str) -> None:
        self.provider = provider
    def genrate_table_name(self):
        return str(uuid4())
    
    