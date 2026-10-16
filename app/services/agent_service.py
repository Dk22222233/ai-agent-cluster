from agent import agent_runtime
from uuid import UUID
from app.repositories import conversation_repo, message_repo
from app.api.schemas import AgentChatRequest, AgentChatResponse, MessageResponse
class AgentService:

    def agent_chat_request_service(self,request:AgentChatRequest,user_id:UUID)->AgentChatResponse:

        #-----if no chat create one-----
        if request.conversation_id is None:
            conv_orm=conversation_repo.create_for_user(user_id=user_id,title=request.message[:60].strip())
        else:
            #---this also enforce ownership
            conv_orm=conversation_repo.get_chat_by_id_for_user(request.conversation_id,user_id)
            if conv_orm is None:
                raise ValueError("Conversation not found")

        #--save user message, 
        message_repo.create_msg(
            conversation_id=conv_orm.id,
            role='user',
            content=request.message # request message is str
        )

        history_orm=message_repo.get_latest(conversation_id=conv_orm.id,n=60)
        #---convert to context for agent

        history=[
            MessageResponse.model_validate(m) for m in history_orm
        ]

        # agent calling
        reply_text=agent_runtime(input=request.message,)

        assistant_orm=message_repo.create_msg(
            conversation_id=conv_orm.id,
            role='assistant',
            content=reply_text
        )
        return AgentChatResponse(
            conversation_id=conv_orm.id,
            response=MessageResponse(
                id=assistant_orm.id,
                role='assistant',
                content= assistant_orm.content or ''
            )
        )

agent_service=AgentService()