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
