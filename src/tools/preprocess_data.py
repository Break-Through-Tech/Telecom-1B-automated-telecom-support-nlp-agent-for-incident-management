import html
import re

from smolagents import tool

# Function to normalize text (lowercase, alphabetic characters & spaces only)
def normalize_text(text: str) -> str:
    upper_unicodes = range(65, 91)
    lower_unicodes = range(97, 123)
        
    result = ""
    for character in text:
        unicode = ord(character)
        if unicode in upper_unicodes or unicode in lower_unicodes or unicode == 32:
            result += character
    return result.lower()

@tool
def run_preprocess_and_training_pipeline(msg: str) -> str:
    """Cleans incoming customer inquiries so the model can use it to make predictions.

    Args:
        msg: customer inquiry to be cleaned.

    Returns: 
        The cleaned customer inquiry
    
    """
    # Remove @mentions
    msg = re.sub(r"@\w+", "", msg)

    # Remove URLs
    msg = re.sub(r"https?://\S+", "", msg)

    # Decode HTML entities
    msg = html.unescape(msg)

    # Normalize text
    msg = normalize_text(msg)

    return msg
