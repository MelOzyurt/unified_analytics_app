# chat/chat_with_doc.py

import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def query_llm(question: str, context: str) -> str:
    """
    Sends the question and context to OpenAI's GPT model and returns the response.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are an AI assistant that answers questions based on provided documents."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ AI Error: {e}"

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
