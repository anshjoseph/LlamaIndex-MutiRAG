from pydantic import BaseModel, Field, validator, ValidationError
from typing import Union, Optional
# from LlamaIndexRAG.Embeding import EmbedProviders
# from LlamaIndexRAG.RAG import RAGProviders

RAGProviders = ["LanceDB"]
EmbedProviders = ["OpenAI"]



def validate_attribute(value, allowed_values):
    if value not in allowed_values:
        raise ValidationError(f"Invalid provider {value}. Supported values: {allowed_values}")
    return value
class Embeding(BaseModel):
    provider:str
    model_name:Optional[str] = ""
class ProviderConfig(BaseModel):
    embeding:Embeding
    chunk_size:int
    overlapping:int
    loc:Optional[str] = ""
    # @validator("embeding")
    # def embeding_eval(cls, value):
    #     return validate_attribute(value, EmbedProviders)

class RAGConfig(BaseModel):
    provider:str
    provider_config:ProviderConfig
    # @validator("provider")
    # def provider_eval(cls, value):
    #     return validate_attribute(value, RAGProviders)
    

class Query(BaseModel):
    provider:str
    index:str
    query:str
    # @validator("provider")
    # def provider_eval(cls, value):
    #     return validate_attribute(value, RAGProviders)

class RAGTaskStatus:
    WAIT = "WAIT"
    PROCESSING = "PROCESSING"
    ERROR = "ERROR"
    SUCESSFUL = "SUCESSFUL"

class RAGTask(BaseModel):
    file_loc:str
    _status:str = RAGTaskStatus.WAIT
    _message:str = ""
    _index:str = ""
    _nodes:list = []
