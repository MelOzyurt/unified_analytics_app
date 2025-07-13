# chat/chat_with_doc.py

import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Placeholder for LLM API call - replace with your actual LLM integration
def query_llm(question: str, context: str) -> str:
    """
    Simulate an LLM answering a question based on the given context.
    Replace this with actual API call to GPT or other model.
    """
    # For demo, just echo question + first 200 chars of context
    return f"Answering your question:\n\n**Question:** {question}\n\n**Context snippet:** {context[:200]}...\n\n(This is a placeholder answer.)"

def chat_with_doc_ui(doc_text: str):
    st.header("💬 Chat With Document")

    if not doc_text or not doc_text.strip():
        st.warning("No document text available for chatting.")
        return

    question = st.text_input("Ask a question about your document:")

    if st.button("Get Answer"):
        if not question.strip():
            st.error("Please enter a question.")
            return

        with st.spinner("Generating answer..."):
            answer = query_llm(question, doc_text)
            st.markdown(f"**Answer:**\n\n{answer}")
