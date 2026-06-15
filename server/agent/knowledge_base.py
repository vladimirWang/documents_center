from datetime import datetime
import copy
from langchain_text_splitters import RecursiveCharacterTextSplitter

import agent.config_data as config
from agent.pgvector_store import get_pgvector_store


class KnowledgeBase:
    def __init__(self):
        self.vector_store = get_pgvector_store()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_overlap=config.chunk_overlap,
            chunk_size=config.chunk_size,
            length_function=len,
            separators=config.separators,
        )

    def add_knowledge(self, content: str, file_id: int, operator: int):
        chunks = []
        if len(content) > config.chunk_overlap:
            chunks = self.splitter.split_text(content)
        else:
            chunks = [content]
        metadata = {
            "file_id": file_id,
            "operator": operator,
            "source": str(file_id),
        }
        self.vector_store.add_texts(chunks, metadatas=[copy.deepcopy(metadata) for _ in chunks])
        print(f"chunks: {chunks}, str: {str}, file_id: {file_id}, operator: {operator}")

    def delete_knowledge(self, knowledge: str):
        self.knowledge_base.remove(knowledge)

    def update_knowledge(self, knowledge: str):
        self.knowledge_base.append(knowledge)

    def get_knowledge(self):
        return self.knowledge_base
