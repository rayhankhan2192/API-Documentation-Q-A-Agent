# API-Documentation-Q-A-Agent

A question-answering agent designed to parse, embed, and query API documentation, providing accurate answers based on document content.

----

## Project Structure

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

## Setup & Running the Agent