"""
Convert Pandoc CodeBlock to minted environment for LaTeX

This filter processes Pandoc's JSON AST to convert markdown code blocks
into LaTeX minted environments instead of the default Shaded/Highlighting
environments that use Pygments-style macros.
"""

from pandocfilters import RawBlock, walk

__all__ = ["apply_minted_filter"]


def convert_code_block_to_minted(key, value, fmt, meta):
    """
    Convert Pandoc CodeBlock to minted environment.

    This function is designed to be used with pandocfilters.walk.
    It processes CodeBlock nodes in Pandoc's JSON AST and converts them to
    raw LaTeX minted environments.

    Parameters
    ----------
    key : str
        The type of the Pandoc AST node
    value : list
        The value of the node
    fmt : str
        The target format (should be 'latex')
    meta : dict
        Metadata from the document

    Returns
    -------
    RawBlock or None
        Returns a RawBlock with minted environment if key is 'CodeBlock',
        otherwise returns None (no change)

    Notes
    -----
    - Code blocks with language specified are rendered with that language
    - Code blocks without language are rendered with 'text' as default
    - Inline code is not processed by this filter (remains as \\texttt{})
    - Unknown languages are passed as-is to minted for error handling
    """
    if key == "CodeBlock":
        # CodeBlock structure: [[ident, classes, keyvals], code]
        # classes[0] contains the language if specified
        [[ident, classes, keyvals], code] = value

        # Extract language from classes, default to 'text' if not specified
        language = classes[0] if classes else "text"

        # Generate minted environment
        # Note: Using breaklines option for automatic line wrapping
        minted_output = f"\\begin{{minted}}[breaklines]{{{language}}}\n{code}\n\\end{{minted}}"

        # Return as raw LaTeX block
        return RawBlock("latex", minted_output)

    # Return None for other node types (no change)
    return None


def apply_minted_filter(source):
    """
    Apply the minted filter to Pandoc JSON AST.

    This function is designed to be used as a Jinja2 filter in nbconvert templates.
    It takes a Pandoc JSON representation of a markdown document and applies
    the code block to minted conversion filter.

    Parameters
    ----------
    source : str
        Pandoc JSON representation (as string) of the document

    Returns
    -------
    str
        Modified Pandoc JSON with CodeBlocks converted to minted environments

    Examples
    --------
    In a Jinja2 template:
        ((( cell.source | convert_pandoc('markdown', 'json') |
            apply_minted_filter |
            convert_pandoc('json', 'latex') )))
    """
    import json

    # Parse the Pandoc JSON
    doc = json.loads(source)

    # Apply the filter using walk
    # walk will recursively traverse the document and apply the action
    doc = walk(doc, convert_code_block_to_minted, '', {})

    return json.dumps(doc)
