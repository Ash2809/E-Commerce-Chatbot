from langchain_astradb import AstraDBVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import pandas as pd
from bot.data_converter import data_converter

load_dotenv()

GOOGLE_API_KEY=os.getenv("OPENAI_API_KEY")
API_ENDPOINT=os.getenv("API_ENDPOINT")
ASTRA_API=os.getenv("ASTRA_API")
ASTRA_KEYSPACE=os.getenv("ASTRA_KEYSPACE")

gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


def ingest_data(status):
    vector_store = AstraDBVectorStore(embedding = gemini_embeddings,
                                      collection_name = "Ecom_Bot",
                                      api_endpoint = API_ENDPOINT,
                                      token = ASTRA_API,
                                      namespace = ASTRA_KEYSPACE)
    storage = status
    
    if storage == None:
        docs = data_converter()
        inserted_ids = vector_store.add_documents(docs)
    else:
        return vector_store
    return vector_store,inserted_ids

if __name__ == "__main__":
    vector_store,inserted_ids = ingest_data(None)
    print(f"inserted {len(inserted_ids)} documents.")
    results = vector_store.similarity_search("can you tell me the low budget sound basshead.")
    for res in results:
            print(f"* {res.page_content} [{res.metadata}]")

