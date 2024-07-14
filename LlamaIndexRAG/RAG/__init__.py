from .lancedb import LanceDB
from .Base import BaseProvider
from typing import Dict

Providers:Dict[str:BaseProvider]={
    "LanceDB":LanceDB
}