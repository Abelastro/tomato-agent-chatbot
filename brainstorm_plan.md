# Vector Store Path Resolution Plan

## Problem Analysis
- Two vector store locations exist: `vectorstore/` and `scripts/vectorstore/`
- `frontend/app.py` expects vectorstore in main directory (`vectorstore/`)
- `ingest.py` uses relative path, creating vectorstore based on execution directory

## Solution Options

### Option 1: Clean up and use absolute paths (Recommended)
1. Delete the duplicate `scripts/vectorstore/` directory
2. Modify `ingest.py` to use absolute path to main `vectorstore/` directory
3. Update documentation to clarify execution from project root

### Option 2: Modify frontend to handle both locations
1. Check both locations for vectorstore
2. Use whichever exists, with preference for main directory

### Option 3: Centralize vectorstore management
1. Create a shared configuration file for vectorstore path
2. Update both frontend and scripts to use centralized config

## Recommended Implementation (Option 1)

### Steps:
1. Remove `scripts/vectorstore/` directory
2. Modify `ingest.py` to use absolute path: `Path(__file__).parent.parent / "vectorstore"`
3. Update documentation to specify running from project root
4. Verify frontend/app.py works with main vectorstore

### Files to Modify:
- `scripts/ingest.py` - Fix path resolution
- `SETUP_INSTRUCTIONS.md` - Update execution instructions
- (Optional) Add error handling in frontend for better UX

## Verification:
- Run `python scripts/seed_knowledge.py` from project root
- Run `python scripts/ingest.py` from project root  
- Verify vectorstore created in main directory
- Test frontend app loads vectorstore successfully
