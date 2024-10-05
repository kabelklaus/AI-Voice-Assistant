# vector_db_chroma_operations.py

from datetime import datetime
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

def initialize_vector_db(embeddings, persist_directory="./chroma_db"):
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name="chatmemory"
    )

def retrieve_from_vectordb(vector_db, query, k=5, time_window=None):
    filter_dict = {}
    
    if time_window:
        current_time = datetime.now().isoformat()
        filter_dict["timestamp"] = {"$gte": (datetime.now() - time_window).isoformat()}

    results = vector_db.similarity_search_with_score(query, k=k, filter=filter_dict)
    
    return [{"content": doc.page_content, "metadata": doc.metadata, "score": score} for doc, score in results]

def add_to_vectordb(vector_db, text, sender, text_splitter, files=None):
    chunks = text_splitter.split_text(text)
    metadata = {
        "sender": sender,
        "timestamp": datetime.now().isoformat(),
        "sender_name": sender
    }
    if files:
        metadata["files"] = ",".join(files)  # Konvertiert die Liste in einen String
    
    vector_db.add_texts(
        texts=chunks,
        metadatas=[metadata for _ in chunks],
        ids=[f"{sender}_{datetime.now().timestamp()}_{i}" for i in range(len(chunks))]
    )