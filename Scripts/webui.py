
import os
import streamlit as st
from ingest import load_and_parse_docs
from embed import embed_and_store
from retrieve import get_top_k_chunks
from generate import llm_prompt

os.environ["STREAMLIT_WATCHER_TYPE"] = "poll"
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

DOC_PATH = r"E:\Python\Machile Learning\2_Artificial Intelligece\1_API Documentation Q&A Agent\docs"
EMBEDDINGS_PATH = "embeddings/chromadb"

st.set_page_config(page_title="API Doc Q&A", layout="wide")
st.title("🤖 API Documentation Q&A Agent")

with st.sidebar:
    st.header("Configuration")
    rebuild = st.button("🔄 Rebuild Embeddings")
    top_k = st.slider("Top K Chunks", min_value=1, max_value=10, value=5)
    show_chunks = st.checkbox("Show Retrieved Chunks", value=True)

chunks = []

if rebuild or not os.path.exists(EMBEDDINGS_PATH) or not os.listdir(EMBEDDINGS_PATH):
    st.info("📚 Ingesting and embedding documentation. Please wait...")
    try:
        chunks = load_and_parse_docs(DOC_PATH)
        if not chunks:
            st.error("❌ No chunks were generated. Check your documents or parsing logic.")
            st.stop()
        embed_and_store(chunks)
        st.success("✅ Embedding completed!")

        st.markdown("### 📄 All Document Chunks")
        for chunk in chunks:
            st.markdown(f"**Chunk ID:** `{chunk['chunk_id']}`")
            st.markdown(f"**Source:** `{chunk['source']}`")
            st.code(chunk['text'][:1000] + ("..." if len(chunk['text']) > 1000 else ""), language="markdown")
    except Exception as e:
        st.error(f"❌ Embedding failed: {e}")
        st.stop()


st.subheader("Ask a question about the API")
question = st.text_input("Your question:")

if question and question.strip():
    try:
        context = get_top_k_chunks(question.strip(), k=top_k)

        used_chunks = context["documents"]
        if not used_chunks:
            st.warning("⚠️ No relevant chunks were found.")
        else:
            answer = llm_prompt(question, [doc["text"] for doc in used_chunks])
            st.markdown("### 🧠 Answer:")
            st.success(answer)

            if show_chunks:
                st.markdown("### 🔍 Chunks Used for Answering:")
                for i, doc in enumerate(used_chunks, 1):
                    st.markdown(f"**[{i}] Source: `{doc.get('source', 'N/A')}`**")
                    st.code(
                        doc["text"][:1000] + ("..." if len(doc["text"]) > 1000 else ""),
                        language="markdown"
                    )
    except Exception as e:
        st.error(f"Error during answer generation: {e}")






##before code

# # 🧠 Q&A interface
# st.subheader("Ask a question about the API")
# question = st.text_input("Your question:")

# if question and question.strip():
#     try:
#         context = get_top_k_chunks(question.strip(), k=top_k)
#         answer = llm_prompt(question, context["documents"])

#         st.markdown("### 🧠 Answer:")
#         st.success(answer)

#         if show_chunks:
#             st.markdown("### 🔍 Top Retrieved Chunks:")
#             for i, doc in enumerate(context["documents"], 1):
#                 st.markdown(f"**[{i}] Source: {doc.get('source', 'N/A')}**")
#                 st.code(doc["text"][:1000] + ("..." if len(doc["text"]) > 1000 else ""), language="markdown")

#     except Exception as e:
#         st.error(f"❌ Error during answer generation: {e}")

