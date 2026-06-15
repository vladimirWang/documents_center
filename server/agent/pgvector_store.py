from functools import lru_cache

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_postgres import PGVector
from sqlalchemy import select

import agent.config_data as config
from base_config.database import SYNC_SQLALCHEMY_DATABASE_URL


def get_embeddings() -> DashScopeEmbeddings:
    return DashScopeEmbeddings(model=config.embedding_model)


@lru_cache(maxsize=1)
def get_pgvector_store() -> PGVector:
    """获取 PGVector 向量库单例（与 ruoyi-fastapi 共用 PostgreSQL）。"""
    print("SYNC_SQLALCHEMY_DATABASE_URL: ", SYNC_SQLALCHEMY_DATABASE_URL)
    return PGVector(
        embeddings=get_embeddings(),
        collection_name=config.collection_name,
        connection=SYNC_SQLALCHEMY_DATABASE_URL,
        use_jsonb=True,
        embedding_length=config.embedding_length,
        create_extension=True,
    )
