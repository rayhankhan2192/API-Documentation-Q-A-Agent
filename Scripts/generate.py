import ollama
from typing import List

def llm_prompt(question: str, context_chunks: List[str]) -> str:
    try:
        context = "\n\n".join(context_chunks)
        prompt = f"""Answer the following question using only the context provided below.
If the context is insufficient, say "I don't have enough information."

Context:
{context}

Question: {question}
Answer:"""

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"[ERROR] Failed to get response: {e}"
