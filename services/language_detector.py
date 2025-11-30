"""
Module 3: Language Detection & Preprocessing Service
Detects language and preprocesses text for TTS
"""

from langdetect import detect, LangDetectException
import re


def detect_language(text):
    """
    Auto-detect text language using langdetect
    Args:
        text: Input text
    Returns:
        Language code ('en', 'ur', etc.) or None if detection fails
    """
    if not text or len(text.strip()) < 3:
        return None

    try:
        detected = detect(text)

        # Map detected language to supported TTS languages
        # Group similar languages
        if detected in ['ur', 'ar', 'fa']:  # Urdu, Arabic, Persian
            return 'ur'
        elif detected in ['en']:
            return 'en'
        elif detected in ['es']:
            return 'es'
        elif detected in ['fr']:
            return 'fr'
        else:
            # Default to English for unsupported languages
            return 'en'

    except LangDetectException:
        # If detection fails, return None (will fallback to manual selection)
        return None


def preprocess_text(text, language='en'):
    """
    Preprocess text for TTS generation
    - Remove unwanted characters based on language
    - Normalize spacing
    - Split long paragraphs if needed

    Args:
        text: Input text
        language: Target language code
    Returns:
        Preprocessed text ready for TTS
    """
    if not text:
        return ""

    # Keep original text structure for better TTS
    # Don't convert to lowercase - TTS works better with proper casing

    if language == 'ur':
        # For Urdu: Keep Urdu characters, punctuation, and numbers
        # Remove Latin characters if mixed content
        text = re.sub(r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\s\d.,!?;:\-]', '', text)
    else:
        # For English and other Latin-based languages
        # Keep alphanumeric, basic punctuation, and common symbols
        text = re.sub(r'[^\w\s.,!?;:\-\'"()]', ' ', text)

    # Normalize multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # Normalize punctuation spacing
    text = re.sub(r'\s*([.,!?;:])\s*', r'\1 ', text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def split_text_into_chunks(text, max_chunk_size=500):
    """
    Split long text into smaller chunks for processing
    Useful for reducing TTS latency and handling long documents

    Args:
        text: Input text
        max_chunk_size: Maximum characters per chunk
    Returns:
        List of text chunks
    """
    if len(text) <= max_chunk_size:
        return [text]

    # Split by sentences (. ! ?)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If adding this sentence exceeds limit, save current chunk
        if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence if current_chunk else sentence

    # Add remaining text
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def normalize_text_for_tts(text, language='en'):
    """
    Additional normalization specifically for TTS quality
    Args:
        text: Input text
        language: Language code
    Returns:
        TTS-optimized text
    """
    # Expand common abbreviations for better pronunciation
    abbreviations = {
        'Mr.': 'Mister',
        'Mrs.': 'Misses',
        'Dr.': 'Doctor',
        'etc.': 'etcetera',
        'e.g.': 'for example',
        'i.e.': 'that is',
    }

    for abbr, full in abbreviations.items():
        text = text.replace(abbr, full)

    # Remove URLs (they don't speak well)
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # Normalize numbers (optional - comment out if you want numbers as-is)
    # text = re.sub(r'\b\d+\b', lambda m: num2words(int(m.group())), text)

    return text.strip()