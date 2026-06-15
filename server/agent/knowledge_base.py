from datetime import datetime
import copy
from langchain_text_splitters import RecursiveCharacterTextSplitter

import agent.config_data as config
from agent.pgvector_store import get_pgvector_store, delete_by_logical_source


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
        deleted_count = delete_by_logical_source(self.vector_store, str(file_id))
        
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
        # print(f"chunks: {chunks}, str: {str}, file_id: {file_id}, operator: {operator}")
        return {
            "deleted_count": deleted_count, # 删除的向量数量
            "added_count": len(chunks), # 新增的向量数量
            "is_update": deleted_count > 0, # 是否更新
            "addleted_count": len(chunks) - deleted_count if deleted_count > 0 else 0, # 当对已向量化后的文件再次向量化时，新增的向量数量 - 删除的向量数量
        }

    def delete_knowledge(self, knowledge: str):
        self.knowledge_base.remove(knowledge)

    def update_knowledge(self, knowledge: str):
        self.knowledge_base.append(knowledge)

    def get_knowledge(self):
        return self.knowledge_base
