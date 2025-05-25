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

# ⚙️ Setup & Running the Agent

## 1. Clone the repository

```bash
git clone https://github.com/rayhankhan2192/API-Documentation-Q-A-Agent
```
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
-Download and Install ollama https://ollama.com/ 
```bash
# 1. open terminal & active ollama 
ollama run llama3.2

# 2. for Gradio UI (Recommended for better interection)
python main.py # This will launch a local Gradio web interface at http://127.0.0.1:7860.

# For terminal based, it will also show all chunks [Don't run without --rebuild]
python cli.py --rebuild 
```

## 6. 🧠 How to Use the App

### Embedding Setup Tab
--Click Rebuild Embeddings to parse and embed your documentation

--View extracted and chunked content below

### Ask a Question Tab
--Enter a question about your API

--Adjust Top K Chunks slider for context depth

--Optionally toggle Show Retrieved Chunks

--Press Get Answer to see the response generated from your docs

## 📄 API Documentation & Assumptions

--Assumes all documents are placed in the docs/ directory

--Supports PDFs, markdown, and plain text files (extendable)

--Chunking splits long texts into manageable segments for embeddings

--Assumes documents are small/medium enough to fit in memory during embedding


## 🧩 Design Choices

--Vector Database: ChromaDB for fast retrieval of document chunks

--Embedding Model: SentenceTransformer (e.g., all-MiniLM-L6-v2) for efficient text-to-vector conversion

--LLM Used: OLLAMA's llama3.2 model (can be replaced or extended with any LLM)

--Frontend: Gradio for a responsive and user-friendly UI

--CLI Support: Provided via cli.py for terminal-based interaction



## 📬 Contact
Rayhan Khan

📧 Personal     : rayhan.khan.2192@gmail.com

📧 Institutional : rayhan35-831@diu.edu.bd

[🔗 LinkedIn Profile](https://www.linkedin.com/in/rayhankhan2192/)

[🔗 GitHub Profile](https://github.com/rayhankhan2192)
