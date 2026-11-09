import re

def clean_text(text: str) -> str:
    """
    Cleans input text by removing extra whitespaces, normalizing lowercase, 
    and retaining essential alphanumeric and punctuation features.
    """
    if not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Strip HTML tags
    text = re.sub(r"<[^>]*>", "", text)
    
    # Normalize whitespaces (convert tabs, newlines, multiple spaces to a single space)
    text = re.sub(r"\s+", " ", text).strip()
    
    return text

def combine_headline_and_body(title: str, text: str) -> str:
    """
    Combines the title and text of an article for feature extraction.
    """
    title_clean = clean_text(title)
    text_clean = clean_text(text)
    
    if title_clean and text_clean:
        return f"{title_clean} . {text_clean}"
    elif title_clean:
        return title_clean
    else:
        return text_clean
