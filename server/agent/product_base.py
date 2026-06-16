from datetime import datetime
import copy
from langchain_text_splitters import RecursiveCharacterTextSplitter
import mimetypes
import agent.config_data as config
from agent.pgvector_store import get_pgvector_store, delete_by_logical_source
from langchain_community.document_loaders import PyPDFLoader
from utils.file import get_local_file, read_filepath_bytes_sync
from urllib.parse import urlparse
from database.models import Product

class ProductBase:
    def __init__(self):
        self.vector_store = get_pgvector_store(config.products_collection_name)

    def add_product(self, product: Product) -> str:
        if product.vectorized:
            return f"产品 {product.name} 已向量化"
        if not product.id:
            raise ValueError("产品id不能为空")
        embedding_txt = f"{product.name} {product.description}"
        self.vector_store.add_texts([embedding_txt], metadatas=[{
            "product_id": product.id,
            "product_name": product.name,
            "product_price": product.price,
        }])
        return f"产品 {product.name} 向量化成功"