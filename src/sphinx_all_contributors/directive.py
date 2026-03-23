"""Directive to include a list of contributors from a JSON file."""

import json
from pathlib import Path
from typing import ClassVar

from docutils import nodes  # type: ignore[import-untyped]
from docutils.parsers.rst import Directive, directives  # type: ignore[import-untyped]

# Standard emoji mapping for all-contributors contribution types
EMOJI_MAP = {
    "audio": "🔊",
    "a11y": "♿️",
    "bug": "🐛",
    "blog": "📝",
    "business": "💼",
    "code": "💻",
    "content": "🖋",
    "data": "🔣",
    "doc": "📖",
    "design": "🎨",
    "example": "💡",
    "eventOrganizing": "📋",
    "financial": "💵",
    "fundingFinding": "🔍",
    "ideas": "🤔",
    "infra": "🚇",
    "maintenance": "🚧",
    "mentoring": "🧑‍🏫",
    "platform": "📦",
    "plugin": "🔌",
    "projectManagement": "📆",
    "question": "💬",
    "research": "🔬",
    "review": "👀",
    "security": "🛡️",
    "tool": "🔧",
    "translation": "🌍",
    "test": "⚠️",
    "tutorial": "✅",
    "talk": "📢",
    "userTesting": "📓",
    "video": "📹",
}


class AllContributorsDirective(Directive):  # type: ignore[misc]
    """Directive to include a list of contributors from a JSON file."""

    # Allow one optional argument for the relative path
    required_arguments = 0
    optional_arguments = 1
    has_content = False
    option_spec: ClassVar[dict[str, object]] = {
        "profile": directives.flag,
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

        # Create a bullet list node
        list_node = nodes.bullet_list()

        # Check if profile option is enabled
        show_profile = "profile" in self.options
        # Check if emoji option is enabled
        use_emoji = "emoji" in self.options

        for contributor in all_contributors.get("contributors", []):
            name = contributor.get("name", "Unknown Contributor")
            contribution_types = contributor.get("contributions", [])

            # Format contributions with optional emoji
            if use_emoji:
                contributions_list = [
                    f"{EMOJI_MAP.get(contrib, '')} {contrib}".strip()
                    for contrib in contribution_types
                ]
            else:
                contributions_list = contribution_types
            contributions = ", ".join(contributions_list)

            # Create a list item node
            list_item_node = nodes.list_item()
            paragraph_node = nodes.paragraph()

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

        return [list_node]
