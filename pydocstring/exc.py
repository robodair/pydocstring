"""
pydocstring exceptions
"""

class InvalidFormatter(Exception):
    """
    Provided name of formatter is not one supported
    """
    pass

class UnknownDeclaration(Exception):
    """
    Could not determine if the declaration was a module, class or method
    """
    pass
