from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# client = chromadb.PersistentClient(path="./chroma_langchain_db")

# vector_store_from_client = Chroma(
#     client=client,
#     collection_name="collection_name",
#     embedding_function=embeddings,
# )

# client is used to get easy access to DB

# collection = client.get_or_create_collection("collection_name")
# collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])

print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2", 
    encode_kwargs={"normalize_embeddings": True}
)

vector_store = Chroma(
    collection_name="2004_buick_lesabre",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)

query = "What is the recommended tire pressure?"
print(f"\nSearching for: '{query}'\n")

results = vector_store.similarity_search_with_score(query, k=3)

# results = vector_store.similarity_search_with_score(
#     "Should I wear a seat belt?", k=1, filter={"source": "news"}
# )
# for res, score in results:
#     print(f"* [SIM={score:3f}] {res.page_content} [{res.metadata}]")

for res, score in results:
    print(f"--- [SIM_SCORE: {score:.4f}] ---")
    print(f"Page: {res.metadata.get('page_number')} | Heading: {res.metadata.get('heading')}")
    print(f"Content: {res.page_content[:300]}...\n") # Print first 300 chars of content



# Chroma(
#   self,
#   collection_name: str = _LANGCHAIN_DEFAULT_COLLECTION_NAME,
#   embedding_function: Embeddings | None = None,
#   persist_directory: str | None = None,
#   host: str | None = None,
#   port: int | None = None,
#   headers: dict[str, str] | None = None,
#   chroma_cloud_api_key: str | None = None,
#   tenant: str | None = None,
#   database: str | None = None,
#   client_settings: chromadb.config.Settings | None = None,
#   collection_metadata: dict | None = None,
#   collection_configuration: CreateCollectionConfiguration | None = None,
#   client: chromadb.ClientAPI | None = None,
#   relevance_score_fn: Callable[[float], float] | None = None,
#   create_collection_if_not_exists: bool | None = True,
#   *,
#   ssl: bool = False
# )