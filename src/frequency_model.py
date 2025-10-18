"""
Frequency Model Module for Khitan Large Script Decoder
Assigns frequency tiers and calculates acoustic signatures.
"""

import json
import os
from typing import Dict, List, Tuple
try:
    import numpy as np
except ImportError:
    np = None


class FrequencyModel:
    """
    Assigns frequency tiers to glyphs based on semantic context.
    Imperial (880-1000 Hz), Administrative (440-660 Hz), Daily (220-440 Hz).
    """
    
    def __init__(self, tiers_file: str = 'data/frequency_tiers.json'):
        """
        Initialize frequency model.
        
        Args:
            tiers_file: Path to frequency tiers JSON
        """
        if os.path.exists(tiers_file):
            with open(tiers_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tiers = data['tiers']
        else:
            self.tiers = {
                "imperial": {"low": 880, "high": 1000},
                "admin": {"low": 440, "high": 660},
                "daily": {"low": 220, "high": 440}
            }
    
    def assign_tiers(self, segments: List[Dict]) -> List[Dict]:
        """
        Assign frequency tiers to segments based on semantics.
        
        Args:
            segments: List of segments with semantic data
            
        Returns:
            Segments with tier and Hz assignments
        """
        for seg in segments:
            tier = self._determine_tier(seg.get('semantic', ''))
            tier_range = self.tiers[tier]
            
            seg['tier'] = tier
            seg['hz'] = (tier_range['low'] + tier_range['high']) / 2
            seg['hz_range'] = (tier_range['low'], tier_range['high'])
        
        return segments
    
    def _determine_tier(self, semantic: str) -> str:
        """
        Determine frequency tier from semantic content.
        
        Args:
            semantic: Semantic meaning
            
        Returns:
            Tier name (imperial/admin/daily)
        """
        semantic_lower = semantic.lower()
        
        imperial_keywords = ['emperor', 'sovereign', 'august', 'imperial', 'majesty']
        admin_keywords = ['general', 'governor', 'official', 'minister', 'degree', 'office']
        
        if any(kw in semantic_lower for kw in imperial_keywords):
            return 'imperial'
        elif any(kw in semantic_lower for kw in admin_keywords):
            return 'admin'
        else:
            return 'daily'
    
    def calculate_signature(self, segments: List[Dict]) -> Dict:
        """
        Calculate acoustic signature of inscription.
        
        Args:
            segments: Segments with Hz assignments
            
        Returns:
            Signature statistics
        """
        hzs = [s['hz'] for s in segments if 'hz' in s]
        
        if not hzs:
            return {'mean_hz': 0, 'std_hz': 0, 'range': (0, 0)}
        
        if np:
            signature = {
                'mean_hz': float(np.mean(hzs)),
                'std_hz': float(np.std(hzs)),
                'min_hz': float(np.min(hzs)),
                'max_hz': float(np.max(hzs)),
                'range': (float(np.min(hzs)), float(np.max(hzs)))
            }
        else:
            signature = {
                'mean_hz': sum(hzs) / len(hzs),
                'std_hz': 0,
                'min_hz': min(hzs),
                'max_hz': max(hzs),
                'range': (min(hzs), max(hzs))
            }
        
        return signature
