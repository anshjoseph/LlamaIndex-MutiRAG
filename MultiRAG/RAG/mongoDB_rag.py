from typing import Any, Coroutine
from MultiRAG.Embeding.base import BaseEmbed
from .base import BaseRAG
from pymongo import MongoClient
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core import VectorStoreIndex, StorageContext
from MultiRAG.DataModel import ProviderConfig, MongoDBConfig, MongoIngestionPipe
from llama_index.core.retrievers import VectorIndexRetriever

class MongoDB(BaseRAG):
    def __init__(self, embeding: BaseEmbed, config:ProviderConfig) -> None:
        super().__init__("MongoDB", embeding, config.chunk_size, config.overlapping)
        self.similarity_top_k = config.similarity_top_k
        self.config:MongoDBConfig = config.rag
        self.client = MongoClient(self.config.uri)
        
    async def append_index(self, nodes) -> Coroutine[Any, Any, str]:
        return super().append_index(nodes)
    
    async def get_docs_index(self, query: str, index: str):
        vector_store = MongoDBAtlasVectorSearch(
            self.client,
            db_name = self.config.db,
            collection_name = self.config.collection_name,
            index_name = index
        )
        vector_store_context = StorageContext.from_defaults(vector_store=vector_store)
        vector_store_index = VectorStoreIndex(nodes=[],storage_context=vector_store_context)
        vector_store_retriever = VectorIndexRetriever(index=vector_store_index, similarity_top_k=self.similarity_top_k)
        return vector_store_retriever.retrieve(query)
    
    async def delete_index(self, index: str) -> Coroutine[Any, Any, bool]:
        return super().delete_index(index)
    
    async def add_index(self, nodes, config:MongoIngestionPipe) -> str:
        index = config.index
        vector_store = MongoDBAtlasVectorSearch(
            self.client,
            db_name = self.config.db,
            collection_name = self.config.collection_name,
            index_name = index
        )
        vector_store_context = StorageContext.from_defaults(vector_store=vector_store)
        vector_store_index = VectorStoreIndex(nodes=nodes,storage_context=vector_store_context,embed_model=self.embeding_model)
        return index

