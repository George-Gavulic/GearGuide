import time
from langchain_classic.embeddings import CacheBackedEmbeddings  
from langchain_classic.storage import LocalFileStore 
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_chroma import Chroma
from uuid import uuid4


# Create your underlying embeddings model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2", 
    encode_kwargs={"normalize_embeddings": True}
)

vector_store = Chroma(
    collection_name="2004_buick_lesabre",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)

# Store persists embeddings to the local filesystem
# This isn't for production use, but is useful for local
# store = LocalFileStore("./cache/")

# cached_embedder = CacheBackedEmbeddings.from_bytes_store(
#     underlying_embeddings,
#     store,
#     namespace=underlying_embeddings.model_name  # Fixed from .model to .model_name
# )

# Example: caching a query embedding
# tic = time.time()
# print(cached_embedder.embed_query("Hello, world!"))
# print(f"First call took: {time.time() - tic:.2f} seconds")

# # Subsequent calls use the cache
# tic = time.time()
# print(cached_embedder.embed_query("Hello, world!"))
# print(f"Second call took: {time.time() - tic:.2f} seconds")

def Embeddings(chunks):
    # chunks.metadata
    # chunks.pagecontent
    for i, chunk in enumerate(chunks):
        metadata = chunk.metadata
        content = chunk.page_content
        vecotor_data[i] = embeddings.embed_query(metadata + content)

    uuids = [str(uuid4()) for _ in range(len(vecotor_data))]
    vector_store.add_documents(documents=vecotor_data, ids=uuids)

