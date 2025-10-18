"""
Phonetics Mapper Module for Khitan Large Script Decoder
Maps glyphs to phonetic values with interpolation for undeciphered glyphs.
"""

from typing import Dict, List, Optional
from src.data_loader import load_glyphs, load_probs


class PhoneticMapper:
    """
    Maps Khitan glyphs to phonetic reconstructions.
    Handles undeciphered glyphs through contextual interpolation.
    """
    
    def __init__(self, glyphs_file: str = 'data/glyph_database.json', 
                 probs_file: str = 'data/phonetic_probabilities.json'):
        """
        Initialize phonetic mapper.
        
        Args:
            glyphs_file: Path to glyph database
            probs_file: Path to phonetic probabilities
        """
        self.glyphs = load_glyphs(glyphs_file)
        self.probs = load_probs(probs_file)
    
    def map_phonetics(self, segments: List[Dict]) -> List[Dict]:
        """
        Map phonetic values to segments.
        
        Args:
            segments: List of segment dictionaries
            
        Returns:
            Segments with phonetic mappings added
        """
        mapped = []
        
        for seg in segments:
            codepoint = seg['codepoint']
            glyph_data = self.glyphs.get(codepoint)
            
            if glyph_data:
                seg['phonetic'] = glyph_data.get('phonetic')
                seg['semantic'] = glyph_data.get('semantic', '[undeciphered]')
                seg['confidence'] = glyph_data.get('confidence', 0.0)
                seg['notes'] = glyph_data.get('notes', '')
                
                if seg['phonetic']:
                    seg['syllable_prob'] = self._get_syllable_prob(seg['phonetic'])
                else:
                    seg['syllable_prob'] = 0.0
            else:
                seg['phonetic'] = None
                seg['semantic'] = '[undeciphered]'
                seg['confidence'] = 0.0
                seg['syllable_prob'] = 0.0
                seg['notes'] = 'Not in database'
            
            mapped.append(seg)
        
        return mapped
    
    def _get_syllable_prob(self, phonetic: str) -> float:
        """
        Determine syllable probability based on phonetic structure.
        
        Args:
            phonetic: Phonetic transcription
            
        Returns:
            Probability score
        """
        if not phonetic:
            return 0.0
        
        vowels = set('aeiouɑəɛɔʊɪ')
        has_vowel = any(c in vowels for c in phonetic.lower())
        
        if not has_vowel:
            return self.probs.get('C', 0.05)
        
        if len(phonetic) == 1:
            return self.probs.get('V', 0.15)
        elif len(phonetic) == 2:
            return self.probs.get('CV', 0.75)
        else:
            return self.probs.get('CVC', 0.10)
    
    def interpolate_unknown(self, seg: Dict, context: List[Dict]) -> Dict:
        """
        Interpolate phonetic value for undeciphered glyph using context.
        
        Args:
            seg: Segment with unknown phonetic
            context: Surrounding segments for context
            
        Returns:
            Segment with interpolated phonetic
        """
        if seg.get('phonetic'):
            return seg
        
        known_neighbors = [
            s for s in context 
            if s.get('phonetic') and s['confidence'] > 0.5
        ]
        
        if known_neighbors:
            seg['phonetic'] = '[interpolated]'
            seg['confidence'] = 0.3
            seg['notes'] = 'Interpolated from context'
        else:
            seg['phonetic'] = '[unknown]'
            seg['confidence'] = 0.0
        
        return seg
    
    def get_phonetic_sequence(self, segments: List[Dict]) -> str:
        """
        Extract phonetic sequence from segments.
        
        Args:
            segments: List of mapped segments
            
        Returns:
            Space-separated phonetic sequence
        """
        phonetics = []
        
        for seg in segments:
            phonetic = seg.get('phonetic')
            if phonetic:
                phonetics.append(phonetic)
            else:
                phonetics.append('[?]')
        
        return ' '.join(phonetics)
