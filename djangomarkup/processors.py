class ProcessorConfigurationError(Exception):
    """ Raised when processor is badly configured (module not found, bad dependencies, ...) """

class ProcessorError(Exception):
    """ Raised when any error occurs during processor transformation (usually means a bug withing processing engine) """

def markdown(src, **kwargs):
    try:
        from markdown2 import markdown as m
    except ImportError:
        try:
            from markdown import markdown as m
        except ImportError:
            raise ProcessorConfigurationError(u"markdown nor markdown2 found")

    return m(src, extras=["code-friendly"]) #, html4tags, tab_width, safe_mode, extras, link_patterns, use_file_vars)

def czechtile(src, **kwargs):
    try:
        from czechtile import (
            parse, register_map,
            expand, expander_map
        )
    except ImportError:
        raise ProcessorConfigurationError(u"czechtile not found")
    tree = parse(src, register_map)
    tree.wrap_document = False
    try:
        return expand(tree, 'xhtml11', expander_map)
    except Exception, err:
        raise ProcessorError(err)

def rest(src, **kwargs):
    try:
        from docutils.core import publish_parts
    except ImportError:
        raise ProcessorConfigurationError(u"docutils not found")

    parts = publish_parts(src, writer_name='html', **kwargs)
    return parts['fragment']

