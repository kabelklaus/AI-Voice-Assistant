# German AI Assistant with RAG

This project implements a German-speaking AI assistant using Retrieval-Augmented Generation (RAG) with LangChain, Groq API, and AstraDB for vector storage.

## Features

- Uses Groq API with the llama-3.1-70b-versatile
- Implements LangChain for data management and processing
- Utilizes AstraDB for chat history storage (may switch to ChromaDB in the future)
- Employs nomic-embed-text:latest from Ollama for embeddings
- Implements text chunking for efficient processing
- Allows user interaction through text or speech input
- Manages configuration data using dotenv

## Prerequisites

- Python 3.8+ (I use 3.11)
- Groq API access
- AstraDB account (https://astra.datastax.com/)
- Ollama running locally

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/german-ai-assistant.git
cd german-ai-assistant
Copy
2. Install the required packages:
pip install -r requirements.txt
Copy
3. Rename `.env_example` to `.env` and fill in your API keys and other configuration details:
mv .env_example .env
Copy
4. Edit the `.env` file with your specific credentials and settings.

## Usage

1. Ensure Ollama is running locally for embeddings.

2. Run the main script:
python main.py
Copy
3. Follow the prompts to interact with the AI assistant. You can choose between text or speech input.

## Adding New Skills

To extend the assistant's capabilities, you can add new skills:

1. Create a new Python file in the `skills` directory (e.g., `new_skill.py`).
2. Implement the skill's functionality.
3. Import and integrate the new skill in `main.py`.

## Future Development

- We are considering switching from AstraDB to ChromaDB for vector storage.
- More skills will be added to enhance the assistant's capabilities.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.