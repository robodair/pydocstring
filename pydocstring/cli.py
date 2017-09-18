"""
pydocstring CLI provides entrypoints for CLI commands

Currently only the ``pydocstring`` command is supported

.. code::

    usage: pydocstring [-h] string [position]

    positional arguments:
    string      The Python document to process
    position    Position of the cursor in the document, defaults to the end

    optional arguments:
    -h, --help  show this help message and exit

"""
from __future__ import print_function
import argparse
import pydocstring


def main():
    """
    CLI entrypoint
    """
    parser = argparse.ArgumentParser("pydocstring")
    parser.add_argument("string", help="The Python document to process")
    parser.add_argument("position", nargs="?", type=int,
                        help="Position of the cursor in the document, defaults to the end")
    args = parser.parse_args()

    position = args.position if args.position else len(args.string)

    output = pydocstring.generate_docstring(args.string, position=position)
    print('"""\n' + output + '"""\n')
