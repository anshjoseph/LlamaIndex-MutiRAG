from typing import Any, Coroutine
import pymongo
from LlamaIndexRAG.Embeding.Base import BaseEmbed
from .Base import BaseProvider
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core import VectorStoreIndex, StorageContext
from LlamaIndexRAG.DataModel import ProviderConfig

class MongoDB(BaseProvider):
    def __init__(self, embeding: BaseEmbed, config:ProviderConfig) -> None:
        super().__init__("MongoDB", embeding, config.chunk_size, config.overlapping)
    async def append_index(self, nodes) -> Coroutine[Any, Any, str]:
        return super().append_index(nodes)
    async def get_docs_index(self, query: str, index: str):
        return super().get_docs_index(query, index)
    async def delete_index(self, index: str) -> Coroutine[Any, Any, bool]:
        return super().delete_index(index)
    async def add_index(self, nodes) -> str:
        return await super().add_index(nodes)