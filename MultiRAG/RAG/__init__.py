from .lancedb_rag import LanceDB
from .mongoDB_rag import MongoDB
from .base import BaseRAG
from typing import Dict

RAGProviders:Dict[str,BaseRAG]={
    "LanceDB":LanceDB,
    "MongoDB": MongoDB
}