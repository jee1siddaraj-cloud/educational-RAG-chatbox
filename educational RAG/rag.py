import os
import pickle
import faiss
import numpy as np

import google.generativeai as genai

from embeddings import create_embeddings
from config import GEMINI_API_KEY, MODEL_NAME

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)
else:
    model = None

if os.path.exists("vector_db/faiss.index") and os.path.exists("vector_db/documents.pkl"):
    index = faiss.read_index("vector_db/faiss.index")

    with open("vector_db/documents.pkl", "rb") as f:
        documents = pickle.load(f)
else:
    index = None
    documents = []


def _build_fallback_answer(question, context):
    if not context.strip():
        return "I couldn't find this information in the indexed content."

    return (
        "I found related content in the indexed document.\n\n"
        f"{context[:1200]}"
    )


def ask(question):

    if index is None or not documents:
        return "The vector index has not been built yet. Run the ingestion step first.", []

    query_embedding = create_embeddings([question])

    _, I = index.search(
        np.array(query_embedding),
        5
    )

    context = ""

    sources = []

    for idx in I[0]:
        if idx < 0 or idx >= len(documents):
            continue

        doc = documents[idx]

        context += doc["text"] + "\n\n"

        sources.append(
            f'{doc["file"]} Page {doc["page"]}'
        )

    if model and GEMINI_API_KEY:
        prompt = f"""
You are an educational assistant.

Answer ONLY using the context below.

If the answer isn't present, say

"I couldn't find this information."

Context

{context}

Question

{question}
"""

        response = model.generate_content(prompt)
        return response.text, sources

    return _build_fallback_answer(question, context), sources