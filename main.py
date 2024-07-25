# main.py

import os
import uuid
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage
import threading
import sys
from datetime import datetime


# Importiere die Funktionen
from operations.vector_db_astra_operations import *

# Sprache
from skills.t2s_elevenlabs_skill import spreche_text
# from skills.t2s_gtts_skill import spreche_text

# Skills
from skills.clock_skill import get_current_time
from skills.date_skill import *
from skills.s2t_skill import continuous_audio_input

# Innerer Monolog
from skills.inner_monologue_skill import InnerMonologueAgent

# prompts
from operations.response_prompt import RESPONSE_PROMPT

# Load environment variables
load_dotenv()

# Initialize Groq LLM llama-3.1-70b-versatile
# llm = ChatGroq(
#     api_key=os.getenv("GROQ_API_KEY"),
#     temperature=0.3,
#     max_tokens=1024,
#     model_name="llama-3.1-70b-versatile"
# )

# Initialize Groq LLM llama3-70b-8192
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
    max_tokens=1024,
    model_name="llama3-70b-8192"
)

# # Initialize Ollama
# llm = ChatOllama(
#     model="llama3.1",
#     temperature=0.3
# )

# Initialize Ollama embeddings
embeddings = OllamaEmbeddings(
    base_url="http://localhost:11434",
    model="nomic-embed-text:latest"
)

# Initialize AstraDB
vector_db = initialize_vector_db(
    embeddings,
    os.getenv("vector_db_APPLICATION_TOKEN"),
    os.getenv("vector_db_API_ENDPOINT")
)

# Initialize text splitter 
# !nicht einfach ändern, da es Auswirkungen auf das Retrieval von Informationen aus der Datenbank hat.!
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
) # Für einen AI Voice Assistant mit Fokus auf präzise Suchergebnisse und typischerweise kürzeren Antworten ist Ihr Ansatz, kleinere Chunks zu verwenden, sehr sinnvoll.

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=200
# ) # default

# Initialize memory
memory = ConversationBufferMemory(return_messages=True)

# Initialize inner monologue agent
inner_monologue_agent = InnerMonologueAgent(llm)

def generate_user_id():
    return str(uuid.uuid4())

# Generate a session ID and user ID
# session_id = str(uuid.uuid4())
user_id = generate_user_id()

# Initialize function calls dictionary
function_calls = {
    "get_current_time": get_current_time,
    "get_current_date": get_current_date,
    "get_current_week": get_current_week,
    "get_current_day": get_current_day,
    "save_user_info": lambda *args: save_user_info(vector_db, *args),
    "get_user_info": lambda *args: get_user_info(vector_db, *args),
}

def add_message_with_timestamp(memory, message_type, content):
    if message_type == "human":
        message = HumanMessage(content=content)
    else:
        message = AIMessage(content=content)
    
    # Fügen Sie den Timestamp als zusätzliches Attribut hinzu
    message.timestamp = datetime.now().isoformat()
    
    memory.chat_memory.add_message(message)

def chat(user_input):
    # Define ANSI escape codes
    ITALIC = "\033[3m"
    LIGHT_GRAY = "\033[1m"
    RESET = "\033[0m"

    # Retrieve conversation history from memory
    conversation_history = memory.chat_memory.messages

    # Retrieve relevant past information
    past_info = retrieve_from_vectordb(vector_db, user_input)
    
    # Format past information and conversation history
    context = "Conversation history:\n"
    for message in conversation_history[-10:]:  # Include last 5 messages for context
        timestamp = getattr(message, 'timestamp', 'N/A')  # Use 'N/A' if timestamp is not available
        context += f"{message.type} ({timestamp}): {message.content}\n"
    
    context += "\nPast context (sorted by relevance and recency):\n"
    for info in past_info:
        sender = info['metadata'].get('sender', info['metadata'].get('info_type', 'Unbekannt'))
        timestamp = info['metadata'].get('timestamp', 'Kein Zeitstempel')
        content = info['content'] if 'content' in info else f"{info['metadata'].get('info_type', 'Info')}: {info['metadata'].get('value', 'Unbekannt')}"
        context += f"{sender} ({timestamp}): {content} (Relevance: {info['score']:.2f})\n"
        
    # Generate inner monologue
    monologue = inner_monologue_agent.generate_inner_monologue(user_input, context)
    print(f"\n💭{ITALIC}{LIGHT_GRAY} Inner Monologue: {monologue}{RESET}\n")

    # Plan actions based on inner monologue
    actions = inner_monologue_agent.plan_actions(monologue)
    print(f"📋{ITALIC}{LIGHT_GRAY} Planned Actions:{RESET}")
    for i, action in enumerate(actions, 1):
        print(f"{ITALIC}{LIGHT_GRAY}  {i}. {action}{RESET}")
    print()

    # Generate response based on planned actions and context
    response_prompt = f"""{RESPONSE_PROMPT}

    Context: {context}
    User input: {user_input}
    Inner monologue: {monologue}
    Planned actions:
    {' '.join(actions)}

    Your response in German:
    """

    response = llm([HumanMessage(content=response_prompt)])

    # Check and execute function calls
    function_results = {}
    while "FUNCTION_CALL:" in response.content:
        for func_name, func in function_calls.items():
            func_call = f"FUNCTION_CALL: {func_name}"
            if func_call in response.content:
                print(f"\n⚙️{ITALIC}{LIGHT_GRAY}  {func_name}{RESET}\n")
                start = response.content.index(func_call) + len(func_call)
                end = response.content.find(")", start)
                if end == -1:  # If closing parenthesis is not found
                    end = len(response.content)
                args = response.content[start:end].strip("(").split(",")
                args = [arg.strip() for arg in args if arg.strip()]  # Remove empty arguments
                if args:
                    result = func(*args)
                else:
                    result = func()  # Call function without arguments if none provided
                function_results[func_name] = result
                # Remove the function call from the response content
                response.content = response.content[:response.content.index(func_call)] + response.content[end+1:]


    # If functions were called, generate a new response incorporating the results
    if function_results:
        function_info = "\n".join([f"{func}: {result}" for func, result in function_results.items()])
        new_prompt = f"""
        Previous response: {response.content}
        Function call results: {function_info}
        Inner monologue: {monologue}
        Planned actions: {', '.join(actions)}
        Based on these function results, the inner monologue, and the planned actions,
        please provide a natural and context-aware response to the user in German.
        Incorporate the information from the function calls, inner monologue, and planned actions naturally into your response.
        """
        new_message = HumanMessage(content=new_prompt)
        response = llm([new_message])

    add_message_with_timestamp(memory, "human", user_input)
    add_message_with_timestamp(memory, "ai", response.content)
    return response.content

def get_user_input(input_method):
    if input_method == 's':
        return continuous_audio_input()
    else:
        return input("You: ")

def get_input_with_timeout(prompt, timeout):
    print(prompt, end='', flush=True)
    result = [None]
    def get_input():
        result[0] = sys.stdin.readline().strip().lower()
    thread = threading.Thread(target=get_input)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        print("\nZeitüberschreitung. Standardmethode wird gewählt.")
        return None
    return result[0]

input_method = get_input_with_timeout("Möchten Sie sprechen (s) oder tippen (t)? Sie haben 5 Sekunden Zeit zu antworten: ", 5)

if input_method not in ['s', 't']:
    print("Keine gültige Eingabe erkannt oder Zeitüberschreitung. Sprechen wird als Standardmethode gewählt.")
    input_method = 's'

print(f"Gewählte Eingabemethode: {'Sprechen' if input_method == 's' else 'Tippen'}")

while True:
    LIGHT_GREEN = "\033[92m"
    RESET = "\033[0m"

    user_input = get_user_input(input_method)
    
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Auf Wiedersehen! Einen schönen Tag noch!")
        break
    
    # Store the user input with metadata
    add_to_vectordb(vector_db, user_input, "User", text_splitter)

    
    response = chat(user_input)
    print(f"{LIGHT_GREEN}AI: {response}{RESET}\n")
    spreche_text(response)

    # Store the AI response with metadata
    add_to_vectordb(vector_db, response, "AI", text_splitter)