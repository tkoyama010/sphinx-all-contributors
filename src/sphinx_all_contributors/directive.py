"""Directive to include a list of contributors from a JSON file."""

import json
from pathlib import Path
from typing import ClassVar

from docutils import nodes  # type: ignore[import-untyped]
from docutils.parsers.rst import Directive, directives  # type: ignore[import-untyped]

# Standard emoji mapping for all-contributors contribution types
EMOJI_MAP = {
    "audio": "\U0001f50a",
    "a11y": "\u267f\ufe0f",
    "bug": "\U0001f41b",
    "blog": "\U0001f4dd",
    "business": "\U0001f4bc",
    "code": "\U0001f4bb",
    "content": "\U0001f58b",
    "data": "\U0001f523",
    "doc": "\U0001f4d6",
    "design": "\U0001f3a8",
    "example": "\U0001f4a1",
    "eventOrganizing": "\U0001f4cb",
    "financial": "\U0001f4b5",
    "fundingFinding": "\U0001f50d",
    "ideas": "\U0001f914",
    "infra": "\U0001f687",
    "maintenance": "\U0001f6a7",
    "mentoring": "\U0001f9d1\u200d\U0001f3eb",
    "platform": "\U0001f4e6",
    "plugin": "\U0001f50c",
    "projectManagement": "\U0001f4c6",
    "question": "\U0001f4ac",
    "research": "\U0001f52c",
    "review": "\U0001f440",
    "security": "\U0001f6e1\ufe0f",
    "tool": "\U0001f527",
    "translation": "\U0001f30d",
    "test": "\u26a0\ufe0f",
    "tutorial": "\u2705",
    "talk": "\U0001f4e2",
    "userTesting": "\U0001f4d3",
    "video": "\U0001f4f9",
}


class AllContributorsDirective(Directive):  # type: ignore[misc]
    """Directive to include a list of contributors from a JSON file."""

    # Allow one optional argument for the relative path
    required_arguments = 0
    optional_arguments = 1
    has_content = False
    option_spec: ClassVar[dict[str, object]] = {
        "profile": directives.flag,
        "table": directives.flag,
        "avatar": directives.flag,
        "emoji": directives.flag,
    }

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

        # Check if table option is enabled
        show_table = "table" in self.options

        if show_table:
            return [self._create_table(all_contributors)]
        return [self._create_bullet_list(all_contributors)]

    def _create_bullet_list(
        self, all_contributors: dict[str, list[dict[str, str]]]
    ) -> nodes.Node:
        """Create a bullet list node from contributors data."""
        # Create a bullet list node
        list_node = nodes.bullet_list()

        # Check if profile option is enabled
        show_profile = "profile" in self.options
        show_avatar = "avatar" in self.options
        # Check if emoji option is enabled
        use_emoji = "emoji" in self.options

        for contributor in all_contributors.get("contributors", []):
            name = contributor.get("name", "Unknown Contributor")
            contribution_types = list(contributor.get("contributions", []))

            # Format contributions with optional emoji
            if use_emoji:
                contributions_list: list[str] = [
                    f"{EMOJI_MAP.get(contrib, '')} {contrib}".strip()
                    for contrib in contribution_types
                ]
            else:
                contributions_list = list(contribution_types)
            contributions = ", ".join(contributions_list)

            # Create a list item node
            list_item_node = nodes.list_item()
            paragraph_node = nodes.paragraph()

            # Add avatar image if the avatar option is enabled
            if show_avatar and "avatar_url" in contributor:
                image_node = nodes.image(uri=contributor["avatar_url"])
                image_node["alt"] = f"{name} avatar"
                image_node["width"] = "50px"
                image_node["height"] = "50px"
                paragraph_node += image_node
                paragraph_node += nodes.Text(" ")

            if show_profile and "profile" in contributor:
                # Create a reference node for the profile link
                reference_node = nodes.reference(
                    "", name, refuri=contributor["profile"]
                )
                paragraph_node += reference_node
                paragraph_node += nodes.Text(f" for {contributions}")
            else:
                # No profile link, just text
                paragraph_node += nodes.Text(f"{name} for {contributions}")

            # Add the paragraph to the list item
            list_item_node += paragraph_node
            list_node += list_item_node

        return list_node

    def _create_table(
        self, all_contributors: dict[str, list[dict[str, str]]]
    ) -> nodes.Node:
        """Create a table node from contributors data."""
        # Check if profile option is enabled
        show_profile = "profile" in self.options

        # Create table structure
        table = nodes.table()
        tgroup = nodes.tgroup(cols=2)
        table += tgroup

        # Define column widths
        tgroup += nodes.colspec(colwidth=1)
        tgroup += nodes.colspec(colwidth=1)

        # Create table head
        thead = nodes.thead()
        tgroup += thead

        # Header row
        row = nodes.row()
        entry = nodes.entry()
        entry += nodes.paragraph(text="Name")
        row += entry

        entry = nodes.entry()
        entry += nodes.paragraph(text="Contributions")
        row += entry

        thead += row

        # Create table body
        tbody = nodes.tbody()
        tgroup += tbody

        # Add contributor rows
        for contributor in all_contributors.get("contributors", []):
            name = contributor.get("name", "Unknown Contributor")
            contributions = ", ".join(contributor.get("contributions", []))

            row = nodes.row()

            # Name cell
            entry = nodes.entry()
            paragraph_node = nodes.paragraph()

            if show_profile and "profile" in contributor:
                reference_node = nodes.reference(
                    "", name, refuri=contributor["profile"]
                )
                paragraph_node += reference_node
            else:
                paragraph_node += nodes.Text(name)

            entry += paragraph_node
            row += entry

            # Contributions cell
            entry = nodes.entry()
            entry += nodes.paragraph(text=contributions)
            row += entry

            tbody += row

        return table
