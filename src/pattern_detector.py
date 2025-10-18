"""
Pattern Detector Module for Khitan Large Script Decoder
Detects formulas, repeated patterns, and clusters using KMeans.
"""

from typing import Dict, List, Tuple
try:
    from sklearn.cluster import KMeans
    import numpy as np
except ImportError:
    KMeans = None
    np = None


def detect_patterns(segments: List[Dict], patterns: Dict) -> Dict:
    """
    Detect known patterns and formulas in segments.
    
    Args:
        segments: Segments with glyph data
        patterns: Pattern catalog
        
    Returns:
        Detected patterns with counts and meanings
    """
    detected = {}
    codepoints = [s['codepoint'] for s in segments]
    
    for pattern_name, pattern_data in patterns.items():
        pattern_glyphs = pattern_data['glyphs']
        count = 0
        positions = []
        
        for i in range(len(codepoints) - len(pattern_glyphs) + 1):
            if codepoints[i:i+len(pattern_glyphs)] == pattern_glyphs:
                count += 1
                positions.append(i)
        
        if count > 0:
            detected[pattern_name] = {
                'count': count,
                'positions': positions,
                'meaning': pattern_data['meaning'],
                'frequency': pattern_data['frequency']
            }
    
    return detected


def cluster_glyphs(segments: List[Dict], n_clusters: int = 3) -> Dict:
    """
    Cluster glyphs based on confidence scores using KMeans.
    
    Args:
        segments: Segments with confidence scores
        n_clusters: Number of clusters
        
    Returns:
        Cluster assignments and statistics
    """
    if not KMeans or not np or len(segments) < n_clusters:
        return {'clusters': [], 'error': 'Clustering unavailable'}
    
    try:
        confidences = np.array([[s['confidence']] for s in segments])
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(confidences)
        
        cluster_stats = {}
        for i in range(n_clusters):
            cluster_indices = [j for j, label in enumerate(labels) if label == i]
            cluster_confs = [segments[j]['confidence'] for j in cluster_indices]
            
            cluster_stats[f'cluster_{i}'] = {
                'size': len(cluster_indices),
                'mean_confidence': float(np.mean(cluster_confs)),
                'indices': cluster_indices
            }
        
        return {
            'labels': labels.tolist(),
            'n_clusters': n_clusters,
            'stats': cluster_stats
        }
    
    except Exception as e:
        return {'clusters': [], 'error': str(e)}


def find_repetitions(segments: List[Dict], min_length: int = 2) -> List[Dict]:
    """
    Find repeated sequences in segments.
    
    Args:
        segments: Segments to analyze
        min_length: Minimum repetition length
        
    Returns:
        List of repeated patterns
    """
    codepoints = [s['codepoint'] for s in segments]
    repetitions = []
    
    for length in range(min_length, len(codepoints) // 2 + 1):
        for i in range(len(codepoints) - length + 1):
            pattern = codepoints[i:i+length]
            
            count = 0
            positions = []
            for j in range(len(codepoints) - length + 1):
                if codepoints[j:j+length] == pattern:
                    count += 1
                    positions.append(j)
            
            if count > 1:
                repetitions.append({
                    'pattern': pattern,
                    'length': length,
                    'count': count,
                    'positions': positions
                })
    
    repetitions.sort(key=lambda x: x['count'] * x['length'], reverse=True)
    
    return repetitions[:10]
