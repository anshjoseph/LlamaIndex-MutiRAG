from .Embeding import Providers as EmbedingProviders
from .RAG import Providers as RAGProviders
from .Embeding import BaseEmbed as EmbedingBase
from .RAG import BaseProvider as RAGBase
from .DataModel import RAGConfig, RAGTask, RAGTaskStatus
import asyncio
from threading import Thread
from .Utils import configure_logger
from typing import Dict
from uuid import uuid4

logger = configure_logger(__name__)
class RAG:
    def __init__(self,VectorDB:RAGBase,PipeLineTASK:int=2) -> None:
        self.file_process_task_queue:asyncio.Queue = asyncio.Queue()
        self.file_store_task_queue:asyncio.Queue = asyncio.Queue()
        
        self.VectorDB:RAGBase = VectorDB
        self.PipeLineTASK:int = PipeLineTASK

        self.RAG_THREAD = Thread(target=self.start)
        self.shutdown = False
    async def __shutdown_loop(self):
        while not self.shutdown:
            await asyncio.sleep(0.5)
    async def __ingestion_task(self):
        while not self.shutdown:
            task:RAGTask =  await self.file_process_task_queue.get()
            task._status = RAGTaskStatus.PROCESSING
            try:
                nodes = await self.VectorDB.genrate_nodes_sentence_splitter(task.file_loc)
            except Exception as e:
                logger.error(f"ERROR in {e}")
                task._status = RAGTaskStatus.ERROR
                continue
            task._nodes = nodes
            await self.file_store_task_queue.put(task)
    async def __nodes_storage(self):
        while not self.shutdown:
            task:RAGTask = await self.file_store_task_queue.get()
            try:
                index =  await self.VectorDB.add_index(task._nodes)
            except Exception as e:
                logger.error(f"ERROR in {e}")
                task._status = RAGTaskStatus.ERROR
                continue
            task._index = index
            task._status = RAGTaskStatus.SUCESSFUL


                
    def start(self):
        loop = asyncio.new_event_loop()
        ingestion_task_pool = [loop.create_task(self.__ingestion_task()) for _ in range(self.PipeLineTASK)]
        file_storage = loop.create_task(self.__nodes_storage())
        loop.run_until_complete(self.__shutdown_loop())
        file_storage.cancel()
        for t in ingestion_task_pool:
            t.cancel()
        loop.close()
        
    


class RAGFactory:
    def __init__(self) -> None:
        self.RAGS:Dict[str,RAG] = dict()
    def make_rag(self,config:RAGConfig):
        rag_name = f"index-{uuid4()}"
        embeding = EmbedingProviders[config.provider_config.embeding]
        vector_db = RAGProviders[config.provider](embeding,config.provider_config)
        rag = RAG(vector_db)
        rag.start()
        self.RAGS[rag_name] = rag
        return rag_name
    def stop_all(self):
        for rag in self.RAGS.values():
            rag.shutdown = True
    def stop(self,rag_name:str):
        if rag_name in self.RAGS.keys():
            self.RAGS[rag_name].shutdown = True
            del self.RAGS.pop(rag_name)
        else:
            raise "NO RAG WITH THAT ID EXIST's"
    
