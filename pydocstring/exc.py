"""
pydocstring exceptions
"""


class InvalidFormatterError(Exception):
    """
    Provided name of formatter is not one supported
    """

    pass


class FailedToGenerateDocstringError(Exception):
    """
    Could not generate a docstring for the given code and position
    """

    pass


class FailedToIngestError(Exception):
    """
    Could not ingest the provided source text
    """

    pass