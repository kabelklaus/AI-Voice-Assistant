# German AI Voice Assistant with RAG

This project implements a German-speaking AI assistant using Retrieval-Augmented Generation (RAG) with LangChain, Groq API, and Chroma for vector storage.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [MacOS Users: Installing PyAudio](#macos-users-installing-pyaudio)
- [Downloading Ollama Embedding Model](#downloading-ollama-embedding-model)
- [Usage](#usage)
- [Adding New Skills](#adding-new-skills)
- [Roadmap](#roadmap)
  - [Database Cleaning Strategy](#database-cleaning-strategy)
- [Contributing](#contributing)
- [License](#license)

## Features

- Uses Groq API with the llama-3.1-70b-versatile
- Implements LangChain for data management and processing
- Utilizes Chroma for chat history storage
- Employs nomic-embed-text:latest from Ollama for embeddings
- Implements text chunking for efficient processing
- Allows user interaction through text or speech input
- Manages configuration data using dotenv

## Prerequisites

- Python 3.8+ (I use 3.11)
- Groq API access
- Chroma
- Ollama running locally

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kabelklaus/AI-Voice-Assistant.git
cd AI-Voice-Assistant
```
2. Install the required packages:
```bash
pip install -r requirements.txt
```
3. Rename `.env_example` to `.env` and fill in your API keys and other configuration details:
```bash
mv .env_example .env
```
4. Edit the `.env` file with your specific credentials and settings.

## MacOS Users: Installing PyAudio

If you're using a Mac and need to install PyAudio, follow these steps:

1. Install Xcode from the App Store and restart your computer.
2. Run the following commands in sequence:

```bash
xcode-select --install
brew remove portaudio
brew install portaudio
pip3 install pyaudio
```
Note: Xcode command line tools are required for some installations. Homebrew requires Xcode, so you can also just run:
```bash
xcode-select --install
```

## Downloading Ollama Embedding Model

This project uses the `nomic-embed-text:latest` model from Ollama for embeddings. To download this model:

1. Ensure Ollama is installed on your system. If not, follow the installation instructions at [Ollama's official website](https://ollama.com/).
2. Open a terminal or command prompt.
3. Run the following command to download the model:
```bash
ollama pull nomic-embed-text:latest
```
This command will download and install the latest version of the `nomic-embed-text` model.
4. Wait for the download to complete. The model size is approximately 670MB, so it may take a few minutes depending on your internet connection.

Once the model is downloaded, Ollama will automatically use it for generating embeddings in this project.

## Usage

1. Ensure Ollama is running locally for embeddings.

2. Run the main script:
```bash
python main.py
```
3. Follow the prompts to interact with the AI assistant. You can choose between text or speech input.

## Adding New Skills

To extend the assistant's capabilities, you can add new skills:

1. Create a new Python file in the `skills` directory (e.g., `new_skill.py`).
2. Implement the skill's functionality.
3. Import and integrate the new skill in `main.py`.
4. Add the skill to the `response_prompt.py` file to make the LLM aware of it. Include an example of how to use the skill to help the LLM better understand and utilize it.

Example addition to `response_prompt.py`:

```python
If the user asks about the weather, respond with:
FUNCTION_CALL: get_weather(location)
For example:
- If the user asks "Wie ist das Wetter in Berlin?", respond with:
FUNCTION_CALL: get_weather("Berlin")
```
This will ensure that the LLM knows how to use the new skill and can incorporate it into its responses.

## Roadmap

- [x] We are considering switching from AstraDB to ChromaDB for vector storage. For more privacy.
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