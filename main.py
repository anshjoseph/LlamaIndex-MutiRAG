from fastapi import FastAPI, UploadFile
from MultiRAG.DataModel import RAGConfig
from MultiRAG import RAGFactory
import uvicorn
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
    docs = await rag_factory.retrive_query(rag_name=rag_id,index=index,query=query)
    send_filter = [{"text":node.text,"score":node.score} for node in docs]
    return send_filter
    
if __name__ == "__main__":
    uvicorn.run("main:app",port=8000,host="0.0.0.0",reload=True)
