import os
import requests
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import sys
import torch
from pathlib import Path

# Add shared directory to path for disease mapping
sys.path.append(str(Path(__file__).resolve().parent.parent / 'shared'))
from disease_mapping import format_cnn_prediction_for_prompt
from huggingface_service import get_huggingface_service, set_huggingface_model

# --- Config ---
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
print(f"Looking for .env file at: {dotenv_path}")
if not dotenv_path.exists():
    st.error(f".env file not found at {dotenv_path}. Please create it with HUGGINGFACE_API_KEY and other required variables.")
else:
    try:
        with open(dotenv_path, "r", encoding="utf-8") as f:
            print(f".env file contents:\n{f.read()}")
        load_dotenv(dotenv_path=dotenv_path, override=True)
        print(f"HUGGINGFACE_API_KEY: {os.getenv('HUGGINGFACE_API_KEY')}")
        print(f"HUGGINGFACE_MODEL: {os.getenv('HUGGINGFACE_MODEL')}")
        print(f"HUGGINGFACE_API_URL: {os.getenv('HUGGINGFACE_API_URL')}")
        if not os.getenv("HUGGINGFACE_API_KEY"):
            st.error("HUGGINGFACE_API_KEY is not set after loading .env file. Please check the file contents and format.")
    except Exception as e:
        st.error(f"Failed to read .env file: {e}")
        print(f"Error reading .env file: {e}")

st.set_page_config(page_title="Tomato Disease Agent", page_icon="🍅", layout="wide")

VECTORSTORE_PATH = Path(__file__).resolve().parent.parent / "vectorstore"

# --- Sidebar UI ---
with st.sidebar:
    st.title("🍅 Tomato Agent")
    st.markdown("RAG chatbot for tomato diseases, enhanced with local vector store.")
    huggingface_model = os.getenv("HUGGINGFACE_MODEL", "microsoft/DialoGPT-medium")
    st.text_input("Hugging Face Model", value=huggingface_model, key="huggingface_model")
    top_k = st.slider("Top-k documents", min_value=2, max_value=8, value=4, step=1)
    strict_mode = st.checkbox("Strict mode (say 'I don't know' if unsure)", value=True)
    backend_url = os.getenv("BACKEND_URL", "http://localhost:5000")
    st.markdown("---")
    st.subheader("Image Analysis")
    st.markdown("Upload tomato leaf images for disease detection")
    if st.button("Clear chat"):
        st.session_state.messages = []

# --- Vectorstore Loader ---
def load_vectorstore():
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        model_kwargs = {"device": "cpu"}
        encode_kwargs = {"normalize_embeddings": True}
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        print(f"Loading vector store from: {VECTORSTORE_PATH}")
        if not VECTORSTORE_PATH.exists():
            st.error(f"Vector store directory {VECTORSTORE_PATH} does not exist. Run `python scripts/seed_knowledge.py` and `python scripts/ingest.py`.")
            return None
        vs = FAISS.load_local(
            folder_path=str(VECTORSTORE_PATH),
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )
        print("Vector store loaded successfully.")
        return vs
    except Exception as e:
        st.error(f"Failed to load vector store: {e}")
        st.info("The vector store may be incompatible. Try rebuilding it by running `python scripts/seed_knowledge.py` and `python scripts/ingest.py`.")
        return None

# --- RAG Chain Builder ---
SYSTEM_PROMPT = """
You are **TomatoDoc**, a plant pathologist assistant specialized in tomato diseases.
Use ONLY the provided context from the tomato disease vector store to answer the user's question.
If the answer isn't in the context, say 'I don't know from the provided context.'
Always include: likely disease(s), reasoning, and a short action plan (bullet points).
Be practical and concise.
"""

def format_docs(docs):
    parts = []
    sources = []
    for i, d in enumerate(docs, start=1):
        parts.append(f"Source {i} ({d.metadata.get('source','unknown')}):\n{d.page_content}")
        sources.append(d.metadata.get("source", f"doc_{i}"))
    return "\n\n".join(parts), sources

def build_chain(vs):
    if vs is None:
        st.error("Cannot build RAG chain: Vector store failed to load.")
        return None, None
    retriever = vs.as_retriever(search_kwargs={"k": top_k})
    current_model = st.session_state.get("huggingface_model", "microsoft/DialoGPT-medium")
    set_huggingface_model(current_model)
    try:
        huggingface_service = get_huggingface_service()
    except ValueError as e:
        st.error(f"Error initializing HuggingFace service: {e}")
        return None, None
    rag_chain = huggingface_service.build_rag_chain(retriever, SYSTEM_PROMPT)
    return rag_chain, retriever

# --- Image Analysis ---
def analyze_image(image_file):
    """Send image to backend API for disease detection."""
    try:
        files = {"file": image_file}
        response = requests.post(f"{backend_url}/predict", files=files)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error analyzing image: {response.json().get('error', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Failed to connect to backend API: {e}")
        return None

def display_image_result(result):
    if result.get('className') == 'No leaf detected':
        st.warning(result['message'])
    else:
        st.success(f"**Detected:** {result.get('humanName', result['className'])}")
        st.info(f"**Confidence:** {result.get('confidence', 0)}%")
        if result.get('kbSlug'):
            st.session_state.last_detection = result
            st.button("💬 Ask about this detection", key="ask_about_detection")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_detection" not in st.session_state:
    st.session_state.last_detection = None

# --- Main Layout ---
st.header("🍅 Tomato Disease Agent")
st.caption("Multi-agent system: RAG chatbot with tomato disease knowledge + CNN image detection")

uploaded_file = st.file_uploader(
    "📷 Upload tomato leaf image for analysis", 
    type=['jpg', 'jpeg', 'png'],
    help="Upload a clear image of tomato leaves for disease detection"
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    with st.spinner("🔍 Analyzing image..."):
        result = analyze_image(uploaded_file)
    if result:
        display_image_result(result)

if not VECTORSTORE_PATH.exists():
    st.warning(f"Vector store not found at {VECTORSTORE_PATH}. Run `python scripts/seed_knowledge.py` then `python scripts/ingest.py` in your terminal.")
else:
    vs = load_vectorstore()
    if vs:
        chain, retriever = build_chain(vs)
        if chain and retriever:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            if st.session_state.get('last_detection') and st.session_state.get('ask_about_detection', False):
                detection = st.session_state.last_detection
                question = f"Tell me about {detection.get('humanName', detection['className'])} and how to treat it"
                st.session_state.last_detection = None
                st.session_state.ask_about_detection = False
            else:
                question = st.chat_input("Describe the symptoms or ask a question about tomato diseases...")

            if question:
                final_question = question
                cnn_context = None
                if st.session_state.get('last_detection'):
                    detection = st.session_state.last_detection
                    cnn_context = format_cnn_prediction_for_prompt(
                        detection['className'], 
                        detection['confidence']
                    )
                if cnn_context:
                    final_question = f"{cnn_context}\n\nUser question: {question}"
                    st.session_state.last_detection = None

                st.session_state.messages.append({"role": "user", "content": question})

                docs = retriever.invoke(question)
                context_text, sources = format_docs(docs)

                q = final_question
                if strict_mode:
                    q += "\n\nIf uncertain, reply: 'I don't know from the provided context.'"

                with st.spinner("Thinking..."):
                    answer = chain.invoke(q)

                st.session_state.messages.append({"role": "assistant", "content": answer})

                with st.chat_message("assistant"):
                    st.markdown(answer)
                    if cnn_context:
                        st.info("💡 Response enhanced with image analysis results")
                    with st.expander("Sources used"):
                        for s in sources:
                            st.code(s)

        st.caption("Tip: Adjust Top‑k in the sidebar to broaden/narrow context.")
