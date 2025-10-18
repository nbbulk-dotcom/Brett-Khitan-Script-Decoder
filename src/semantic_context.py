"""
Semantic Context Module for Khitan Large Script Decoder
Weights semantics based on inscription type and archaeological context.
"""

from typing import Dict, List


def weight_semantics(segments: List[Dict], metadata: Dict) -> Dict:
    """
    Apply semantic weights based on inscription context.
    
    Args:
        segments: Segments with semantic data
        metadata: Inscription metadata (type, date, location)
        
    Returns:
        Weighted segments and overall weight
    """
    weights = {
        'epitaph_stele': 0.90,
        'administrative': 0.85,
        'ritual': 0.88,
        'daily': 0.70
    }
    
    inscription_type = metadata.get('type', 'daily')
    weight = weights.get(inscription_type, 0.70)
    
    for seg in segments:
        seg['semantic_weight'] = weight * seg.get('confidence', 0.0)
        seg['context_type'] = inscription_type
    
    return {
        'segments': segments,
        'overall_weight': weight,
        'inscription_type': inscription_type
    }


def contextualize_meaning(semantic: str, context_type: str) -> str:
    """
    Contextualize semantic meaning based on inscription type.
    
    Args:
        semantic: Base semantic meaning
        context_type: Type of inscription
        
    Returns:
        Contextualized meaning
    """
    if context_type == 'epitaph_stele':
        if 'emperor' in semantic.lower():
            return f"{semantic} (honorific title)"
        elif 'father' in semantic.lower() or 'mother' in semantic.lower():
            return f"{semantic} (genealogical reference)"
    
    elif context_type == 'administrative':
        if 'governor' in semantic.lower() or 'official' in semantic.lower():
            return f"{semantic} (official title)"
    
    return semantic


def extract_semantic_fields(segments: List[Dict]) -> Dict:
    """
    Extract semantic fields from segments.
    
    Args:
        segments: Segments with semantic data
        
    Returns:
        Categorized semantic fields
    """
    fields = {
        'titles': [],
        'genealogy': [],
        'temporal': [],
        'locational': [],
        'other': []
    }
    
    for seg in segments:
        semantic = seg.get('semantic', '').lower()
        
        if any(kw in semantic for kw in ['emperor', 'sovereign', 'general', 'governor', 'official']):
            fields['titles'].append(seg)
        elif any(kw in semantic for kw in ['father', 'mother', 'son', 'child']):
            fields['genealogy'].append(seg)
        elif any(kw in semantic for kw in ['month', 'day', 'year', 'hundred']):
            fields['temporal'].append(seg)
        elif any(kw in semantic for kw in ['west', 'north', 'east', 'south', 'country']):
            fields['locational'].append(seg)
        else:
            fields['other'].append(seg)
    
    return fields
