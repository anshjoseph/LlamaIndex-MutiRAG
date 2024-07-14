from .OpenAI import OpenAI
from .Base import BaseEmbed
from typing import Dict
Providers:Dict[str,BaseEmbed] ={
    "OpenAI_Embeding": OpenAI
}