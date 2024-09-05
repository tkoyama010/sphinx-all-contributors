from docutils import nodes
from docutils.parsers.rst import Directive
import json
import os

class AllContributorsDirective(Directive):
    # Allow one optional argument for the relative path
    required_arguments = 0
    optional_arguments = 1
    has_content = False

    def run(self):
        env = self.state.document.settings.env
        srcdir = env.srcdir

        # Get the path from the argument or default to .all-contributorsrc
        relative_path = self.arguments[0] if self.arguments else '.all-contributorsrc'
        contributors_file = os.path.join(srcdir, relative_path)

        if not os.path.exists(contributors_file):
            return [nodes.error(None, nodes.paragraph(text=f"Error: {relative_path} file not found."))]

        with open(contributors_file, 'r', encoding='utf-8') as f:
            all_contributors = json.load(f)

        contributors_list = []

        for contributor in all_contributors.get('contributors', []):
            name = contributor.get('name', 'Unknown Contributor')
            contributions = ', '.join(contributor.get('contributions', []))
            contributors_list.append(f"- {name} {contributions}")

        # Join the list items with newlines
        content = "\n".join(contributors_list)

        # Create a paragraph node containing the content
        paragraph_node = nodes.paragraph(text=content)
        return [paragraph_node]
