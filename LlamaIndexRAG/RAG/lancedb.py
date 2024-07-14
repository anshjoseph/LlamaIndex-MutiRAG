from typing import Any, Coroutine
from LlamaIndexRAG.Embeding.Base import BaseEmbed
from .Base import BaseProvider
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.core import VectorStoreIndex, StorageContext

class LanceDB(BaseProvider):
    def __init__(self, provider: str, embeding: BaseEmbed, chunk_size: int, overlapping: int, rag_name:str) -> None:
        super().__init__(provider, embeding, chunk_size, overlapping)
        self.rag_name = rag_name
        
    #Basic operation's
    async def append_index(self, index: str, file_path: str, mode: str) -> Coroutine[Any, Any, str]:
        return super().append_index(index, file_path)
    
    async def add_index(self, file_path: str, mode: str) -> str:
        table_name = self.genrate_table_name()
        # TODO: add reranking in the DB
        vector_store = LanceDBVectorStore(f"DataBase/{self.rag_name}",table_name=table_name)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        if mode is "ss-split":
            nodes = await self.genrate_nodes_sentence_splitter()
        elif mode is "tt-split":
            nodes = await self.genrate_nodes_text_splitter()
        else:
            raise f"mode sould be (ss-split or tt-split)"
        vector_index = VectorStoreIndex(nodes=nodes,storage_context=storage_context,embed_model=self.embeding_model)
        return table_name
    
    async def delete_index(self, index: str) -> bool:
        return await super().delete_index(index)