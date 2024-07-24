# German AI Voice Assistant with RAG

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

## Roadmap

- [ ] We are considering switching from AstraDB to ChromaDB for vector storage. For more privacy.
- [ ] More skills will be added to enhance the assistant's capabilities.
- [ ] Regular database cleaning
  - Implement a cleaning strategy while preserving entries with "info_type" in metadata
  - Cleaning methods to consider:
    - [ ] Time-based cleaning
    - [ ] Redundancy removal
    - [ ] Context cleaning
    - [ ] Frequency-based cleaning
    - [ ] Size limitation

### Database Cleaning Strategy

Our database cleaning strategy will focus on maintaining relevant information while optimizing storage and performance. Here's a breakdown of our approach:

1. Time-based Cleaning:
   - Remove older entries not marked as user information (no "info_type" in metadata)
   - E.g., delete entries older than 30 days that aren't saved user information

2. Redundancy Removal:
   - Identify very similar entries (high similarity in embeddings)
   - Keep only the most recent entry
   - Exclude entries with "info_type" in metadata from this process

3. Context Cleaning:
   - Remove context information from past conversations that's no longer relevant
   - Always retain the most important or frequently accessed information

4. Frequency-based Cleaning:
   - Remove entries that are rarely or never retrieved, except those with an "info_type"

5. Size Limitation:
   - Implement a maximum number of entries or maximum database size
   - When the limit is reached, remove the oldest entries (excluding "info_type" entries)

This strategy will help us maintain a clean, efficient database while preserving crucial user information.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.