import json
import chromadb
from chromadb.utils import embedding_functions

# Using Sentence Transformers (all-MiniLM-L6-v2 is downloaded automatically by chromadb if not specified, 
# but defining it ensures consistent local behavior)
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path="./.chroma")
collection = chroma_client.get_or_create_collection(name="resource_demands", embedding_function=embed_fn)

def init_db():
    if collection.count() == 0:
        with open("industries.json", "r") as f:
            industries = json.load(f)
        
        consumers = [i for i in industries if i.get("role") == "consumer"]
        
        docs = [c["demand"] for c in consumers]
        ids = [c["id"] for c in consumers]
        metadatas = [{"name": c["name"], "lat": c["lat"], "lon": c["lon"], "demand": c["demand"]} for c in consumers]
        
        collection.add(
            documents=docs,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Loaded {len(consumers)} consumer demands into ChromaDB.")
    else:
        print(f"ChromaDB ready ready with {collection.count()} items.")

def search_demands(query_text: str, k: int = 5):
    return collection.query(
        query_texts=[query_text],
        n_results=k
    )
