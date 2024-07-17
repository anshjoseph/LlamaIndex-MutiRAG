from LlamaIndexRAG.Embeding import EmbedProviders
from LlamaIndexRAG.RAG import RAGProviders
from .RAG import BaseProvider as RAGBase
from .DataModel import RAGConfig, RAGTask, RAGTaskStatus
import asyncio
from threading import Thread
from .Utils import configure_logger
from typing import Dict
from uuid import uuid4
import tempfile
import os

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
        embeding = EmbedProviders[config.provider_config.embeding.provider](config.provider_config.embeding.model_name)
        vector_db = RAGProviders[config.provider](embeding,config.provider_config)
        rag = RAG(vector_db)
        rag.RAG_THREAD.start()
        self.RAGS[rag_name] = rag
        return rag_name
    def stop_all(self):
        for rag in self.RAGS.values():
            rag.shutdown = True
    def stop(self,rag_name:str):
        if rag_name in self.RAGS.keys():
            self.RAGS[rag_name].shutdown = True
            self.RAGS.pop(rag_name)
        else:
            raise "NO RAG WITH THAT ID EXIST's"
    
    async def file_ingest(self,rag_name,file)->RAGTask:
        if rag_name not in self.RAGS.keys():
            raise f"rag: {rag_name} not exit"
        if file.content_type not in ["application/pdf","application/x-pdf"]:
            raise f"only support pdf for now"
        task_id = str(uuid4())
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(await file.read())
        prev = temp_file.name
        file_name = f"/tmp/{task_id}.pdf"
        os.rename(prev,file_name)
        task = RAGTask(file_loc=file_name)
        await self.RAGS[rag_name].file_process_task_queue.put(task)
        while task._status in [RAGTaskStatus.WAIT,RAGTaskStatus.PROCESSING]:
            await asyncio.sleep(0.4)
        os.rename(file_name,prev)
        return task
    async def retrive_query(self,rag_name:str,index:str,query:str):
        # TODO: makes checks
        rag = self.RAGS[rag_name]
        return await rag.VectorDB.get_docs_index(query=query,index=index)
        
        
