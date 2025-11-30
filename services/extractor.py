"""
Module 2: Text Extraction & Cleaning Service
Extracts text from PDF, DOCX, Images, and TXT files
"""

import pdfplumber
from docx import Document
from PIL import Image
import pytesseract
import os
import re


def extract_text_from_pdf(file_path):
    """
    Extract text from PDF using pdfplumber
    Args:
        file_path: Path to PDF file
    Returns:
        Extracted text as string
    """
    text_parts = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return '\n'.join(text_parts)
    except Exception as e:
        raise Exception(f"PDF extraction error: {str(e)}")


def extract_text_from_docx(file_path):
    """
    Extract text from Word document using python-docx
    Args:
        file_path: Path to DOCX file
    Returns:
        Extracted text as string
    """
    try:
        doc = Document(file_path)
        paragraphs = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
        return '\n'.join(paragraphs)
    except Exception as e:
        raise Exception(f"DOCX extraction error: {str(e)}")


def extract_text_from_image(file_path):
    """
    Extract text from image using pytesseract OCR
    Args:
        file_path: Path to image file
    Returns:
        Extracted text as string
    """
    try:
        img = Image.open(file_path)
        # Use pytesseract for OCR
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        raise Exception(f"OCR extraction error: {str(e)}")


def extract_text_from_txt(file_path):
    """
    Extract text from plain text file
    Args:
        file_path: Path to TXT file
    Returns:
        File contents as string
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except Exception as e:
        raise Exception(f"TXT file read error: {str(e)}")


def extract_text_from_file(file_path):
    """
    Main extraction function - detects file type and extracts text
    Args:
        file_path: Path to file
    Returns:
        Extracted text as string
    """
    filename_lower = file_path.lower()

    # PDF files
    if filename_lower.endswith('.pdf'):
        return extract_text_from_pdf(file_path)

    # Word documents
    elif filename_lower.endswith('.docx'):
        return extract_text_from_docx(file_path)

    # Image files (OCR)
    elif filename_lower.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
        return extract_text_from_image(file_path)

    # Plain text files
    elif filename_lower.endswith('.txt'):
        return extract_text_from_txt(file_path)

    # Fallback: try to read as text
    else:
        try:
            return extract_text_from_txt(file_path)
        except:
            raise Exception(f"Unsupported file type: {os.path.splitext(file_path)[1]}")


def clean_text(text):
    """
    Clean and normalize extracted text
    - Remove unwanted symbols and blank lines
    - Ensure proper spacing and UTF-8 encoding

    Args:
        text: Raw extracted text
    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Normalize line endings (Windows/Mac/Unix)
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove excessive blank lines (more than 2 consecutive newlines)
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    # Remove control characters except newlines and tabs
    text = re.sub(r'[\x00-\x08\x0b-\x1f\x7f-\x9f]', '', text)

    # Remove excessive whitespace while preserving single spaces
    text = re.sub(r'[ \t]+', ' ', text)

    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    # Final strip
    text = text.strip()

    # Ensure UTF-8 encoding
    try:
        text = text.encode('utf-8', errors='replace').decode('utf-8')
    except:
        pass

    return text