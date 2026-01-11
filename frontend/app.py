import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="Ask Me Anything About Yoga", layout="centered")

st.title("🧘 Ask Me Anything About Yoga")
st.write("Powered by a Retrieval-Augmented Generation (RAG) system")

query = st.text_area(
    "Ask anything about yoga:",
    placeholder="e.g. What are the benefits of shavasana?"
)

if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, params={"query": query})
                data = response.json()

                # Safety warning
                if data.get("isUnsafe"):
                    st.error(
                        "⚠️ This question involves health-related risks. "
                        "Please consult a certified yoga instructor or medical professional."
                    )

                # Answer
                st.subheader("Answer")
                st.write(data.get("answer", "No answer returned."))

                # Sources
                st.subheader("Sources Used")
                for src in data.get("sources", []):
                    st.write(f"- **{src['id']}**: {src['title']}")

            except Exception as e:
                st.error(f"Error connecting to backend: {e}")
