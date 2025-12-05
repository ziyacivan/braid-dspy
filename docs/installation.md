# Installation

## Requirements

- Python >= 3.9
- dspy-ai >= 2.0.0

## Install from PyPI

```bash
pip install braid-dspy
```

## Install from Source

```bash
git clone https://github.com/yourusername/braid-py.git
cd braid-py
pip install -e .
```

## Install with Development Dependencies

```bash
pip install -e ".[dev]"
```

## Verify Installation

```python
from braid import BraidReasoning
print("BRAID-DSPy installed successfully!")
```

## Using with uv

If you're using `uv` as your package manager:

```bash
uv pip install braid-dspy
```

Or for development:

```bash
git clone https://github.com/yourusername/braid-py.git
cd braid-py
uv sync
```

