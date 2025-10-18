# Brett Sound Simulator - Khitan Large Script

## Overview

The Brett Sound Simulator generates audio files that emulate the estimated tone, intonation, and voice inflections for Khitan Large Script using the Brett Method. This tool brings the voices of the Liao Dynasty (907-1125 CE) to life through frequency-based harmonic analysis and Para-Mongolic prosody.

## Features

- **Declarative Intonation**: Steady with slight fall for governance texts
- **Voice Profiles**: Male (hierarchical), Female (administrative), Child (communal)
- **Phoneme Accuracy**: IPA-based mappings with Para-Mongolic reconstructions
- **Frequency Analysis**: Brett Method harmonic frequencies (293-880 Hz range)
- **WAV Output**: High-quality 44.1 kHz, 16-bit PCM audio files

## Installation

### Prerequisites

```bash
# Required Python packages
pip install numpy scipy pandas

# Optional (for advanced audio processing)
pip install pydub
```

### System Requirements

- Python 3.8+
- 4GB+ RAM recommended
- Speakers or headphones for audio playback

## Usage

### Basic Usage

```bash
# Process a specific inscription
python brett_sound_simulator.py --inscription yelu_yanning

# Synthesize custom text
python brett_sound_simulator.py --text "ɣuɑŋ ti kim"

# Use different voice profile
python brett_sound_simulator.py --text "yelü kwe" --voice male

# Process all available inscriptions
python brett_sound_simulator.py
```

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--inscription` | `-i` | Inscription ID | None |
| `--text` | `-t` | Custom text to synthesize | None |
| `--voice` | `-v` | Voice profile (male/female/child) | female |
| `--output` | `-o` | Output directory | audio_output |
| `--phoneme-map` | `-p` | Path to custom phoneme CSV | Built-in |

### Examples

#### Example 1: Yelü Yanning Epitaph (1134 CE)

```bash
python brett_sound_simulator.py --inscription yelu_yanning
```

**Output**: `audio_output/yelu_yanning_khitan.wav`

**Context**: Imperial epitaph stele

**Reading**: "ɣuɑŋ-ti-kim-tɑi-siɑŋ-kun" (emperor sovereign gold great general)

**Voice**: Male (100 Hz, authoritative hierarchical)

#### Example 2: Administrative Record

```bash
python brett_sound_simulator.py --text "yelü kwe vadis" --voice female
```

**Output**: `audio_output/custom_khitan.wav`

**Context**: Administrative decree style

**Voice**: Female (200 Hz, administrative clarity)

#### Example 3: Custom Text

```bash
python brett_sound_simulator.py --text "xiao kim" --voice male
```

**Output**: `audio_output/custom_khitan.wav`

**Context**: Personal name or title

**Voice**: Male (100 Hz, formal tone)

## Phoneme Mapping

### Built-in Phonemes

The simulator includes default mappings for 10 Para-Mongolic phonemes:

| Glyph | IPA | Frequency (Hz) | Duration (s) | Stress | Context |
|-------|-----|----------------|--------------|--------|---------|
| ɣuɑŋ | ɣuɑŋ | 880.00 | 0.6 | primary | Emperor |
| ti | ti | 659.26 | 0.4 | secondary | Sovereign |
| kim | kim | 587.33 | 0.5 | primary | Gold |
| tɑi | tɑi | 523.25 | 0.5 | primary | Great |
| siɑŋ | siɑŋ | 493.88 | 0.5 | primary | General |
| kun | kun | 440.00 | 0.5 | primary | Lord |
| yelü | jɛ.lu | 392.00 | 0.6 | primary | Clan name |
| kwe | kʷɛ | 349.23 | 0.4 | secondary | Command |
| vadis | və.dis | 329.63 | 0.5 | primary | Decree |
| xiao | ɕiɑu | 293.66 | 0.5 | primary | Empress clan |

### Custom Phoneme Maps

Create a CSV file with the following format:

```csv
glyph,ipa,pitch,duration,stress
ɣuɑŋ,ɣuɑŋ,880.00,0.6,primary
ti,ti,659.26,0.4,secondary
```

**Columns**:
- `glyph`: Romanized form (e.g., "ɣuɑŋ", "ti")
- `ipa`: IPA transcription (e.g., "ɣuɑŋ", "ti")
- `pitch`: Frequency in Hz (Brett Method frequencies)
- `duration`: Seconds (0.4-0.6 typical)
- `stress`: 'primary', 'secondary', or 'none'

**Usage**:
```bash
python brett_sound_simulator.py --text "ɣuɑŋ ti" --phoneme-map data/custom_phonemes.csv
```

## Voice Profiles

### Male Voice (Hierarchical/Imperial)
- **Pitch**: 100 Hz (deep, authoritative)
- **Rate**: 130 words/minute
- **Context**: Imperial decrees, epitaphs, hierarchical texts
- **Intonation**: Steady with slight fall (declarative authority)
- **Example**: Yelü Yanning epitaph

### Female Voice (Administrative)
- **Pitch**: 200 Hz (mid-range, clear)
- **Rate**: 140 words/minute
- **Context**: Administrative records, governance documents
- **Intonation**: Steady for formal clarity
- **Example**: Bureaucratic records

### Child Voice (Communal)
- **Pitch**: 280 Hz (high, youthful)
- **Rate**: 180 words/minute
- **Context**: Communal texts, informal records
- **Intonation**: Melodic, expressive
- **Example**: Community records

## Intonation Patterns

### Declarative Intonation (Default)

The simulator applies Para-Mongolic declarative prosody:

1. **Primary Stress**: Steady with slight fall (1.0 → 0.85 amplitude)
   - Reflects authoritative governance style
   - Used for emphasized words

2. **Secondary Stress**: Neutral fall (0.95 → 0.90 amplitude)
   - Gentle decline for supporting words

3. **Unstressed**: Flat (0.9 amplitude)
   - Baseline pronunciation

## Technical Details

### Audio Specifications

- **Format**: WAV (Waveform Audio File Format)
- **Sample Rate**: 44,100 Hz (CD quality)
- **Bit Depth**: 16-bit PCM
- **Channels**: Mono
- **File Size**: ~1-5 MB per phrase

### Frequency Analysis

Based on the Brett Method:
- **Base Frequency**: 392 Hz (Para-Mongolic G4)
- **Range**: 293-880 Hz (Imperial tier)
- **Harmonic Relationships**: Aligned with Liao Dynasty hierarchy

### Signal Processing

1. **Tone Generation**: Pure sine waves at phoneme frequencies
2. **Envelope**: Fade in/out (10ms) to prevent clicks
3. **Intonation**: Amplitude modulation based on stress
4. **Pitch Adjustment**: Voice profile-specific resampling
5. **Normalization**: Peak limiting at 80% to prevent clipping

## Integration with Decoder

The sound simulator works seamlessly with the main decoder:

```python
from khitan_large_decoder import KhitanDecoder
from brett_sound_simulator import KhitanSoundSimulator

# Decode inscription
decoder = KhitanDecoder()
result = decoder.decode('yelu_yanning')

# Synthesize audio
simulator = KhitanSoundSimulator()
audio = simulator.synthesize_phrase(
    result['phonetics'],
    voice_type='male'
)
simulator.save_wav(audio, 'yelu_yanning_output.wav')
```

## Validation and Accuracy

### Linguistic Basis

- **Para-Mongolic Reconstruction**: Based on Liao Dynasty phonology
- **Kane 2009**: Cross-referenced with Khitan linguistic analysis
- **Liu/Liu 2004**: Aligned with glyph phonetic values
- **IPA Standards**: International Phonetic Alphabet compliance

### Quality Metrics

- **Phoneme Accuracy**: IPA-based transcription
- **Prosodic Fidelity**: Mongolic intonation patterns
- **Frequency Precision**: Brett Method harmonic analysis
- **Cultural Authenticity**: Context-appropriate voice profiles

## Troubleshooting

### Common Issues

**Issue**: No audio output
```bash
# Check if file was created
ls -lh audio_output/

# Verify audio file
file audio_output/yelu_yanning_khitan.wav
```

**Issue**: Audio sounds distorted
- Reduce amplitude by adjusting normalization factor
- Check sample rate compatibility

**Issue**: Missing phonemes
- Create custom phoneme map CSV
- Use `--phoneme-map` option

**Issue**: Import errors
```bash
# Install missing dependencies
pip install numpy scipy pandas
```

## Advanced Usage

### Batch Processing

Process multiple inscriptions:

```python
from brett_sound_simulator import KhitanSoundSimulator

simulator = KhitanSoundSimulator()

inscriptions = ['yelu_yanning', 'xiao_xiaozhong']
for insc_id in inscriptions:
    simulator.process_inscription(insc_id, 'batch_output')
```

### Custom Voice Profiles

Modify voice characteristics:

```python
simulator = KhitanSoundSimulator()
simulator.voice_profiles['custom'] = VoiceProfile(
    type='custom',
    pitch=150,  # Hz
    rate=135,   # words/minute
    description='Custom voice'
)
```

## Research and Validation

### Methodology

The sound simulator is based on:

1. **Brett Method**: Frequency-based harmonic analysis
2. **Para-Mongolic Prosody**: Liao Dynasty speech patterns
3. **Kane 2009**: Khitan phonological reconstruction
4. **Archaeological Context**: Site-specific semantic analysis

### References

- Kane, D. (2009). *The Kitan Language and Script*
- Liu, F. & Liu, J. (2004). *Khitan Large Script Dictionary*
- Wu, Y. & Janhunen, J. (2010). *New Materials on the Khitan Small Script*
- Brett, N. (2025). *Khitan Large Script Decoder v2.1*

## Contributing

To improve the sound simulator:

1. Add new phoneme mappings
2. Refine intonation patterns
3. Enhance voice profiles
4. Validate against linguistic benchmarks

Submit improvements via GitHub pull requests.

## License

MIT License - Free for academic and commercial use

## Citation

```bibtex
@software{brett2025khitan_sound,
  author = {Brett, Nicolas},
  title = {Brett Sound Simulator for Khitan Large Script},
  year = {2025},
  url = {https://github.com/nbbulk-dotcom/Brett-Khitan-Script-Decoder}
}
```

## Contact

- **GitHub**: [@nbbulk-dotcom](https://github.com/nbbulk-dotcom)
- **Email**: nbbulk@gmail.com
- **Twitter**: @nbbulk

---

**Last Updated**: October 18, 2025

**Version**: 1.0

**Status**: Production Ready
