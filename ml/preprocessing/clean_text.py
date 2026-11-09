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
    
    Avoids overly aggressive preprocessing to preserve useful
    linguistic information for TF-IDF feature extraction.
    """
    if not isinstance(text, str):
        return ""
    
    # Decode HTML entities (e.g., &amp; -> &, &nbsp; -> space, &#39; -> ')
    text = html.unescape(text)
    
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
    Uses a separator to distinguish title from body content.
    """
    title_clean = clean_text(title)
    text_clean = clean_text(text)
    
    if title_clean and text_clean:
        return f"{title_clean} . {text_clean}"
    elif title_clean:
        return title_clean
    else:
        return text_clean
