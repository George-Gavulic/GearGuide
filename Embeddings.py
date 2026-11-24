import time
from langchain_classic.embeddings import CacheBackedEmbeddings  
from langchain_classic.storage import LocalFileStore 
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

# Create your underlying embeddings model
underlying_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2", encode_kwargs={"normalize_embeddings": True})

# Store persists embeddings to the local filesystem
# This isn't for production use, but is useful for local
store = LocalFileStore("./cache/")

cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings,
    store,
    namespace=underlying_embeddings.model_name  # Fixed from .model to .model_name
)

# Example: caching a query embedding
tic = time.time()
print(cached_embedder.embed_query("Hello, world!"))
print(f"First call took: {time.time() - tic:.2f} seconds")

# Subsequent calls use the cache
tic = time.time()
print(cached_embedder.embed_query("Hello, world!"))
print(f"Second call took: {time.time() - tic:.2f} seconds")