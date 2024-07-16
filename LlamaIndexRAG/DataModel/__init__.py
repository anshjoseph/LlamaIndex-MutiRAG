from pydantic import BaseModel, Field, validator, ValidationError
from typing import Union, Optional
# from LlamaIndexRAG.Embeding import EmbedProviders
# from LlamaIndexRAG.RAG import RAGProviders

class LanceDB(BaseModel):
    loc:str

def validate_attribute(value, allowed_values):
    if value not in allowed_values:
        raise ValidationError(f"Invalid provider {value}. Supported values: {allowed_values}")
    return value

class ProviderConfig(BaseModel):
    embeding:str
    chunk_size:int
    overlapping:int
    loc:Optional[str] = ""
    @validator("embeding")
    def embeding_eval(cls, value):
        return validate_attribute(value, ["openai"])

class RAGConfig(BaseModel):
    provider:str
    provider_config:ProviderConfig
    @validator("provider")
    def provider_eval(cls, value):
        return validate_attribute(value, ["lacebd"])
    
class Query(BaseModel):
    provider:str
    index:str
    query:str
    @validator("provider")
    def provider_eval(cls, value):
        return validate_attribute(value, list(RAGProviders.keys()))

class RAGTaskStatus:
    WAIT = "WAIT"
    PROCESSING = "PROCESSING"
    ERROR = "ERROR"
    SUCESSFUL = "SUCESSFUL"

class RAGTask(BaseModel):
    file_loc:str
    _status:str
    _message:str
    _index:str
    _nodes:list
