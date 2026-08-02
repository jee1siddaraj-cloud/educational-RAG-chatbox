from rag import ask

print("="*50)
print("Educational RAG Chatbot")
print("="*50)
print("Type 'exit' to quit.")
print("Make sure you have built the index first by running ingest.py with a real PDF in the data folder.")

while True:

    question = input("\nYou : ")

    if question.lower() == "exit":
        break

    answer, sources = ask(question)

    print("\nBot:\n")

    print(answer)

    print("\nSources")

    for source in sources:
        print(source)