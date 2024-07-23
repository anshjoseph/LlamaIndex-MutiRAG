from uuid import uuid4
from llama_parse import LlamaParse
from MultiRAG.Embeding import BaseEmbed
from MultiRAG.utils import configure_logger
from llama_index.core.node_parser import (
    MarkdownElementNodeParser,
    SentenceSplitter,
    TextSplitter
)
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
import dotenv
import os

dotenv.load_dotenv()


logger = configure_logger(__name__)

class BaseRAG:
    def __init__(self, provider:str, embeding:BaseEmbed, chunk_size:int, overlapping:int) -> None:
        self.provider = provider
        self.base_embed:BaseEmbed = embeding
        self.embeding_model = self.base_embed.get_embeding()
        self.chunk_size = chunk_size
        self.overlapping = overlapping
        self.LLAMA_CLOUD  = os.getenv("LLAMA_PARSE_KEY")
        if self.LLAMA_CLOUD is None:
            raise "LLAMA_PARSE_KEY is not exit in .env"
        self.parse = LlamaParse(
            api_key=self.LLAMA_CLOUD,
            result_type="markdown",
        )
        #TODO: make llm base class
        self.OPENAI_KEY = os.getenv("OPENAI_KEY")
        if self.OPENAI_KEY is None:
            raise "OPENAI_KEY is not exit in .env"
        self.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.2,api_key=self.OPENAI_KEY)

        Settings.embed_model = self.embeding_model
        Settings.llm = self.llm
    def genrate_index_name(self):
        return str(uuid4())
    
    async def genrate_nodes_sentence_splitter(self,file_loc:str):
        docs = await self.parse.aload_data(file_path=file_loc)
        node_parser = MarkdownElementNodeParser(num_workers=8,llm=self.llm)
        nodes = await node_parser.aget_nodes_from_documents(docs)
        nodes, objects = node_parser.get_nodes_and_objects(nodes)
        nodes = await SentenceSplitter(chunk_size=self.chunk_size, chunk_overlap=self.overlapping).aget_nodes_from_documents(
            nodes
        )
        return nodes
    async def genrate_nodes_text_splitter(self,file_loc:str):
        docs = await self.parse.aload_data(file_path=file_loc)
        node_parser = MarkdownElementNodeParser(num_workers=8,llm=self.llm)
        nodes = await node_parser.aget_nodes_from_documents(docs)
        nodes, objects = node_parser.get_nodes_and_objects(nodes)
        nodes = await TextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.overlapping).aget_nodes_from_documents(
            nodes
        )
        return nodes
    
    #TODO: make that in file lvl's
    async def append_index(self,nodes)->str:
        """
        index: index should be already present in the RAG
        mode: it take two modes (tt-split, ss-split) for diffrent node genration mech.
        """
        raise NotImplementedError
    async def add_index(self,nodes)->str:
        """
        index: index should be already present in the RAG
        mode: it take two modes (tt-split, ss-split) for diffrent node genration mech.
        """
        raise NotImplementedError
    async def delete_index(self,index:str)->bool:
        raise NotImplementedError
    async def get_docs_index(self,query:str ,index: str):
        raise NotImplementedError
    
    
    