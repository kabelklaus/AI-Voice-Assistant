# vector_db_operations.py

from datetime import datetime
from langchain_astradb import AstraDBVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter

def initialize_astra_db(embeddings, token, api_endpoint):
    return AstraDBVectorStore(
        token=token,
        api_endpoint=api_endpoint,
        namespace="default_keyspace",
        collection_name="chatmemory",
        embedding=embeddings
    )

def save_user_info(astra_db, user_id, info_type, value):
    # Define ANSI escape codes
    ITALIC = "\033[3m"
    LIGHT_GRAY = "\033[1m"
    RESET = "\033[0m"
    
    existing_info = get_user_info(astra_db, user_id, info_type)
    if existing_info:
        # If information exists, update it instead of creating a new entry
        metadata = {
            "user_id": user_id,
            "info_type": info_type,
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        astra_db.update_texts([f"{info_type}: {value}"], [metadata], filter={"user_id": user_id, "info_type": info_type})
        action = "Updated"
    else:
        # If it's new information, save it as before
        metadata = {
            "user_id": user_id,
            "info_type": info_type,
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        astra_db.add_texts([f"{info_type}: {value}"], [metadata])
        action = "Saved"
    
    print(f"⚙️{ITALIC}{LIGHT_GRAY}  {action} user info: {info_type} = {value}{RESET}\n")
    return value

def get_user_info(astra_db, user_id, info_type):
    results = astra_db.similarity_search_with_score(
        f"user_id:{user_id} info_type:{info_type}",
        k=1,
        filter={"user_id": user_id, "info_type": info_type}
    )
    if results:
        return results[0][0].page_content.split(": ")[1]
    return None

def retrieve_from_vectordb(astra_db, query, k=5, time_window=None):
    filter_dict = {}
    
    if time_window:
        current_time = datetime.now().isoformat()
        filter_dict["timestamp"] = {"$gte": (datetime.now() - time_window).isoformat()}

    results = astra_db.similarity_search_with_score(query, k=k, filter=filter_dict)
    
    # Sortiere die Ergebnisse nach Timestamp (neueste zuerst)
    sorted_results = sorted(results, key=lambda x: x[0].metadata['timestamp'], reverse=True)
    
    return [{"content": doc.page_content, "metadata": doc.metadata, "score": score} for doc, score in sorted_results]

def add_to_vectordb(astra_db, text, sender, text_splitter):
    chunks = text_splitter.split_text(text)
    metadata = {
        "sender": sender,
        "timestamp": datetime.now().isoformat(),
        "sender_name": sender,
        "files": []
    }
    texts_with_metadata = [(chunk, metadata) for chunk in chunks]
    
    astra_db.add_texts([text for text, _ in texts_with_metadata], [metadata for _, metadata in texts_with_metadata])