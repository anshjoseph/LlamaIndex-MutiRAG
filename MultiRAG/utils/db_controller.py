import redis
import dotenv
import os

dotenv.load_dotenv()
class DB_controller:
    def __init__(self) -> None:
        try:
            self.pool = redis.ConnectionPool.from_url(os.getenv("REDIS"))
            self.redis_client = redis.Redis.from_pool(self.pool)
        except:
            raise "can't able to connect to redis"
        self.rag_list:list = self.redis_client.get("rags-list")
        
    async def add_rag(self,rag_id:str,config:str):
        """
        rag_id: contain the rags, our system connect to
        config: it's json of config which it is using
        """
        await self.redis_client.set(rag_id,config)
        self.rag_list.append(rag_id)