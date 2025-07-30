import streamlit as st
import os
import time
import base64
from agents.ingestion_agent import process_file
from agents.retrieval_agent import store_chunks_mcp, search_chunks_mcp
from agents.llm_response_agent import generate_response_mcp

# Set Streamlit page config
st.set_page_config(page_title="Agentic RAG Chatbot", layout="wide", page_icon="🧠")

# --- Load Background Image for Hero Section ---
def get_base64_bg_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_image = get_base64_bg_image("1000_F_131155172_4ZVdaT7YF5yJHqircjy59DDxV6aWFds9.jpg")

# --- Inject CSS ---
st.markdown(f"""
    <style>
    .main {{
        background-color: #d0eaff !important;
    }}

    .hero {{
        background-image: url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-repeat: no-repeat;
        padding: 5rem 2rem;
        text-align: center;
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }}
    .hero h1 {{
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
    }}
    .hero p {{
        font-size: 1.2rem;
    }}

    .stTextInput>div>div>input,
    .stChatInput>div>div {{
        background-color: #f5faff !important;
        color: #000 !important;
    }}

    .stChatMessage.user {{
        background-color: #cce6ff !important;
        border-left: 4px solid #3399ff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: black;
    }}
    .stChatMessage.assistant {{
        background-color: #d6f5d6 !important;
        border-left: 4px solid #32cd32;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: black;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
    <div class="hero">
        <h1>Agentic RAG Chatbot 🤖</h1>
        <p>Upload a document and chat with it using intelligent agents</p>
    </div>
""", unsafe_allow_html=True)

# --- Session State ---
if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False
if "document_chunks" not in st.session_state:
    st.session_state.document_chunks = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Layout: Left (Upload) | Right (Chat) ---
left_col, right_col = st.columns([1, 2])

# --- LEFT: Upload Section ---
with left_col:
    st.subheader("📤 Upload Your Document")
    uploaded_file = st.file_uploader("Supported: PDF, DOCX, PPTX, CSV, TXT, MD", type=["pdf", "docx", "pptx", "csv", "txt", "md"])

    if uploaded_file:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())

        mcp_msg = process_file(uploaded_file.name)
        store_chunks_mcp(mcp_msg)

        st.session_state.document_chunks = mcp_msg["payload"]["chunks"]
        st.session_state.document_uploaded = True
        st.success("✅ Document uploaded and processed!")

# --- RIGHT: Chat Section ---
with right_col:
    st.subheader("💬 Ask Questions")

    if not st.session_state.document_uploaded:
        st.info("👈 Upload a document first to start chatting.")
    else:
        # Display past messages
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["message"])

        # New user input
        if query := st.chat_input("Ask something about the document..."):
            st.session_state.chat_history.append({"role": "user", "message": query})
            with st.chat_message("user"):
                st.markdown(query)

            retrieval_mcp = {
                "sender": "UI",
                "receiver": "RetrievalAgent",
                "type": "RETRIEVAL_REQUEST",
                "trace_id": "chat-session-1",
                "payload": {"query": query}
            }

            context_mcp = search_chunks_mcp(retrieval_mcp)
            response_mcp = generate_response_mcp(context_mcp)
            answer = response_mcp["payload"]["answer"]

            with st.chat_message("assistant"):
                placeholder = st.empty()
                typing_text = ""
                for char in answer:
                    typing_text += char
                    placeholder.markdown(typing_text)
                    time.sleep(0.01)

            st.session_state.chat_history.append({"role": "assistant", "message": answer})
