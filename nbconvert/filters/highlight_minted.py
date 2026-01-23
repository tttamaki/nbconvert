"""
Module containing filter functions that use LaTeX minted package for highlighting.
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from nbconvert.utils.base import NbConvertBase

__all__ = ["Highlight2LatexMinted"]


class Highlight2LatexMinted(NbConvertBase):
    """Convert code to LaTeX using minted package for Python."""

    def __init__(self, **kwargs):
        """Initialize the converter."""
        super().__init__(**kwargs)

    def __call__(self, source, language=None, metadata=None, strip_verbatim=False):
        """
        Return unprocessed source code for minted package to handle.

        Parameters
        ----------
        source : str
            source of the cell to highlight
        language : str
            language to highlight the syntax of (only python is handled)
        metadata : NotebookNode cell metadata
            metadata of the cell to highlight
        strip_verbatim : bool
            ignored for minted (kept for compatibility)
        """
        if not source or len(source) == 0:
            return " "

        # Return source as-is, minted will handle the highlighting
        return source
