"""
Builds a FAISS vector store from ./knowledge using Hugging Face embeddings.
Run after seeding knowledge:
    python scripts/seed_knowledge.py
    python scripts/ingest.py
"""
import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

def load_markdown_docs(knowledge_dir: Path):
    docs = []
    for md in sorted(knowledge_dir.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        docs.append(Document(page_content=text, metadata={"source": md.name}))
    return docs

def main():
    load_dotenv()
    knowledge_dir = Path("knowledge")
    assert knowledge_dir.exists(), "Run scripts/seed_knowledge.py first to create ./knowledge files."

    raw_docs = load_markdown_docs(knowledge_dir)
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    splits = splitter.split_documents(raw_docs)

    # Initialize Hugging Face embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    # Build FAISS vector store
    vs = FAISS.from_documents(splits, embeddings)
    vectorstore_path = Path(__file__).parent.parent / "vectorstore"
    vs.save_local(str(vectorstore_path))
    print(f"Built vectorstore with {len(splits)} chunks from {len(raw_docs)} files -> {vectorstore_path}")

if __name__ == "__main__":
    main()
