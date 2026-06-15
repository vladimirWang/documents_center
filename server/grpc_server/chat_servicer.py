import grpc

from grpc_generated import chat_pb2, chat_pb2_grpc
from module_chat.chat_service import chat


class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    def Ask(self, request, context):
        question = request.question.strip()
        if not question:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("question 不能为空")
            return chat_pb2.ChatResponse(code=400, message="question 不能为空")

        try:
            answer = chat(question)
            return chat_pb2.ChatResponse(code=200, message="ok", answer=answer)
        except Exception as exc:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(exc))
            return chat_pb2.ChatResponse(code=500, message=str(exc))
