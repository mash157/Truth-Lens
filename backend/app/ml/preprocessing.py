import re
import html


def clean_text(text: str) -> str:
    """
    Cleans input text by:
    - Handling non-string inputs
    - Decoding HTML entities (&amp; -> &, &nbsp; -> space, etc.)
    - Stripping HTML tags
    - Normalizing whitespace
    - Lowercasing
    """
    if not isinstance(text, str):
        return ""
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Lowercase
    text = text.lower()
    
    # Strip HTML tags
    text = re.sub(r"<[^>]*>", "", text)
    
    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()
    
    return text


def combine_headline_and_body(title: str, text: str) -> str:
    """
    Combines headline and text for model input.
    """
    title_clean = clean_text(title)
    text_clean = clean_text(text)
    
    if title_clean and text_clean:
        return f"{title_clean} . {text_clean}"
    elif title_clean:
        return title_clean
    else:
        return text_clean
