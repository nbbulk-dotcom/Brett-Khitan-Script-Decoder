"""
Model Refinement Module for Khitan Large Script Decoder
Iteratively refines glyph database with new data and confidence updates.
"""

from typing import Dict, List
import json


def refine(new_data: List[Dict], current_glyphs: Dict) -> Dict:
    """
    Refine glyph database with new data.
    
    Args:
        new_data: List of new glyph entries
        current_glyphs: Current glyph database
        
    Returns:
        Updated glyph database with version info
    """
    updated = current_glyphs.copy()
    added = 0
    modified = 0
    
    for entry in new_data:
        codepoint = entry.get('codepoint')
        
        if not codepoint:
            continue
        
        if codepoint not in updated:
            updated[codepoint] = entry
            added += 1
        else:
            existing = updated[codepoint]
            
            if entry.get('confidence', 0) > 0:
                avg_confidence = (
                    existing.get('confidence', 0) + entry.get('confidence', 0)
                ) / 2
                existing['confidence'] = avg_confidence
                
                if entry.get('phonetic'):
                    existing['phonetic'] = entry['phonetic']
                
                if entry.get('semantic'):
                    existing['semantic'] = entry['semantic']
                
                modified += 1
    
    return {
        'updated_glyphs': updated,
        'stats': {
            'added': added,
            'modified': modified,
            'total': len(updated)
        },
        'version': '2.2'
    }


def merge_phonetic_variants(glyphs: Dict) -> Dict:
    """
    Merge phonetic variants for same codepoint.
    
    Args:
        glyphs: Glyph database
        
    Returns:
        Merged database
    """
    merged = {}
    
    for codepoint, data in glyphs.items():
        phonetic = data.get('phonetic')
        
        if isinstance(phonetic, list):
            data['phonetic'] = ' / '.join(phonetic)
            data['notes'] = data.get('notes', '') + ' [variant readings merged]'
        
        merged[codepoint] = data
    
    return merged


def update_confidence_scores(glyphs: Dict, validation_results: Dict) -> Dict:
    """
    Update confidence scores based on validation results.
    
    Args:
        glyphs: Glyph database
        validation_results: Validation metrics
        
    Returns:
        Updated glyph database
    """
    fit_factor = validation_results.get('fit', 1.0)
    consistency_factor = validation_results.get('consistency', 1.0)
    
    updated = {}
    
    for codepoint, data in glyphs.items():
        current_conf = data.get('confidence', 0)
        
        adjusted_conf = current_conf * fit_factor * consistency_factor
        adjusted_conf = max(0.0, min(1.0, adjusted_conf))
        
        data['confidence'] = adjusted_conf
        updated[codepoint] = data
    
    return updated


def export_refinements(glyphs: Dict, filepath: str):
    """
    Export refined glyph database to JSON.
    
    Args:
        glyphs: Refined glyph database
        filepath: Output file path
    """
    glyph_list = [
        {**data, 'codepoint': cp}
        for cp, data in glyphs.items()
    ]
    
    output = {
        'glyphs': glyph_list,
        'metadata': {
            'version': '2.2',
            'total_glyphs': len(glyph_list),
            'refined': True
        }
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
