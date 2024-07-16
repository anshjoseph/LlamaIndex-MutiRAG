from fastapi import FastAPI, UploadFile
from LlamaIndexRAG import RAGProviders, EmbedingProviders
from LlamaIndexRAG.DataModel import RAGConfig
import uvicorn
from concurrent.futures import ThreadPoolExecutor
import asyncio
from typing import Dict
DB:Dict[str:RAGConfig] = {}

"""
file -> nodes 

upadte (file 1 , file 2)

[]

END USER CASE:

- upload file
- create agent


user A -> he upload -> index

id -> append, upload

"""

