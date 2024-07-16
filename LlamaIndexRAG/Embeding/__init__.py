from .OpenAI import OpenAI
from .Base import BaseEmbed
from typing import Dict
EmbedProviders:Dict[str,BaseEmbed] ={
    "OpenAI": OpenAI
}