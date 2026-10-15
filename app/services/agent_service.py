from agent import agent_runtime
from uuid import UUID
class AgentService:
    def agent_chat_request_service(self,request:str,conversation_id:UUID):
        resp=agent_runtime(input=request)
        return resp

agent_service=AgentService()