# Agentic RAG Chatbot 🤖

**Agentic RAG Chatbot** is a document-aware assistant powered by an agent-based Retrieval-Augmented Generation (RAG) architecture. It allows users to upload various types of documents (PDFs, Word, PPTs, CSVs, etc.) and ask natural language questions, receiving smart, context-driven answers. Behind the scenes, multiple specialized agents coordinate via a lightweight messaging protocol to break down and solve tasks like parsing, embedding, retrieving, and generating responses.

## What It Can Do

- Upload documents in PDF, DOCX, PPTX, TXT, CSV, or Markdown format.
- Chunk and semantically embed document contents using `SentenceTransformers`.
- Store and retrieve relevant context using FAISS vector search.
- Ask questions about the uploaded document through a sleek chat interface.
- Get coherent, context-aware answers from an open-source LLM like Mistral-7B (via OpenRouter).
- Enjoy a clean, responsive UI built using Streamlit with real-time updates.

## How It Works

The chatbot follows a modular, agent-driven architecture. Each agent is responsible for a distinct task and communicates using a custom `Model Context Protocol (MCP)` message format.

1. **IngestionAgent**: Parses the uploaded file, chunks its contents, and creates semantic embeddings.
2. **RetrievalAgent**: Receives a user query, performs vector search to retrieve relevant chunks from FAISS.
3. **LLMResponseAgent**: Sends the query and retrieved context to a language model to generate an answer.

All agent communication is traceable, allowing for future debugging, transparency, or extension into more complex agent systems.

## Setup Instructions

Follow these steps to set up and run the project locally:

✅ 1. Clone the repository


git clone https://github.com/S-Satwika/Agentic_RAG-Chatbot.git

cd Agentic_RAG-Chatbot


✅ 2. Create a Virtual Environment


python -m venv venv

source venv/bin/activate        # On Windows: venv\Scripts\activate

✅ 3. Install Dependencies


pip install -r requirements.txt


✅ 4. Download SentenceTransformer model

No manual download needed the model all-MiniLM-L6-v2 is automatically loaded by the SentenceTransformers library.


## API Keys & Configuration
This project uses external APIs for embeddings and LLM responses. Set the following environment variables:

**Hugging Face**

 HUGGINGFACE_API_TOKEN=your_huggingface_token
 
**OpenRouter API**

 OPENROUTER_API_KEY=your_openrouter_api_key

 
Get your key at: https://openrouter.ai


💡 Tip: You can also use a .env file and load it with python-dotenv.

## How to Run the App

After setting up everything, launch the app using:

streamlit run app.py

This will start a local server at:

👉 http://localhost:8501



