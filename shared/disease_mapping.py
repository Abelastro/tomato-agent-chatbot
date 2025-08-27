"""
Disease name mapping between CNN model classes and knowledge base slugs.
This ensures consistent naming across the RAG chatbot and image classifier.
"""

# Mapping from CNN model class names to knowledge base slugs
CNN_TO_KB_MAPPING = {
    'Tomato_Bacterial_spot': 'bacterial-spot',
    'Tomato_Early_blight': 'early-blight', 
    'Tomato_Late_blight': 'late-blight',
    'Tomato_Leaf_Mold': None,  # Not in current knowledge base
    'Tomato_Septoria_leaf_spot': 'septoria-leaf-spot',
    'Tomato_Spider_mites_Two-spotted_spider_mite': None,  # Not in current knowledge base
    'Tomato_Target_Spot': None,  # Not in current knowledge base
    'Tomato_Yellow_Leaf_Curl_Virus': None,  # Not in current knowledge base
    'Tomato_mosaic_virus': 'tomato-mosaic-virus',
    'Tomato_healthy': None,  # Healthy plant
    'Tomato_Leaf_Curl_Virus': None  # Not in current knowledge base
}

# Reverse mapping from knowledge base slugs to human-readable names
KB_TO_HUMAN = {
    'early-blight': 'Early Blight',
    'late-blight': 'Late Blight', 
    'septoria-leaf-spot': 'Septoria Leaf Spot',
    'bacterial-spot': 'Bacterial Spot',
    'tomato-mosaic-virus': 'Tomato Mosaic Virus',
    'physiological-leaf-curl': 'Physiological Leaf Curl'
}

def map_cnn_to_kb(cnn_class_name):
    """Map CNN model class name to knowledge base slug."""
    return CNN_TO_KB_MAPPING.get(cnn_class_name)

def get_human_readable_name(kb_slug):
    """Get human-readable disease name from knowledge base slug."""
    return KB_TO_HUMAN.get(kb_slug, kb_slug.replace('-', ' ').title())

def is_disease_in_knowledge_base(cnn_class_name):
    """Check if a CNN-detected disease exists in the knowledge base."""
    kb_slug = map_cnn_to_kb(cnn_class_name)
    return kb_slug is not None

def format_cnn_prediction_for_prompt(cnn_class_name, confidence):
    """
    Format CNN prediction for injection into RAG prompt.
    Returns None if disease not in knowledge base.
    """
    kb_slug = map_cnn_to_kb(cnn_class_name)
    if not kb_slug:
        return None
    
    human_name = get_human_readable_name(kb_slug)
    return f"Computer vision analysis suggests: {human_name} (confidence: {confidence}%)."
