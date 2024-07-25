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

def save_user_info(vector_db, user_id, info_type, value):
    # Define ANSI escape codes
    ITALIC = "\033[3m"
    LIGHT_GRAY = "\033[1m"
    RESET = "\033[0m"
    
    metadata = {
        "user_id": user_id,
        "info_type": info_type,
        "value": value,
        "timestamp": datetime.now().isoformat()
    }
    
    # Chroma unterstützt Upsert, also können wir einfach hinzufügen/aktualisieren
    vector_db.add_texts(
        texts=[f"{info_type}: {value}"],
        metadatas=[metadata],
        ids=[f"{user_id}_{info_type}"]
    )
    
    print(f"⚙️{ITALIC}{LIGHT_GRAY}  Updated user info: {info_type} = {value}{RESET}\n")
    return value

def get_user_info(vector_db, user_id, info_type):
    where_clause = {
        "$and": [
            {"user_id": {"$eq": user_id}},
            {"info_type": {"$eq": info_type}}
        ]
    }
    
    results = vector_db.get(where=where_clause)
    
    if results['documents']:
        # Nehmen wir an, dass wir nur ein Ergebnis erwarten
        return results['documents'][0].split(": ")[1] if results['documents'][0] else None
    return None

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