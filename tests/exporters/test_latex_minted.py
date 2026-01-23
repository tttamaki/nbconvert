"""Tests for LatexMintedExporter"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from nbconvert.exporters.latex_minted import LatexMintedExporter

from .base import ExportersTestsBase


class TestLatexMintedExporter(ExportersTestsBase):
    """Tests for LatexMintedExporter"""

    exporter_class = LatexMintedExporter

    def test_constructor(self):
        """Can a LatexMintedExporter be constructed?"""
        exporter = LatexMintedExporter()
        assert exporter is not None
        assert exporter.template_name == "latex_minted"

    def test_minted_package_included(self):
        """Does the output include minted package?"""
        exporter = LatexMintedExporter()
        output, resources = exporter.from_filename(
            self._get_notebook("notebook3.ipynb"))
        assert r"\usepackage{minted}" in output

    def test_no_pygments_definitions(self):
        """Does the output exclude pygments definitions?"""
        exporter = LatexMintedExporter()
        output, resources = exporter.from_filename(
            self._get_notebook("notebook3.ipynb"))
        assert r"\newcommand\PY" not in output
        assert "pygments_definitions" not in output

    def test_minted_environment_used(self):
        """Does the output use minted environment for code cells?"""
        exporter = LatexMintedExporter()
        output, resources = exporter.from_filename(
            self._get_notebook("notebook3.ipynb"))
        assert r"\begin{minted}" in output
        assert r"\end{minted}" in output
        # Check that code is not wrapped with \PY macros
        assert r"\PY{" not in output

    def test_markdown_code_blocks_use_minted(self):
        """Does the output use minted environment for markdown code blocks?"""
        from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

        # Create a notebook with markdown cells containing code blocks
        nb = new_notebook(cells=[
            new_markdown_cell("# Test\n\n```python\nprint('hello')\n```"),
            new_markdown_cell("Bash example:\n\n```bash\necho test\n```"),
            new_markdown_cell("No language:\n\n```\nplain text\n```"),
        ])

        exporter = LatexMintedExporter()
        output, resources = exporter.from_notebook_node(nb)

        # Check that markdown code blocks use minted environment
        assert r"\begin{minted}[breaklines]{python}" in output
        assert r"\begin{minted}[breaklines]{bash}" in output
        assert r"\begin{minted}[breaklines]{text}" in output

        # Check that Pandoc's Shaded/Highlighting environments are not used
        assert r"\begin{Shaded}" not in output
        assert r"\begin{Highlighting}" not in output

        # Check that Pygments token macros are not used in markdown code blocks
        assert r"\KeywordTok" not in output
        assert r"\StringTok" not in output
        assert r"\ControlFlowTok" not in output
        assert r"\NormalTok" not in output
