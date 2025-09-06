import streamlit as st
import requests

API_URL = "http://localhost:8000/api"  # backend FastAPI

st.set_page_config(page_title="Academic RAG Chatbot", layout="wide")

# Sidebar
with st.sidebar:
    st.header("📚 Academic RAG Chatbot")
    st.write(
        """
        Welcome! Ask questions about your uploaded academic documents.
        
        **Instructions:**
        1. Upload your documents below.
        2. Type your question in the chat box.
        3. The bot will answer using your uploaded docs + LM Studio model.
        """
    )

st.title("🎓 Academic RAG Chatbot")

# --- Session State for Chat History ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- File Upload Section ---
uploaded_files = st.file_uploader(
    "📂 Upload your academic documents",
    type=["pdf", "txt", "docx", "zip"],
    accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("📤 Uploading files..."):
        for file in uploaded_files:
            files = {"file": (file.name, file.getvalue())}
            try:
                res = requests.post(f"{API_URL}/upload", files=files)
                if res.status_code == 200:
                    st.success(f"✅ Uploaded {file.name}")
                else:
                    st.error(f"❌ Failed to upload {file.name}")
            except Exception as e:
                st.error(f"⚠️ Error uploading {file.name}: {e}")

# --- Chat Handling Function ---
def send_message(user_input: str):
    if user_input.strip():
        # Add user message immediately
        st.session_state.history.append({"role": "user", "message": user_input})

        # Create placeholder for assistant response
        placeholder = st.empty()
        placeholder.chat_message("assistant").markdown("🤔 Thinking...")

        try:
            response = requests.post(f"{API_URL}/ask", json={"query": user_input})
            response.raise_for_status()
            answer = response.json().get("answer", "⚠️ No answer returned.")
        except Exception as e:
            answer = f"⚠️ Error contacting API: {e}"

        # Replace placeholder with actual answer
        placeholder.chat_message("assistant").markdown(answer)

        # Save bot response
        st.session_state.history.append({"role": "bot", "message": answer})

# --- Display Chat History ---
for chat in st.session_state.history:
    if chat["role"] == "user":
        with st.chat_message("user"):
            st.markdown(chat["message"])
    else:
        with st.chat_message("assistant"):
            st.markdown(chat["message"])

# --- Chat Input ---
if prompt := st.chat_input("Type your question here..."):
    send_message(prompt)
    st.rerun()  # forces UI refresh so message appears instantly
