# String Utils Library - test

A simple Python utility library for string and text manipulation.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from stringutils import format_text, parse_options

# Format text with click-based styling
formatted = format_text("Hello World", bold=True)

# Parse command options
options = parse_options(["--verbose", "--output=file.txt"])
```

## Testing

```bash
pytest tests/
```

## Development

This project uses pinned dependencies for stability. Run tests before making changes.
