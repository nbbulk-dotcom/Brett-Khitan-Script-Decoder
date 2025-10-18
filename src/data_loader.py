"""
Data Loader Module for Khitan Large Script Decoder
Handles loading and normalization of glyphs, corpus, and probabilities.
"""

import json
import os
from typing import Dict, List, Tuple, Optional


def load_corpus(file_path: str = 'data/inscriptions_corpus.json') -> Dict:
    """
    Load inscriptions corpus from JSON file.
    
    Args:
        file_path: Path to corpus JSON file
        
    Returns:
        Dictionary of inscriptions with metadata
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Corpus file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['inscriptions']


def normalize_glyph(glyph):
    """
    Normalize glyph representation.
    Handles both single glyphs and stacked/compound glyphs.
    
    Args:
        glyph: Glyph codepoint or list of codepoints
        
    Returns:
        Normalized glyph representation
    """
    if isinstance(glyph, list):
        return tuple(sorted(glyph))
    return glyph


def load_glyphs(file_path: str = 'data/glyph_database.json') -> Dict:
    """
    Load glyph database from JSON file.
    
    Args:
        file_path: Path to glyph database JSON file
        
    Returns:
        Dictionary mapping codepoints to glyph data
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Glyph database not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return {entry['codepoint']: entry for entry in data['glyphs']}


def load_probs(file_path: str = 'data/phonetic_probabilities.json') -> Dict:
    """
    Load phonetic probabilities from JSON file.
    
    Args:
        file_path: Path to probabilities JSON file
        
    Returns:
        Dictionary of syllable type probabilities
    """
    if not os.path.exists(file_path):
        return {
            "CV": 0.75,
            "V": 0.15,
            "CVC": 0.10
        }
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_inscription(inscription: Dict) -> bool:
    """
    Validate inscription structure.
    
    Args:
        inscription: Inscription dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_keys = ['lines', 'metadata']
    
    if not all(key in inscription for key in required_keys):
        return False
    
    if not isinstance(inscription['lines'], list):
        return False
    
    if not isinstance(inscription['metadata'], dict):
        return False
    
    return True
