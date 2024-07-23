from pydantic import BaseModel
from typing import Union, Optional


class Embeding(BaseModel):
    provider:str
    model_name:Optional[str] = ""


class LanceDBConfig(BaseModel):
    loc: Optional[str] = ""

class MongoDBConfig(BaseModel):
    uri: Optional[str] = ""
    db: Optional[str] = ""
    collection_name: Optional[str] = ""


class ProviderConfig(BaseModel):
    embeding:Embeding
    chunk_size:int
    overlapping:int
    worker:int
    similarity_top_k:int
    rag: Union[LanceDBConfig,MongoDBConfig]


class RAGConfig(BaseModel):
    provider:str
    provider_config:ProviderConfig
    
    

class Query(BaseModel):
    provider:str
    index:str
    query:str


class RAGTaskStatus:
    WAIT = "WAITING"
    PROCESSING = "PROCESSING"
    ERROR = "ERROR"
    SUCESSFUL = "SUCESSFUL"

class RAGTask(BaseModel):
    file_loc:str
    _status:str = RAGTaskStatus.WAIT
    _message:str = ""
    _index:str = ""
    _nodes:list = []
