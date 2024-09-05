"""Directive to include a list of contributors from a JSON file."""

import json
from pathlib import Path

from docutils import nodes  # type: ignore[import-untyped]
from docutils.parsers.rst import Directive  # type: ignore[import-untyped]


class AllContributorsDirective(Directive):  # type: ignore[misc]
    """Directive to include a list of contributors from a JSON file."""

    # Allow one optional argument for the relative path
    required_arguments = 0
    optional_arguments = 1
    has_content = False

    def run(self) -> list[nodes.Node]:
        """Return a list of nodes to insert into the document."""
        env = self.state.document.settings.env
        srcdir = Path(env.srcdir)

        # Get the path from the argument or default to .all-contributorsrc
        relative_path = self.arguments[0] if self.arguments else ".all-contributorsrc"
        contributors_file = srcdir / relative_path

        if not Path(contributors_file).exists():
            return [
                nodes.error(
                    None,
                    nodes.paragraph(text=f"Error: {relative_path} file not found."),
                ),
            ]

        with Path(contributors_file).open(encoding="utf-8") as f:
            all_contributors = json.load(f)

        contributors_list = []

        for contributor in all_contributors.get("contributors", []):
            name = contributor.get("name", "Unknown Contributor")
            contributions = ", ".join(contributor.get("contributions", []))
            contributors_list.append(f"- {name} {contributions}")

        # Join the list items with newlines
        content = "\n".join(contributors_list)

        # Create a paragraph node containing the content
        paragraph_node = nodes.paragraph(text=content)
        return [paragraph_node]
