from .openai_emded import OpenAI
from .base import BaseEmbed
from typing import Dict
EmbedProviders:Dict[str,BaseEmbed] ={
    "OpenAI": OpenAI
}