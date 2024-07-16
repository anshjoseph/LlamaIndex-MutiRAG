from typing import Any, Coroutine
from LlamaIndexRAG.Embeding.Base import BaseEmbed
from .Base import BaseProvider
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from LlamaIndexRAG.DataModel import ProviderConfig

class LanceDB(BaseProvider):
    def __init__(self, embeding: BaseEmbed, config:ProviderConfig) -> None:
        super().__init__(config.provider, embeding, config.chunk_size, config.overlapping)
        self.loc = config.loc
        self.config = config
        self.path = f"DataBase/{self.loc}"

        
    #Basic operation's
    async def append_index(self, nodes) -> Coroutine[Any, Any, str]:
        return None
    
    async def add_index(self, nodes) -> str:
        table_name = self.genrate_table_name()
        # TODO: add reranking in the DB
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
        query_engine = vector_index.as_query_engine()
        return query_engine.retrieve(query)