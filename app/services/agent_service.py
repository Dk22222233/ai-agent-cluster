from agent import agent_runtime, AgentResult, ExecutionContext
from uuid import UUID
from sqlalchemy.orm import Session
from app.adapters.agent_history_context import _orm_to_agent_dto, _message_dto_to_orm
from app.repositories import conversation_repo, message_repo
from app.api.schemas import AgentChatRequest, AgentChatResponse, MessageResponse
class AgentService:

    def agent_chat_request_service(self,request:AgentChatRequest,user_id:UUID,db:Session)->AgentChatResponse:
        #-----if no chat create one-----
        if request.conversation_id is None:
            conv_orm=conversation_repo.create_for_user(user_id=user_id,title=request.message[:60].strip(),db=db)
        else:
            #---this also enforce ownership
            conv_orm=conversation_repo.get_chat_by_id_for_user(request.conversation_id,user_id,db)
            if conv_orm is None:
                raise ValueError("Conversation not found")

        #--save user message, 
        message_repo.create_msg(
            conversation_id=conv_orm.id,
            role='user',
            # status=',', # only do work when there is something wrong
            content=request.message,# request message is str
            tool_calls=None,
            tool_call_id=None,
            db=db  
            
        )

        history_orm=message_repo.get_latest(conversation_id=conv_orm.id,n=60,db=db)
        #---convert to context for agent

        history=_orm_to_agent_dto(history_orm)
        ctx:ExecutionContext=ExecutionContext(
            user_id=user_id,
            db=db
        )
        # agent calling
        result:AgentResult=agent_runtime(input=request.message,history=history,ctx=ctx)
        #------orm is none at first
        assistant_orm=None
        # iteration of new_message and pick Message objects
        for msg in result.new_messages:

            row=message_repo.create_msg(
                conversation_id=conv_orm.id,
                
                status=(
                    'completed' if result.finish_reason in ('stop',None)
                    else 'failed'
                ),
                **_message_dto_to_orm(msg),
                db=db
            )
            if msg is result.message:
                assistant_orm=row

        return AgentChatResponse(
            conversation_id=conv_orm.id,
            response=MessageResponse(
                id=assistant_orm.id,
                role='assistant',
                content= assistant_orm.content ,
                )
        )

agent_service=AgentService()