"""
Impelemted a Gradio interface for an API Documentation Q&A Agent.

"""

import os
import gradio as gr
from Scripts.chunks_load_docs import load_and_parse_docs
from Scripts.embed import embed_and_store
from Scripts.query_agent import get_top_k_chunks, llm_prompt

DOC_PATH = r"E:\Python\Machile Learning\2_Artificial Intelligece\1_API Documentation Q&A Agent\docs"
EMBEDDINGS_PATH = "embeddings/chromadb"

last_chunks = []

def rebuild_embeddings():
    global last_chunks
    try:
        chunks = load_and_parse_docs(DOC_PATH)
        if not chunks:
            return "❌ No chunks were generated. Check your documents or parsing logic.", ""
        
        embed_and_store(chunks)
        last_chunks = chunks

        display = ""
        for chunk in chunks:
            display += f"---\n"
            display += f"**Chunk ID:** `{chunk['chunk_id']}`\n\n"
            display += f"**Source:** `{chunk['source']}`\n\n"
            display += "```\n" + chunk["text"][:1000] + ("..." if len(chunk["text"]) > 1000 else "") + "\n```\n\n"

        return f"✅ Embedding completed! {len(chunks)} chunks stored.", display
    except Exception as e:
        return f"❌ Embedding failed: {str(e)}", ""

def answer_question(question, top_k, show_chunks):
    if not question.strip():
        return "⚠️ Please enter a question.", ""

    try:
        context = get_top_k_chunks(question.strip(), k=top_k)
        used_chunks = context.get("documents", [])
        if not used_chunks:
            return "⚠️ No relevant chunks were found.", ""

        answer = llm_prompt(question, [doc["text"] for doc in used_chunks])

        if show_chunks:
            chunk_texts = ""
            for i, doc in enumerate(used_chunks, 1):
                chunk_texts += f"🔹 **Chunk {i}** - Source: `{doc.get('source', 'N/A')}`\n"
                chunk_texts += "```\n" + doc['text'][:1000] + ("..." if len(doc['text']) > 1000 else "") + "\n```\n\n"
            return answer, chunk_texts
        else:
            return answer, ""

    except Exception as e:
        return f"❌ Error: {str(e)}", ""

with gr.Blocks(title="API Doc Q&A Agent") as demo:
    gr.Markdown("# 🤖 API Documentation Q&A Agent")

    with gr.Tab("📚 Embedding Setup"):
        embed_output = gr.Textbox(label="Embedding Status", lines=3, interactive=False)
        chunk_display = gr.Markdown(label="Parsed Chunks Preview")
        with gr.Row():
            embed_button = gr.Button("🔄 Rebuild Embeddings")
            clear_embed = gr.Button("🧹 Clear")
        embed_button.click(fn=rebuild_embeddings, outputs=[embed_output, chunk_display])
        clear_embed.click(fn=lambda: ("", ""), outputs=[embed_output, chunk_display])

    with gr.Tab("💬 Ask a Question"):
        with gr.Row():
            question = gr.Textbox(label="Your Question", placeholder="Ask something about the API...", lines=2)
            show_chunks = gr.Checkbox(label="Show Retrieved Chunks", value=True)

        with gr.Row():
            submit_button = gr.Button("Get Answer")
            clear_qa = gr.Button("🧹 Clear")
        with gr.Row():
            answer_box = gr.Textbox(label="🧠 Answer", lines=3)
            chunk_answer_display = gr.Textbox(label="🔄 Chunks Used for Answer", lines=3)

        submit_button.click(
            fn=lambda q, show: answer_question(q, 5, show),  # Fixed k=5
            inputs=[question, show_chunks],
            outputs=[answer_box, chunk_answer_display]
        )

        clear_qa.click(
            fn=lambda: ("", "", ""),
            outputs=[question, answer_box, chunk_answer_display]
        )


#demo.launch()
demo.launch(share=True)




# import os
# import streamlit as st
# from Scripts.chunks_load_docs import load_and_parse_docs
# from Scripts.embed import embed_and_store
# from Scripts.query_agent import get_top_k_chunks
# from Scripts.query_agent import llm_prompt

# os.environ["STREAMLIT_WATCHER_TYPE"] = "poll"
# os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# DOC_PATH = r"E:\Python\Machile Learning\2_Artificial Intelligece\1_API Documentation Q&A Agent\docs"
# EMBEDDINGS_PATH = "embeddings/chromadb"

# st.set_page_config(page_title="API Doc Q&A", layout="wide")
# st.title("🤖 API Documentation Q&A Agent")

# with st.sidebar:
#     st.header("Configuration")
#     rebuild = st.button("🔄 Rebuild Embeddings")
#     top_k = st.slider("Top K Chunks", min_value=1, max_value=10, value=5)
#     show_chunks = st.checkbox("Show Retrieved Chunks", value=True)

# chunks = []

# if rebuild or not os.path.exists(EMBEDDINGS_PATH) or not os.listdir(EMBEDDINGS_PATH):
#     st.info("📚 Ingesting and embedding documentation. Please wait...")
#     try:
#         chunks = load_and_parse_docs(DOC_PATH)
#         if not chunks:
#             st.error("❌ No chunks were generated. Check your documents or parsing logic.")
#             st.stop()
#         embed_and_store(chunks)
#         st.success("✅ Embedding completed!")

#         st.markdown("### 📄 All Document Chunks")
#         for chunk in chunks:
#             st.markdown(f"**Chunk ID:** `{chunk['chunk_id']}`")
#             st.markdown(f"**Source:** `{chunk['source']}`")
#             st.code(chunk['text'][:1000] + ("..." if len(chunk['text']) > 1000 else ""), language="markdown")
#     except Exception as e:
#         st.error(f"❌ Embedding failed: {e}")
#         st.stop()


# st.subheader("Ask a question about the API")
# question = st.text_input("Your question:")

# if question and question.strip():
#     try:
#         context = get_top_k_chunks(question.strip(), k=top_k)

#         used_chunks = context["documents"]
#         if not used_chunks:
#             st.warning("⚠️ No relevant chunks were found.")
#         else:
#             answer = llm_prompt(question, [doc["text"] for doc in used_chunks])
#             st.markdown("### 🧠 Answer:")
#             st.success(answer)

#             if show_chunks:
#                 st.markdown("### 🔍 Chunks Used for Answering:")
#                 for i, doc in enumerate(used_chunks, 1):
#                     st.markdown(f"**[{i}] Source: `{doc.get('source', 'N/A')}`**")
#                     st.code(
#                         doc["text"][:1000] + ("..." if len(doc["text"]) > 1000 else ""),
#                         language="markdown"
#                     )
#     except Exception as e:
#         st.error(f"Error during answer generation: {e}")
