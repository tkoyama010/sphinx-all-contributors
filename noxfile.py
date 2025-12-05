#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["nox"]
# ///
"""Automation tasks for Nox."""

import nox

nox.needs_version = "2025.10.14"
nox.options.default_venv_backend = "uv|virtualenv"


if __name__ == "__main__":
    nox.main()
