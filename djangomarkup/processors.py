class ProcessorConfigurationError(Exception):
    """ Raised when processor is badly configured (module not found, bad dependencies, ...) """

class ProcessorError(Exception):
    """ Raised when any error occurs during processor transformation (usually means a bug withing processing engine) """

def markdown(src, **kwargs):
    try:
        from markdown2 import markdown as m
    except ImportError:
        from markdown import markdown as m

    return m(src) #, html4tags, tab_width, safe_mode, extras, link_patterns, use_file_vars)

def czechtile(src, **kwargs):
    pass
