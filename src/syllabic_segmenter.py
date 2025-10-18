"""
Syllabic Segmenter Module for Khitan Large Script Decoder
Segments lines into syllables based on CV patterns and probabilities.
"""

from typing import Dict, List, Tuple


def segment_syllables(line: List[str], probs: Dict) -> List[Dict]:
    """
    Segment line into syllables based on CV probabilities.
    
    Args:
        line: List of glyph codepoints
        probs: Syllable type probabilities (CV, V, CVC)
        
    Returns:
        List of syllable segments with probabilities
    """
    segments = []
    i = 0
    
    while i < len(line):
        if i + 1 < len(line):
            seg = {
                'type': 'CV',
                'glyphs': [line[i], line[i+1]],
                'prob': probs.get('CV', 0.75)
            }
            i += 2
        else:
            seg = {
                'type': 'V',
                'glyphs': [line[i]],
                'prob': probs.get('V', 0.15)
            }
            i += 1
        
        segments.append(seg)
    
    return segments


def detect_boundaries(segments: List[Dict], threshold: float = 0.5) -> List[int]:
    """
    Detect word boundaries based on syllable probabilities.
    
    Args:
        segments: Syllable segments
        threshold: Probability threshold for boundary detection
        
    Returns:
        List of boundary indices
    """
    boundaries = []
    
    for i, seg in enumerate(segments):
        if seg.get('prob', 0) < threshold:
            boundaries.append(i)
    
    return boundaries


def analyze_transitions(segments: List[Dict]) -> Dict:
    """
    Analyze syllable transitions.
    
    Args:
        segments: Syllable segments
        
    Returns:
        Transition statistics
    """
    transitions = []
    
    for i in range(len(segments) - 1):
        current = segments[i]['type']
        next_seg = segments[i + 1]['type']
        transitions.append(f"{current}->{next_seg}")
    
    transition_counts = {}
    for trans in transitions:
        transition_counts[trans] = transition_counts.get(trans, 0) + 1
    
    return {
        'transitions': transition_counts,
        'total': len(transitions),
        'unique': len(transition_counts)
    }
