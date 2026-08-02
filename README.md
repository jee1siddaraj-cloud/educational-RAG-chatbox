# 📚 Educational RAG Chatbot

An end-to-end **Retrieval-Augmented Generation (RAG)** chatbot built using **Python**, **FAISS**, **Sentence Transformers**, and **Google Gemini API**. The chatbot allows users to upload educational PDF documents, indexes them into a vector database, retrieves the most relevant content for a query, and generates context-aware answers with source citations.

---

## 🚀 Features

* 📄 Supports one or multiple PDF documents
* ✂️ Automatic text extraction and chunking
* 🧠 Semantic embeddings using `all-MiniLM-L6-v2`
* ⚡ Fast similarity search with **FAISS**
* 🤖 Answer generation using **Google Gemini API**
* 📖 Displays source PDF names and page numbers
* 🏗️ Modular project structure for easy maintenance

---

## 🛠️ Tech Stack

* Python 3.10+
* FAISS
* Sentence Transformers
* PyPDF
* Google Gemini API
* NumPy
* python-dotenv

---

## 📂 Project Structure

```text
Educational-RAG/
│
├── app.py                 # Main chatbot application
├── ingest.py              # PDF ingestion and indexing
├── rag.py                 # Retrieval + LLM pipeline
├── embeddings.py          # Embedding generation
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Gemini API Key
│
├── data/                  # Store PDF documents
│
├── vector_db/
│   ├── faiss.index
│   └── documents.pkl
│
└── utils/
    └── pdf_loader.py
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/Educational-RAG.git
cd Educational-RAG
```

### 2. Create a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure Gemini API

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

You can generate a free API key from:

https://aistudio.google.com/app/apikey

---

## 📥 Add PDF Documents

Place one or more PDF files inside the `data/` folder.

Example:

```text
data/
├── MachineLearning.pdf
├── PythonTutorial.pdf
└── AINotes.pdf
```

---

## 📚 Create the Vector Database

Run:

```bash
python ingest.py
```

This process will:

* Read all PDFs
* Extract text
* Split text into chunks
* Generate embeddings
* Store vectors in FAISS
* Save document metadata

---

## 💬 Start the Chatbot

Run:

```bash
python app.py
```

Example:

```text
==================================================
Educational RAG Chatbot
==================================================

You:
What is machine learning?

Bot:

Machine learning is a branch of artificial intelligence that enables systems to learn from data without being explicitly programmed.

Sources

MachineLearning.pdf - Page 15
AINotes.pdf - Page 7
```

---

## 🔄 Workflow

```text
User Question
        │
        ▼
Sentence Transformer
(Query Embedding)
        │
        ▼
FAISS Vector Search
        │
        ▼
Top 5 Relevant Chunks
        │
        ▼
Google Gemini API
        │
        ▼
Generated Answer
        │
        ▼
Answer + Source Citations
```

---

## 📦 Requirements

```text
faiss-cpu
sentence-transformers
pypdf
google-generativeai
numpy
python-dotenv
tqdm
```

Install using:

```bash
pip install -r requirements.txt
```

---

## 🚀 Future Enhancements

* Streamlit web interface
* Chat history and conversational memory
* Support for DOCX and TXT files
* OCR support for scanned PDFs
* ChromaDB or Qdrant integration
* Hybrid keyword + semantic search
* Cross-encoder re-ranking
* Inline citations in responses
* Incremental indexing for newly added PDFs

---

## 🎯 Learning Objectives

This project demonstrates:

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases
* Large Language Model Integration
* Document Embedding
* Information Retrieval
* Prompt Engineering

---

## 📜 License

This project is intended for educational and learning purposes. Feel free to modify and extend it for your own projects.
