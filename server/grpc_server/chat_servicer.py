import grpc

from database.session import SessionLocal
from grpc_generated import chat_pb2, chat_pb2_grpc
from module_chat.chat_service import (
    chat_invoke,
    get_chat_session_detail,
    get_current_user_sessions,
    serialize_chat_session,
)


class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    def Ask(self, request, context):
        question = request.question.strip()
        if not question:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("question 不能为空")
            return chat_pb2.ChatResponse(code=400, message="question 不能为空")

        session_id = request.session_id.strip()
        if not session_id:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("session_id 不能为空")
            return chat_pb2.ChatResponse(code=400, message="session_id 不能为空")

        user_id = request.user_id
        if user_id <= 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("user_id 无效")
            return chat_pb2.ChatResponse(code=400, message="user_id 无效")

        try:
            answer = chat_invoke(question, session_id, user_id)
            return chat_pb2.ChatResponse(code=200, message="ok", answer=answer)
        except Exception as exc:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(exc))
            return chat_pb2.ChatResponse(code=500, message=str(exc))

    def GetCurrentUserSessions(self, request, context):
        user_id = request.user_id
        if user_id <= 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("user_id 无效")
            return chat_pb2.GetCurrentUserSessionsResponse(code=400, message="user_id 无效")

        db = SessionLocal()
        try:
            sessions = get_current_user_sessions(db, user_id)
            return chat_pb2.GetCurrentUserSessionsResponse(
                code=200,
                message="ok",
                sessions=[
                    chat_pb2.ChatSessionInfo(
                        id=item["id"],
                        user_id=item["user_id"],
                        created_at=item["created_at"],
                        updated_at=item["updated_at"],
                    )
                    for item in (serialize_chat_session(session) for session in sessions)
                ],
            )
        except Exception as exc:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(exc))
            return chat_pb2.GetCurrentUserSessionsResponse(code=500, message=str(exc))
        finally:
            db.close()

    def GetChatSessionById(self, request, context):
        session_id = request.session_id.strip()
        if not session_id:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("session_id 不能为空")
            return chat_pb2.GetChatSessionByIdResponse(code=400, message="session_id 不能为空")

        user_id = request.user_id
        if user_id <= 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("user_id 无效")
            return chat_pb2.GetChatSessionByIdResponse(code=400, message="user_id 无效")

        db = SessionLocal()
        try:
            detail = get_chat_session_detail(db, session_id, user_id)
            session = detail["session"]
            return chat_pb2.GetChatSessionByIdResponse(
                code=200,
                message="ok",
                session=chat_pb2.ChatSessionInfo(
                    id=session["id"],
                    user_id=session["user_id"],
                    created_at=session["created_at"],
                    updated_at=session["updated_at"],
                ),
                messages=[
                    chat_pb2.ChatMessageInfo(role=msg["role"], content=msg["content"])
                    for msg in detail["messages"]
                ],
            )
        except ValueError as exc:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(str(exc))
            return chat_pb2.GetChatSessionByIdResponse(code=404, message=str(exc))
        except Exception as exc:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(exc))
            return chat_pb2.GetChatSessionByIdResponse(code=500, message=str(exc))
        finally:
            db.close()
