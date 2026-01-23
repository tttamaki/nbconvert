# LaTeX Minted Exporter

This is a custom nbconvert exporter that converts Jupyter notebooks to LaTeX using the `minted` package for syntax highlighting instead of Pygments' built-in LaTeX macros.

## Overview

The standard `LatexExporter` uses Pygments to generate LaTeX code with custom `\PY{...}` macros for syntax highlighting. The `LatexMintedExporter` delegates syntax highlighting to the LaTeX `minted` package, which also uses Pygments but at PDF compile time.

## Features

- Uses `minted` package for code highlighting
- Focuses on Python code (ipython/python3)
- Cleaner LaTeX output without Pygments macro definitions
- Maintains the same cell styling as the default LaTeX template

## Usage

### Python API

```python
from nbconvert.exporters import LatexMintedExporter

exporter = LatexMintedExporter()
(body, resources) = exporter.from_filename('notebook.ipynb')

with open('output.tex', 'w') as f:
    f.write(body)
```

### Command Line

```bash
jupyter nbconvert --to latex_minted notebook.ipynb
```

## Requirements

### For LaTeX Generation

- nbconvert
- traitlets

### For PDF Compilation

- A LaTeX distribution (e.g., TeX Live, MiKTeX)
- The `minted` package
- Python with Pygments installed (required by minted)
- The `-shell-escape` flag when compiling:

```bash
pdflatex -shell-escape output.tex
```

## Template Structure

The exporter uses a custom template hierarchy:

- `latex_minted/index.tex.j2` - Main template entry point
- `latex/index_minted.tex.j2` - Minted-specific index template
- `latex/style_minted.tex.j2` - Style template with minted environments
- `latex/base.tex.j2` - Base LaTeX template (inherited)

## Implementation Details

### Custom Highlighter

The `Highlight2LatexMinted` class in `nbconvert/filters/highlight_minted.py` returns unprocessed source code instead of applying Pygments formatting. This allows the `minted` package to handle syntax highlighting directly in LaTeX.

### Template Modifications

The `style_minted.tex.j2` template:

- Includes the `minted` package
- Defines a `draw_cell_minted` macro that wraps code in `\begin{minted}{python3}...\end{minted}`
- Uses the existing `draw_cell` macro for output cells
- Omits Pygments definitions that would normally be included

## Testing

Run the test suite:

```bash
pytest tests/exporters/test_latex_minted.py -v
```

## Limitations

- Currently optimized for Python code only
- Other languages will be treated as plain text
- Markdown cells still require pandoc for conversion
