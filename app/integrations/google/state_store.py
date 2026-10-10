from app.infrastructure.redis.client import redis_client
import secrets
import json
from uuid import UUID
from datetime import datetime, timezone
class OAuthStateStore:
    KEY_PREFIX ='oauth:state:'
    def __init__(self,redis_client):
        self.redis_client=redis_client
    #------this 
    def _key(self,state:str)->str:
        return f'{self.KEY_PREFIX}{state}'


    def save(self,state:str,user_id:UUID,code_verifier:str,expires_at:datetime)->None:
        ttl=int((expires_at-datetime.now(timezone.utc)).total_seconds())
        if ttl<=0:
            raise ValueError('expires_at must be in future')
        # json serilization....python objects turned into json serilized data
        payload=json.dumps({
            'user_id':str(user_id), # UUID-> str cuz json store str not UUID
            'code_verifier':code_verifier
        })
        #-----state become the redis key, value is json serilize data, expiry time=computed ttl
        self.redis_client.set(self._key(state),payload,ex=ttl)
    #---get the state  value and delete in the same shot
    def consume(self, state:str)-> dict|None:
        raw=self.redis_client.getdel(self._key(state))
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except (ValueError,TypeError):
            return None
state_store=OAuthStateStore(redis_client)