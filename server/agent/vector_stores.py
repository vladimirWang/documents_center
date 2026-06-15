import agent.config_data as config
from agent.pgvector_store import get_pgvector_store


class VectorStore(object):
    def __init__(self):
        self.vector_store = get_pgvector_store()

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={'k': config.search_kwargs})
