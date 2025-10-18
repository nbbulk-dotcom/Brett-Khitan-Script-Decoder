#!/usr/bin/env python3
"""
Brett Sound Simulator - Khitan Large Script
============================================
Generates audio files that emulate the estimated tone, intonation, and voice 
inflections for Khitan Large Script using the Brett Method.

Created by: Nicolas of the Family Brett
Date: October 18, 2025
License: MIT
"""

import numpy as np
from scipy.io import wavfile
import pandas as pd
import os
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
import argparse

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("Warning: pydub not available. Install with: pip install pydub")

@dataclass
class VoiceProfile:
    """Voice profile configuration"""
    type: str  # 'male', 'female', 'child'
    pitch: float  # Hz
    rate: int  # Words per minute
    description: str

@dataclass
class PhonemeData:
    """Phoneme data structure"""
    glyph: str
    ipa: str
    pitch: float
    duration: float
    stress: str

class KhitanSoundSimulator:
    """Sound simulator for Khitan Large Script"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.voice_profiles = {
            'male': VoiceProfile('male', 100, 130, 'Authoritative hierarchical tone'),
            'female': VoiceProfile('female', 200, 140, 'Administrative clarity'),
            'child': VoiceProfile('child', 280, 180, 'Communal tone')
        }
        self.base_freq = 392  # Para-Mongolic G4
        
    def load_phoneme_map(self, file_path: str) -> Dict[str, PhonemeData]:
        """Load phoneme-to-IPA mapping"""
        if not os.path.exists(file_path):
            return self._create_default_phoneme_map()
        
        df = pd.read_csv(file_path)
        phoneme_map = {}
        for _, row in df.iterrows():
            phoneme_map[row['glyph']] = PhonemeData(
                glyph=row['glyph'],
                ipa=row['ipa'],
                pitch=row['pitch'],
                duration=row['duration'],
                stress=row['stress']
            )
        return phoneme_map
    
    def _create_default_phoneme_map(self) -> Dict[str, PhonemeData]:
        """Create default phoneme mappings for Khitan"""
        default_phonemes = {
            'ɣuɑŋ': PhonemeData('ɣuɑŋ', 'ɣuɑŋ', 880.00, 0.6, 'primary'),
            'ti': PhonemeData('ti', 'ti', 659.26, 0.4, 'secondary'),
            'kim': PhonemeData('kim', 'kim', 587.33, 0.5, 'primary'),
            'tɑi': PhonemeData('tɑi', 'tɑi', 523.25, 0.5, 'primary'),
            'siɑŋ': PhonemeData('siɑŋ', 'siɑŋ', 493.88, 0.5, 'primary'),
            'kun': PhonemeData('kun', 'kun', 440.00, 0.5, 'primary'),
            'yelü': PhonemeData('yelü', 'jɛ.lu', 392.00, 0.6, 'primary'),
            'kwe': PhonemeData('kwe', 'kʷɛ', 349.23, 0.4, 'secondary'),
            'vadis': PhonemeData('vadis', 'və.dis', 329.63, 0.5, 'primary'),
            'xiao': PhonemeData('xiao', 'ɕiɑu', 293.66, 0.5, 'primary')
        }
        return default_phonemes
    
    def generate_tone(self, freq: float, duration: float) -> np.ndarray:
        """Generate sine wave for phoneme"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        tone = np.sin(2 * np.pi * freq * t)
        
        # Apply envelope
        envelope = np.ones_like(tone)
        fade_samples = int(0.01 * self.sample_rate)
        if len(tone) > 2 * fade_samples:
            envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
            envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        return tone * envelope
    
    def apply_declarative_intonation(self, audio: np.ndarray, stress: str) -> np.ndarray:
        """Apply declarative intonation for governance texts"""
        samples = len(audio)
        
        if stress == 'primary':
            # Steady with slight fall for authority
            curve = np.linspace(1.0, 0.85, samples)
        elif stress == 'secondary':
            # Neutral for secondary stress
            curve = np.linspace(0.95, 0.90, samples)
        else:
            # Flat for unstressed
            curve = np.ones(samples) * 0.9
        
        return audio * curve
    
    def synthesize_phrase(self, text: str, voice_type: str = 'female', 
                         phoneme_map: Optional[Dict] = None) -> np.ndarray:
        """Synthesize a phrase into audio"""
        if phoneme_map is None:
            phoneme_map = self._create_default_phoneme_map()
        
        audio_segments = []
        words = text.replace('-', ' ').split()
        
        for word in words:
            if word in phoneme_map:
                phoneme = phoneme_map[word]
                
                # Generate tone
                tone = self.generate_tone(phoneme.pitch, phoneme.duration)
                
                # Apply declarative intonation
                tone = self.apply_declarative_intonation(tone, phoneme.stress)
                
                # Adjust for voice profile
                voice = self.voice_profiles[voice_type]
                pitch_factor = voice.pitch / 200  # Normalize to female baseline
                tone = self._adjust_pitch(tone, pitch_factor)
                
                audio_segments.append(tone)
                
                # Add brief silence
                silence = np.zeros(int(0.12 * self.sample_rate))
                audio_segments.append(silence)
        
        if audio_segments:
            combined = np.concatenate(audio_segments)
            max_val = np.max(np.abs(combined))
            if max_val > 0:
                combined = combined / max_val * 0.8
            return combined
        return np.array([])
    
    def _adjust_pitch(self, audio: np.ndarray, factor: float) -> np.ndarray:
        """Adjust pitch by resampling"""
        if factor == 1.0:
            return audio
        
        indices = np.arange(0, len(audio), factor)
        indices = indices[indices < len(audio)].astype(int)
        return audio[indices]
    
    def save_wav(self, audio: np.ndarray, output_path: str):
        """Save audio as WAV file"""
        audio_int = (audio * 32767).astype(np.int16)
        wavfile.write(output_path, self.sample_rate, audio_int)
        print(f"Saved audio to: {output_path}")
    
    def process_inscription(self, inscription_id: str, output_dir: str = 'audio_output'):
        """Process a decoded inscription into audio"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Example inscriptions
        inscriptions = {
            'yelu_yanning': {
                'text': 'ɣuɑŋ ti kim tɑi siɑŋ kun',
                'voice': 'male',
                'context': 'Imperial epitaph (1134 CE)'
            },
            'xiao_xiaozhong': {
                'text': 'yelü kwe vadis',
                'voice': 'female',
                'context': 'Administrative record (1091 CE)'
            }
        }
        
        if inscription_id not in inscriptions:
            print(f"Inscription {inscription_id} not found")
            return
        
        insc = inscriptions[inscription_id]
        print(f"Processing {inscription_id}: {insc['text']}")
        print(f"Context: {insc['context']}")
        print(f"Voice: {insc['voice']}")
        
        audio = self.synthesize_phrase(insc['text'], insc['voice'])
        output_path = os.path.join(output_dir, f"{inscription_id}_khitan.wav")
        self.save_wav(audio, output_path)
        
        return output_path

def main():
    parser = argparse.ArgumentParser(
        description='Brett Sound Simulator for Khitan Large Script'
    )
    parser.add_argument('--inscription', '-i', help='Inscription ID')
    parser.add_argument('--text', '-t', help='Custom text to synthesize')
    parser.add_argument('--voice', '-v', choices=['male', 'female', 'child'], 
                       default='female', help='Voice profile')
    parser.add_argument('--output', '-o', default='audio_output', 
                       help='Output directory')
    parser.add_argument('--phoneme-map', '-p', help='Path to phoneme CSV file')
    
    args = parser.parse_args()
    
    simulator = KhitanSoundSimulator()
    
    if args.inscription:
        simulator.process_inscription(args.inscription, args.output)
    elif args.text:
        os.makedirs(args.output, exist_ok=True)
        
        phoneme_map = None
        if args.phoneme_map:
            phoneme_map = simulator.load_phoneme_map(args.phoneme_map)
        
        print(f"Synthesizing: {args.text}")
        print(f"Voice: {args.voice}")
        
        audio = simulator.synthesize_phrase(args.text, args.voice, phoneme_map)
        output_path = os.path.join(args.output, f"custom_khitan.wav")
        simulator.save_wav(audio, output_path)
    else:
        print("Processing all available inscriptions...")
        for insc_id in ['yelu_yanning', 'xiao_xiaozhong']:
            simulator.process_inscription(insc_id, args.output)

if __name__ == "__main__":
    main()
