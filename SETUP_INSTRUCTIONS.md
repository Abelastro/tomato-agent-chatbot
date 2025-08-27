# Setup Instructions for Tomato Disease Agent

## 1. Knowledge Base Setup

First, set up the tomato disease knowledge base and vector store:

```bash
# From the project root directory (important!)
python scripts/seed_knowledge.py
python scripts/ingest.py
```

This will:
- Create markdown files in `knowledge/` directory
- Build a FAISS vector store in `vectorstore/` directory

## 2. Get a Hugging Face API Key

1. Go to https://huggingface.co/settings/tokens
2. Create a new token with "read" permissions
3. Copy the token to your clipboard

## 3. Update Environment Variables

Edit the `.env` file in the project root directory and replace the placeholder values:

```env
# Hugging Face API Key
HUGGINGFACE_API_KEY=your_actual_api_key_here

# Hugging Face Model (use a model that works with free tier)
HUGGINGFACE_MODEL=microsoft/DialoGPT-medium
```

## 4. Alternative Models for Free Tier

If you're using the free tier, try these models that typically work better:

- `microsoft/DialoGPT-medium` (conversational model)
- `gpt2` (smaller model, usually works)
- `distilgpt2` (even smaller, should work)

## 5. Testing the Setup

Run the test script to verify everything works:

```bash
python test_huggingface_api.py
```

## 6. Running the Application

Start the Streamlit application:

```bash
streamlit run frontend/app.py
```

## Troubleshooting

### Vector Store Not Found
If you get "Vector store not found" error:
- Make sure you ran `python scripts/seed_knowledge.py` and `python scripts/ingest.py` from the project root directory
- Check that `vectorstore/` directory exists in the main project folder (not in scripts/)
- The vectorstore should contain `index.faiss` and `index.pkl` files

### 403 Error
If you get a 403 error, it means your API key doesn't have sufficient permissions. Make sure:
- You're using a valid API key from Hugging Face
- The key has at least "read" permissions
- You're not trying to use a premium/paid model

### Model Loading Issues
Some models may take time to load on Hugging Face's servers. If you get a "model is loading" response, wait a minute and try again.

### Rate Limiting
Free tier has rate limits. If you get rate limit errors, wait a bit before making more requests.
