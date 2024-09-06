"""Sphinx extension for All Contributors."""

from sphinx.application import Sphinx

from .directive import AllContributorsDirective


def setup(app: Sphinx) -> dict[str, str | bool]:
    """Set up the extension."""
    app.add_directive("all-contributors", AllContributorsDirective)
    return {
        "version": "0.1.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
