# analyze_data_ai.py

import streamlit as st
from openai import OpenAI

# OpenAI istemcisi, st.secrets'ten API anahtarı alınıyor
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_data_ai_ui():
    st.header("🧠 AI ile Veri Analizi")

    prompt = st.text_area("Analiz için veri açıklamasını ya da sorunu yazın:")

    if st.button("Analiz Et"):
        if not prompt.strip():
            st.error("Lütfen bir açıklama ya da soru girin.")
            return

        with st.spinner("AI analiz yapıyor..."):
            result = ai_interpretation(prompt)
            st.markdown("### Sonuç:")
            st.write(result)


def ai_interpretation(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a data analysis assistant. "
                        "Provide insights and explain statistical results in plain language."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.7,
        )
        # ChatCompletion yanıtından içerik al
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"**AI Error:** {e}"
