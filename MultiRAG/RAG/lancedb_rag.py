from typing import Any, Coroutine
from MultiRAG.Embeding.base import BaseEmbed
from .base import BaseRAG
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from MultiRAG.DataModel import ProviderConfig, LanceDBConfig
from llama_index.core.retrievers import VectorIndexRetriever

class LanceDB(BaseRAG):
    def __init__(self, embeding: BaseEmbed, config:ProviderConfig) -> None:
        super().__init__("LanceDB", embeding, config.chunk_size, config.overlapping)
        self.similarity_top_k = config.similarity_top_k
        self.config:LanceDBConfig = config.rag
        self.loc = self.config.loc
        self.path = f"DataBase/{self.loc}"

    async def append_index(self, nodes) -> Coroutine[Any, Any, str]:
        return None
    
    async def add_index(self, nodes) -> str:
        table_name = self.genrate_index_name()
        vector_store = LanceDBVectorStore(self.path,table_name=table_name)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        vector_index = VectorStoreIndex(nodes=nodes,storage_context=storage_context,embed_model=self.embeding_model)
        return table_name
    
    async def delete_index(self, index: str) -> bool:
        return await super().delete_index(index)
    
    async def get_docs_index(self, query:str ,index: str):
        vector_store = LanceDBVectorStore(uri=self.path,table_name=index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        vector_index = VectorStoreIndex(nodes=[],storage_context=storage_context)
        query_engine = VectorIndexRetriever(vector_index,similarity_top_k=self.similarity_top_k)
        # query_engine = vector_index.as_query_engine(llm=self.llm)
        return query_engine.retrieve(query)