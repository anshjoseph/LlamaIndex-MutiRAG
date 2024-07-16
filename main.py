from fastapi import FastAPI, UploadFile, Depends
from LlamaIndexRAG.DataModel import RAGConfig, RAGTask, RAGTaskStatus
from LlamaIndexRAG import RAGFactory, RAG
import uvicorn
import asyncio
import time
from typing import Dict
import dotenv

dotenv.load_dotenv()
DB:Dict[str,RAGConfig] = {}

rag_factory = RAGFactory()
app = FastAPI()


@app.get("/")
def heartbeat():
    return time.time()
@app.post("/create-rag")
def create_rag(request:RAGConfig):
    print(request)
    rag_id = rag_factory.make_rag(request)
    # rag_id = "hello"
    return {"rag_id":rag_id}
@app.post("/rag-upload-file/{rag_id}")
async def rag_upload_file(file:UploadFile,rag_id:str):
    try:
        task = await rag_factory.file_ingest(rag_name=rag_id,file=file)
        return  {"index":task._index,"status":task._status,"message":"DONE"}
    except Exception as e:
        return {"index":None,"status":"ERROR","message":f"{e}"}
@app.get("/rag-retrive/{rag_id}/{index}")
async def rag_retrive(query:str,rag_id:str,index:str):
    ...
if __name__ == "__main__":
    uvicorn.run("main:app",port=8000,host="0.0.0.0",reload=True)

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

