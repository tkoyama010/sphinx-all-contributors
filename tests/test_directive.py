"""Test for the sphinx-all-contributors directive."""

import json
import shutil
from pathlib import Path
from typing import Any

import pytest
from docutils import nodes
from docutils.frontend import OptionParser
from docutils.parsers.rst import Parser
from docutils.statemachine import State, StateMachine, StringList
from docutils.utils import new_document
from sphinx.application import Sphinx
from sphinx.util import logging

from sphinx_all_contributors.directive import AllContributorsDirective


@pytest.fixture
def sphinx_app(tmpdir: Path) -> Sphinx:
    """Create a Sphinx application for testing."""
    # Copy conf.py to the tmpdir
    conf_path = Path(__file__).parent / "conf.py"
    shutil.copy(conf_path, tmpdir / "conf.py")

    app = Sphinx(
        tmpdir,
        tmpdir,
        tmpdir / "_build",
        tmpdir / "_build" / ".doctrees",
        buildername="html",
        confoverrides={"extensions": ["sphinx_all_contributors"]},
    )
    app.warning = logging.getLogger("sphinx").warning
    return app


class MockState(State):
    """Mock State class for testing."""

    def __init__(self, document: Any) -> None:  # noqa: ANN401
        """Initialize the MockState."""
        self.document = document
        self.reporter = document.reporter


class MockStateMachine(StateMachine):
    """Mock StateMachine class for testing."""

    def __init__(self, document: Any) -> None:  # noqa: ANN401
        """Initialize the MockStateMachine."""
        self.document = document
        self.reporter = document.reporter
        self.current_state = MockState(document)


@pytest.mark.parametrize(
    ("options", "has_profiles", "should_have_links"),
    [
        pytest.param({}, False, False, id="no_profile_option_no_data"),
        pytest.param({}, True, False, id="no_profile_option_with_data"),
        pytest.param({"profile": None}, True, True, id="profile_option_enabled"),
    ],
)
def test_all_contributors_directive(
    sphinx_app: Sphinx,
    tmpdir: Path,
    options: dict[str, Any],
    *,
    has_profiles: bool,
    should_have_links: bool,
) -> None:
    """Test the all-contributors directive with different options."""
    # Create contributor data with optional profile information
    contributors_data = {
        "contributors": [
            {
                "name": "John Doe",
                "contributions": ["code", "doc"],
                "avatar_url": "https://avatars.githubusercontent.com/u/1?v=4",
                **({"profile": "https://github.com/johndoe"} if has_profiles else {}),
            },
            {
                "name": "Jane Smith",
                "contributions": ["design", "test"],
                "avatar_url": "https://avatars.githubusercontent.com/u/2?v=4",
                **({"profile": "https://github.com/janesmith"} if has_profiles else {}),
            },
        ]
    }
    contributors_file = tmpdir / ".all-contributorsrc"
    with Path(contributors_file).open("w") as f:
        json.dump(contributors_data, f)

    # Create a minimal Sphinx environment
    settings = OptionParser(components=[Parser]).get_default_values()
    document = new_document("<test>", settings=settings)
    document.settings.env = sphinx_app.env
    state_machine = MockStateMachine(document)

    # Create a directive instance
    directive = AllContributorsDirective(
        name="all-contributors",
        arguments=[str(contributors_file)],
        options=options,
        content=StringList([""], source="test"),
        lineno=0,
        content_offset=0,
        block_text="",
        state=MockState(document),
        state_machine=state_machine,
    )

    # Run the directive
    result = directive.run()

    # Assert that the result is a list containing a bullet_list node
    assert isinstance(result, list), "Result is not a list"  # noqa: S101
    assert len(result) == 1, "Result list does not have length 1"  # noqa: S101
    assert isinstance(result[0], nodes.bullet_list), (  # noqa: S101
        "First element is not a bullet list"
    )

    # Assert that the bullet_list contains the expected list items
    list_items = result[0].children
    assert len(list_items) == 2, "List items does not have length 2"  # noqa: S101, PLR2004

    # Check if links are present based on should_have_links
    first_para = list_items[0].children[0]
    if should_have_links:
        assert isinstance(first_para.children[0], nodes.reference), (  # noqa: S101
            "Should contain reference node when profile option is enabled"
        )
        assert first_para.children[0]["refuri"] == "https://github.com/johndoe", (  # noqa: S101
            "Profile link should be correct"
        )
    else:
        assert isinstance(first_para.children[0], nodes.Text), (  # noqa: S101
            "Should contain text node when profile option is disabled"
        )

    # Assert text content is correct
    assert list_items[0].astext() == "John Doe for code, doc", (  # noqa: S101
        "First list item text is incorrect"
    )
    assert list_items[1].astext() == "Jane Smith for design, test", (  # noqa: S101
        "Second list item text is incorrect"
    )


@pytest.mark.parametrize(
    ("options", "has_profiles", "should_have_links"),
    [
        pytest.param({}, False, False, id="table_no_profile_option_no_data"),
        pytest.param({}, True, False, id="table_no_profile_option_with_data"),
        pytest.param({"profile": None}, True, True, id="table_profile_option_enabled"),
    ],
)
def test_all_contributors_directive_table(
    sphinx_app: Sphinx,
    tmpdir: Path,
    options: dict[str, Any],
    *,
    has_profiles: bool,
    should_have_links: bool,
) -> None:
    """Test the all-contributors directive with table option."""
    # Create contributor data with optional profile information
    contributors_data = {
        "contributors": [
            {
                "name": "John Doe",
                "contributions": ["code", "doc"],
                **({"profile": "https://github.com/johndoe"} if has_profiles else {}),
            },
            {
                "name": "Jane Smith",
                "contributions": ["design", "test"],
                **({"profile": "https://github.com/janesmith"} if has_profiles else {}),
            },
        ]
    }
    contributors_file = tmpdir / ".all-contributorsrc"
    with Path(contributors_file).open("w") as f:
        json.dump(contributors_data, f)

    # Create a minimal Sphinx environment
    settings = OptionParser(components=[Parser]).get_default_values()
    document = new_document("<test>", settings=settings)
    document.settings.env = sphinx_app.env
    state_machine = MockStateMachine(document)

    # Add table option
    table_options = {**options, "table": None}

    # Create a directive instance
    directive = AllContributorsDirective(
        name="all-contributors",
        arguments=[str(contributors_file)],
        options=table_options,
        content=StringList([""], source="test"),
        lineno=0,
        content_offset=0,
        block_text="",
        state=MockState(document),
        state_machine=state_machine,
    )

    # Run the directive
    result = directive.run()

    # Assert that the result is a list containing a table node
    assert isinstance(result, list), "Result is not a list"  # noqa: S101
    assert len(result) == 1, "Result list does not have length 1"  # noqa: S101
    assert isinstance(result[0], nodes.table), (  # noqa: S101
        "First element is not a table"
    )

    # Get the table structure
    table = result[0]
    tgroup = table.children[0]
    assert isinstance(tgroup, nodes.tgroup), "No tgroup in table"  # noqa: S101

    # Check table has thead and tbody
    thead = None
    tbody = None
    for child in tgroup.children:
        if isinstance(child, nodes.thead):
            thead = child
        elif isinstance(child, nodes.tbody):
            tbody = child

    assert thead is not None, "No thead in table"  # noqa: S101
    assert tbody is not None, "No tbody in table"  # noqa: S101

    # Check header row
    header_row = thead.children[0]
    assert isinstance(header_row, nodes.row), "No header row"  # noqa: S101
    header_cells = header_row.children
    assert len(header_cells) == 2, "Header should have 2 cells"  # noqa: S101, PLR2004
    assert header_cells[0].astext() == "Name", "First header should be 'Name'"  # noqa: S101
    assert header_cells[1].astext() == "Contributions", (  # noqa: S101
        "Second header should be 'Contributions'"
    )

    # Check body rows
    body_rows = tbody.children
    assert len(body_rows) == 2, "Table body should have 2 rows"  # noqa: S101, PLR2004

    # Check first row
    first_row = body_rows[0]
    first_row_cells = first_row.children
    assert len(first_row_cells) == 2, "First row should have 2 cells"  # noqa: S101, PLR2004

    # Check if links are present based on should_have_links
    first_cell_para = first_row_cells[0].children[0]
    if should_have_links:
        assert isinstance(first_cell_para.children[0], nodes.reference), (  # noqa: S101
            "Should contain reference node when profile option is enabled"
        )
        assert first_cell_para.children[0]["refuri"] == "https://github.com/johndoe", (  # noqa: S101
            "Profile link should be correct"
        )
    else:
        assert isinstance(first_cell_para.children[0], nodes.Text), (  # noqa: S101
            "Should contain text node when profile option is disabled"
        )

    # Assert text content is correct
    assert first_row_cells[0].astext() == "John Doe", (  # noqa: S101
        "First row name is incorrect"
    )
    assert first_row_cells[1].astext() == "code, doc", (  # noqa: S101
        "First row contributions are incorrect"
    )

    # Check second row
    second_row = body_rows[1]
    second_row_cells = second_row.children
    assert second_row_cells[0].astext() == "Jane Smith", (  # noqa: S101
        "Second row name is incorrect"
    )
    assert second_row_cells[1].astext() == "design, test", (  # noqa: S101
        "Second row contributions are incorrect"
    )


@pytest.mark.parametrize(
    ("options", "should_have_avatars"),
    [
        pytest.param({}, False, id="no_avatar_option"),
        pytest.param({"avatar": None}, True, id="avatar_option_enabled"),
    ],
)
def test_all_contributors_directive_with_avatar(
    sphinx_app: Sphinx,
    tmpdir: Path,
    options: dict[str, Any],
    *,
    should_have_avatars: bool,
) -> None:
    """Test the all-contributors directive with avatar option."""
    # Create contributor data with avatar URLs
    contributors_data = {
        "contributors": [
            {
                "name": "John Doe",
                "contributions": ["code", "doc"],
                "avatar_url": "https://avatars.githubusercontent.com/u/1?v=4",
            },
            {
                "name": "Jane Smith",
                "contributions": ["design", "test"],
                "avatar_url": "https://avatars.githubusercontent.com/u/2?v=4",
            },
        ]
    }
    contributors_file = tmpdir / ".all-contributorsrc"
    with Path(contributors_file).open("w") as f:
        json.dump(contributors_data, f)

    # Create a minimal Sphinx environment
    settings = OptionParser(components=[Parser]).get_default_values()
    document = new_document("<test>", settings=settings)
    document.settings.env = sphinx_app.env
    state_machine = MockStateMachine(document)

    # Create a directive instance
    directive = AllContributorsDirective(
        name="all-contributors",
        arguments=[str(contributors_file)],
        options=options,
        content=StringList([""], source="test"),
        lineno=0,
        content_offset=0,
        block_text="",
        state=MockState(document),
        state_machine=state_machine,
    )

    # Run the directive
    result = directive.run()

    # Assert that the result is a list containing a bullet_list node
    assert isinstance(result, list), "Result is not a list"  # noqa: S101
    assert len(result) == 1, "Result list does not have length 1"  # noqa: S101
    assert isinstance(result[0], nodes.bullet_list), (  # noqa: S101
        "First element is not a bullet list"
    )

    # Assert that the bullet_list contains the expected list items
    list_items = result[0].children
    assert len(list_items) == 2, "List items does not have length 2"  # noqa: S101, PLR2004

    # Check if avatars are present based on should_have_avatars
    first_para = list_items[0].children[0]
    if should_have_avatars:
        # First child should be an image node when avatar option is enabled
        assert isinstance(first_para.children[0], nodes.image), (  # noqa: S101
            "Should contain image node when avatar option is enabled"
        )
        assert (  # noqa: S101
            first_para.children[0]["uri"]
            == "https://avatars.githubusercontent.com/u/1?v=4"
        ), "Avatar URL should be correct"
        assert first_para.children[0]["alt"] == "John Doe avatar", (  # noqa: S101
            "Avatar alt text should be correct"
        )
        assert first_para.children[0]["width"] == "50px", "Avatar width should be 50px"  # noqa: S101
        assert first_para.children[0]["height"] == "50px", (  # noqa: S101
            "Avatar height should be 50px"
        )
        # Second child should be a space text node
        assert isinstance(first_para.children[1], nodes.Text), (  # noqa: S101
            "Should contain space text node after avatar"
        )
        # When avatar is present, astext includes the alt text
        assert list_items[0].astext() == "John Doe avatar John Doe for code, doc", (  # noqa: S101
            "First list item text is incorrect with avatar"
        )
        expected = "Jane Smith avatar Jane Smith for design, test"
        assert list_items[1].astext() == expected, (  # noqa: S101
            "Second list item text is incorrect with avatar"
        )
    else:
        # First child should be text node when avatar option is disabled
        assert isinstance(first_para.children[0], nodes.Text), (  # noqa: S101
            "Should contain text node when avatar option is disabled"
        )
        # Without avatar, text content is normal
        assert list_items[0].astext() == "John Doe for code, doc", (  # noqa: S101
            "First list item text is incorrect"
        )
        assert list_items[1].astext() == "Jane Smith for design, test", (  # noqa: S101
            "Second list item text is incorrect"
        )
