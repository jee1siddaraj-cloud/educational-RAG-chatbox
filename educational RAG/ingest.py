import os
import pickle
import faiss
import numpy as np

from embeddings import create_embeddings
from utils.pdf_loader import load_pdf

CHUNK_SIZE = 500


def chunk_text(text):

    chunks = []

    for i in range(0, len(text), CHUNK_SIZE):
        chunks.append(text[i:i+CHUNK_SIZE])

    return chunks


documents = []

folder = "data"
os.makedirs("vector_db", exist_ok=True)

if not os.path.exists(folder):
    print(f"Folder '{folder}' does not exist.")
    raise SystemExit(1)

for file in os.listdir(folder):

    if not file.endswith(".pdf"):
        continue

    pdf_path = os.path.join(folder, file)
    pages = load_pdf(pdf_path)

    if not pages:
        print(f"Skipped {file}: no readable text was extracted.")
        continue

    for page in pages:

        if not page.get("text"):
            continue

        chunks = chunk_text(page["text"])

        for chunk in chunks:

            documents.append({

                "text": chunk,

                "page": page["page"],

                "file": file

            })

if not documents:
    print("No text was extracted from the PDF files.")
    raise SystemExit(1)

texts = [doc["text"] for doc in documents]

embeddings = create_embeddings(texts)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

faiss.write_index(index, "vector_db/faiss.index")

with open("vector_db/documents.pkl", "wb") as f:
    pickle.dump(documents, f)

print(f"Indexed {len(documents)} chunks from {len(os.listdir(folder))} file(s).")