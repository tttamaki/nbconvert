"""LaTeX Exporter with Minted highlighting"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os

from traitlets import default

from nbconvert.filters.highlight_minted import Highlight2LatexMinted
from nbconvert.filters.markdown_minted import apply_minted_filter
from nbconvert.filters.pandoc import ConvertExplicitlyRelativePaths

from .latex import LatexExporter


class LatexMintedExporter(LatexExporter):
    """
    Exports to a LaTeX template with minted package for syntax highlighting.
    Designed for Python code highlighting only.
    """

    export_from_notebook = "LaTeX (Minted)"

    @default("template_name")
    def _template_name_default(self):
        return "latex_minted"

    def from_notebook_node(self, nb, resources=None, **kw):
        """Convert from notebook node with minted highlighting."""
        # Register our custom minted highlight filter (no pygments)
        highlight_code = Highlight2LatexMinted(parent=self)
        self.register_filter("highlight_code", highlight_code)

        # Register minted filter for markdown code blocks
        self.register_filter("apply_minted_filter", apply_minted_filter)

        # Need to handle explicit relative paths like parent does
        nb_path = resources.get("metadata", {}).get(
            "path") if resources else None
        texinputs = os.path.abspath(nb_path) if nb_path else os.getcwd()
        convert_explicitly_relative_paths = self.filters.get(
            "convert_explicitly_relative_paths",
            ConvertExplicitlyRelativePaths(texinputs=texinputs, parent=self),
        )
        self.register_filter("convert_explicitly_relative_paths",
                             convert_explicitly_relative_paths)

        # Call grandparent to avoid LatexExporter's highlight_code registration
        from .templateexporter import TemplateExporter
        return TemplateExporter.from_notebook_node(self, nb, resources, **kw)
