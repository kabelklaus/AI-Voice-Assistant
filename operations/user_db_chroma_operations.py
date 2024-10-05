# user_db_chroma_operations.py

from datetime import datetime
from langchain_chroma import Chroma

def initialize_user_db(embeddings, persist_directory="./user_chroma_db"):
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name="user_info"
    )

def save_user_info(user_db, user_id, info_type, value):
    ITALIC = "\033[3m"
    LIGHT_GRAY = "\033[1m"
    RESET = "\033[0m"
    
    metadata = {
        "user_id": user_id,
        "info_type": info_type,
        "value": value,
        "timestamp": datetime.now().isoformat()
    }
    
    user_db.add_texts(
        texts=[f"{info_type}: {value}"],
        metadatas=[metadata],
        ids=[f"{user_id}_{info_type}"]
    )
    
    print(f"⚙️{ITALIC}{LIGHT_GRAY}  Updated user info: {info_type} = {value}{RESET}\n")
    return value

def get_user_info(user_db, user_id, info_type):
    where_clause = {
        "$and": [
            {"user_id": {"$eq": user_id}},
            {"info_type": {"$eq": info_type}}
        ]
    }
    
    results = user_db.get(where=where_clause)
    
    if results['documents']:
        return results['documents'][0].split(": ")[1] if results['documents'][0] else None
    return None

def retrieve_all_user_info(user_db, user_id):
    where_clause = {"user_id": {"$eq": user_id}}
    
    results = user_db.get(where=where_clause)
    
    user_info = {}
    if results['documents']:
        for doc, metadata in zip(results['documents'], results['metadatas']):
            info_type = metadata['info_type']
            value = doc.split(": ")[1]
            user_info[info_type] = value
    
    return user_info