from .directive import AllContributorsDirective


def setup(app):
    app.add_directive("all-contributors", AllContributorsDirective)
    return {
        "version": "0.0.dev0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
