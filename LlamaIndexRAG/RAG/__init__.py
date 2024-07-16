from .lancedb import LanceDB
from .Base import BaseProvider
from typing import Dict

RAGProviders:Dict[str,BaseProvider]={
    "LanceDB":LanceDB
}