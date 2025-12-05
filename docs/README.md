# Building Documentation

## Local Build

To build the documentation locally:

```bash
# Install dependencies
pip install -e ".[docs]"

# Build HTML documentation
cd docs
make html

# View the documentation
open _build/html/index.html
```

## Read the Docs

This project is configured for Read the Docs. The configuration is in `.readthedocs.yaml`.

To set up on Read the Docs:

1. Go to https://readthedocs.org/
2. Import your repository
3. Read the Docs will automatically detect the `.readthedocs.yaml` file
4. Documentation will be built automatically on each commit

## Documentation Structure

- `index.md` - Main documentation page
- `installation.md` - Installation instructions
- `api/` - API reference (auto-generated from docstrings)
- `examples/` - Usage examples
- `integration.md` - Integration guide

## Writing Documentation

- Use Markdown (`.md`) files with MyST parser extensions
- API documentation is auto-generated from docstrings using Sphinx autodoc
- Code examples should be tested and working

