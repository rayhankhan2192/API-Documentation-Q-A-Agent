# API-Documentation-Q-A-Agent

A question-answering agent designed to parse, embed, and query API documentation, providing accurate answers based on document content.

## Project Structure

```
API-Documentation-Q-A-Agent/
│
├── docs/ # API documentation files (input data)
├── scripts/ # Scripts for ingestion, embedding, and querying
│
│ ├── chunks_load_docs.py
│ ├── embed.py
│ └── query_agent.py
├── main.py # Gradio interface
├── cli.py # Terminal Based
└── requirements.txt # Python dependencies
└── README.md # This file
└── venv # create a venv in your local machine

```

# Setup & Running the Agent

## 1. Clone the repository

git clone [Github][def]

[def]: https://github.com/rayhankhan2192/API-Documentation-Q-A-Agent/tree/main

```bash 
cd api-docs-qa-agent

```
## 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```
## 4. Prepare your API documentation files

-Place your API docs (PDFs, markdown, etc.) inside the docs/ directory.

## 5. Run the agent

```bash
python main.py # for Gradio UI (Recomended for better interection)

python cli.py --rebuild # For terminal based, it will show all chunks [Don't run without --rebuild]
```
-This will launch a local Gradio web interface at http://127.0.0.1:7860.

### In the UI:
-Use the Embedding Setup tab to parse and embed your documentation.

-Use the Ask a Question tab to query the embedded docs and get answers.


## API Documentation & Assumptions

-This project assumes your API documentation files are located in docs/.

-Documents should be in formats supported by the parsing scripts (e.g., PDFs, markdown).

-The chunking logic splits documents into manageable text segments for embedding.

-Assumes a reasonably sized dataset that fits into available memory for embeddings.


## Design Choices

Vector Database: Uses Chromadb to store document embeddings (chunks) for fast similarity search.

Embedding Model: SentenceTransformer to convert text chunks into vector representations.

Large Language Model (LLM): Answers questions by prompting an LLM (usees OLLAMA llama3.2) using retrieved document chunks as context.

Framework: Gradio for creating an interactive web UI.

