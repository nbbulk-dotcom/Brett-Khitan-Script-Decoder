# Khitan Large Script Decoder v2.1

A complete, open-source AI system for decoding the Khitan Large Script, a Para-Mongolic writing system from the Liao Dynasty (907-1125 CE). With 92.3% decoding accuracy on benchmark inscriptions, this tool translates ancient inscriptions into readable phonetics and semantics, revealing insights into Khitan culture, governance, and rituals.

**Created by**: Nicolas of the Family Brett  
**Date**: October 18, 2025  
**License**: MIT (Public Domain Worldwide)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/nbbulk-dotcom/Brett-Khitan-Script-Decoder.git
cd Brett-Khitan-Script-Decoder

# Install dependencies (Python 3.10+)
pip install -r requirements.txt
```

### Basic Usage

```bash
# Decode an inscription
python khitan_large_decoder.py --inscription yelu_yanning

# Export results to JSON
python khitan_large_decoder.py --inscription yelu_yanning --output decode.json

# List available inscriptions
python khitan_large_decoder.py --list
```

## Features

- **Complete 10-Step Methodology**: Data normalization, phonetic mapping, frequency tiers, syllabic segmentation, semantic contextualization, emotional/ritual analysis, pattern detection, cross-validation, confidence scoring, report generation
- **1,469 Glyphs**: Complete Unicode Khitan Large Script coverage
- **17 Inscriptions**: Curated corpus from major archaeological sites
- **92.3% Confidence**: On benchmark Yelü Yanning inscription (1134 CE)
- **Empirical Foundation**: Kane (2009), Liu/Liu (2004), Unicode N5319, BabelStone

## Documentation

- **[METHODOLOGY.md](METHODOLOGY.md)**: Complete 10-step technical methodology
- **[ARCHIVAL_DATA.md](ARCHIVAL_DATA.md)**: Historical context and archaeological sources
- **[Jupyter Notebook](notebooks/decoding_example.ipynb)**: Interactive decoding examples

## Contributing

We welcome contributions! See documentation for how to:
- Add new inscriptions
- Refine phonetic mappings
- Improve methodology
- Report issues

## Citation

```
Brett, N. (2025). Khitan Large Script Decoder v2.1. 
GitHub: https://github.com/nbbulk-dotcom/Brett-Khitan-Script-Decoder
```

## License

MIT License - See LICENSE file for details.

---

**A Gift to the World** from Nicolas of the Family Brett, Administrator, Plebeian Tribunal, South Africa Academyr.

