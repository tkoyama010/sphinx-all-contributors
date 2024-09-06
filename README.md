# sphinx-all-contributors

[![All Contributors](https://img.shields.io/github/all-contributors/tkoyama010/sphinx-all-contributors?color=ee8449)](https://sphinx-all-contributors.readthedocs.io/en/latest/reference/about.html#contributors)
[![Documentation Status](https://readthedocs.org/projects/sphinx-all-contributors/badge/?version=latest)](https://sphinx-all-contributors.readthedocs.io/en/latest/?badge=latest)

`sphinx-all-contributors` is a Sphinx extension that allows you to easily display a list of contributors from a `.all-contributorsrc` file in your Sphinx documentation. The list is generated in a simple, readable format like:

```
- Contributor Name 1 - ideas, docs
- Contributor Name 2 - code
```

## Features

- Automatically reads the list of contributors from a `.all-contributorsrc` file.
- Customizable relative path to the `.all-contributorsrc` file.
- Outputs a list of contributors in a clean, human-readable format.

## Installation

1. Clone or download this repository.
1. Install the package by running:

```bash
pip install .
```

## Usage

Add `sphinx-all-contributors` to the `extensions` list in your `conf.py`:

```python
# conf.py
extensions = [
    "sphinx_all_contributors",
    # other extensions
]
```

Create a `.all-contributorsrc` file in your documentation source directory (or another location). You can create this file manually following the [all-contributors](https://allcontributors.org/docs/en/format/specification) format, or you can use the [all-contributors bot](https://allcontributors.org/docs/en/bot/overview) to automate this process and ensure that your contributor data is accurate and up-to-date. An example `.all-contributorsrc` file looks like this:

```json
{
  "contributors": [
    {
      "name": "Contributor Name 1",
      "contributions": ["ideas", "docs"]
    },
    {
      "name": "Contributor Name 2",
      "contributions": ["code"]
    }
  ]
}
```

In your `.rst` file, use the `all-contributors` directive to display the list of contributors. You can specify the relative path to the `.all-contributorsrc` file or omit it to use the default path (`.all-contributorsrc` in the source directory).

Example 1: Using the default `.all-contributorsrc` path:

```rst
.. all-contributors::
```

Example 2: Specifying a relative path to the `.all-contributorsrc` file:

```rst
.. all-contributors:: config/.all-contributorsrc
```

Build your documentation:

```bash
make html
```

The generated HTML (or other formats) will contain a list of contributors in the format:

```
- Contributor Name 1 - ideas, docs
- Contributor Name 2 - code
```
