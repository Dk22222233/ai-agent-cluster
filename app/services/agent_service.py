from agent import agent_runtime
class AgentService:
    def agent_chat_request_service(self,request:str):
        resp=agent_runtime(input=request)
        return resp

agent_service=AgentService()