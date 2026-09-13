import pandas as pd
import os
from config import settings

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

VECTOR_DB_DIR = settings.vector_db_dir
KNOWLEDGE_FILE = settings.knowledge_file

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_CACHE = "/models"

def get_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name = EMBEDDING_MODEL,
        cache_folder = EMBEDDING_CACHE
    )
    return embeddings

def load_product_documents():
    df = pd.read_csv(KNOWLEDGE_FILE)
    documents = []
    for _, row in df.iterrows():
        content = f"""Product Name: {row['product_name']}\n Description: {row['description']} \n Ideal For: {row['ideal_for']} \n Pros: {row['pros']} \n Cons: {row['cons']}"""
        documents.append(Document(page_content=content, metadata={"product_id": row["product_id"], "product_name": row["product_name"]}))
    return documents

def create_vector_store():
    documents = load_product_documents()
    embeddings = get_embeddings()

    vector_store = Chroma.from_documents(
        documents = documents,
        embedding = embeddings,
        persist_directory = VECTOR_DB_DIR
    )

    return vector_store

def load_vector_store():
    embeddings = get_embeddings()

    vector_store = Chroma(
        persist_directory = VECTOR_DB_DIR,
        embedding_function = embeddings
    )

    return vector_store

def retrieve_product_information(query,k=3):
    vector_store = load_vector_store()
    documents = vector_store.similarity_search(query,k=k)

    return documents

def retrieve_product_by_id(product_id):
    vector_store = load_vector_store()
    documents = vector_store.similarity_search(
        query="product information",
        k=1,
        filter = {
            "product_id": product_id
        }
    )
    if not documents:
        return None

    return documents[0]