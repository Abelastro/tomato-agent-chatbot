# 🍅 Tomato Disease Agent Chatbot (Multi-Agent System)

A **multi-agent AI system** for tomato disease detection and consultation. Combines RAG chatbot with CNN image analysis for comprehensive plant health diagnosis.

## 🏗️ Architecture Overview

**Dual-Agent System:**
- **🤖 RAG Chatbot Agent**: Uses FAISS vector store + OpenAI for disease knowledge retrieval
- **👁️ CNN Vision Agent**: Uses deep learning for image-based disease detection
- **🧠 Intelligent Integration**: Combines both agents for enhanced diagnosis

## 🚀 Quickstart

### 1) Clone & setup
```bash
git clone <YOUR-REPO-URL> tomato-agent-chatbot
cd tomato-agent-chatbot

# Create and activate a virtual environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Install deps
pip install -r requirements.txt
```

### 2) Configure your API key
Create `.env` from the example:
```bash
cp .env.example .env
# then edit .env and set OPENAI_API_KEY
```

### 3) Seed knowledge & build the vector store
```bash
python scripts/seed_knowledge.py     # writes markdown knowledge files into ./knowledge
python scripts/ingest.py             # builds ./vectorstore using FAISS
```

### 4) Start the backend API (CNN Model)
```bash
cd backend
python app.py
```
The API will run on http://localhost:5000

### 5) Run the frontend chatbot
```bash
cd frontend  
streamlit run app.py
```
Open the local URL shown in the terminal.

### 6) Use the system
- **Chat Mode**: Type questions about tomato diseases
- **Image Mode**: Upload leaf images for automatic detection
- **Combined Mode**: Get enhanced responses using both image analysis and knowledge base

---

## 🧠 What's inside
- **Streamlit UI** for chat and history
- **LangChain RAG pipeline** (OpenAI chat + embeddings)
- **FAISS** vector store persisted on disk
- **Flask API** for CNN image analysis
- **Intelligent integration** between vision and language agents

## 📂 Project structure
```
tomato-agent-chatbot/
├── frontend/                 # Streamlit application
│   ├── app.py               # Main chatbot interface
│   └── requirements.txt     # Frontend dependencies
├── backend/                 # Flask API server
│   ├── app.py              # CNN model inference API
│   └── requirements.txt    # Backend dependencies
├── model/                   # Deep learning models
│   └── mainModel.keras     # Pre-trained CNN model
├── scripts/                 # Knowledge management
│   ├─ seed_knowledge.py    # Creates disease markdown files
|   └─ ingest.py            # Builds FAISS vector store
├── shared/                  # Common utilities
│   └── disease_mapping.py  # Disease name mapping
├── knowledge/              # Generated disease knowledge
├── vectorstore/            # FAISS vector database
├── .env.example           # Environment template
├── requirements.txt       # Main dependencies
└── README.md
```

## 🔧 Tech choices
- **Frontend**: Streamlit + LangChain + OpenAI GPT
- **Backend**: Flask + TensorFlow/Keras + MobileNetV2  
- **Vector Store**: FAISS with OpenAI embeddings
- **Integration**: REST API + intelligent context injection

## 🧪 Try these features

**Chat Mode:**
- *"My tomato leaves have small dark circular spots with yellow halos. What could this be?"*
- *"Leaves are curling upwards and plants are stunted—diagnosis?"*
- *"Give me a treatment plan for early blight."*

**Image Mode:**
- Upload clear images of tomato leaves
- Get instant disease detection with confidence scores
- Click "Ask about this detection" for detailed information

**Combined Mode:**
- Automatic context injection from image analysis
- Enhanced responses using both visual and textual knowledge

## 🖼️ Vision Integration
The system now includes full CNN image analysis integration:
- **11 disease classes** detected by the CNN model
- **Intelligent mapping** between CNN outputs and knowledge base
- **Confidence-based filtering** (70% threshold)
- **Seamless context injection** into RAG responses


