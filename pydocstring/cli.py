"""
pydocstring CLI provides entrypoints for CLI commands

Currently only the ``pydocstring`` command is supported

To use pydocstring from the command line you call ``pydocstring`` with the source, and optionally
the position of the cursor within that source.

You may also want to provide

.. code-block:: text

    usage: pydocstring [-h] [-f {google,numpy,reST}] [--version] string [position]

    positional arguments:
    string                The Python document to process
    position              Position of the cursor in the document, defaults to the end

    optional arguments:
    -h, --help            show this help message and exit
    -f {google,numpy,reST}, --formatter {google,numpy,reST}
                            docstring formatter to use
    --version             show program's version number and exit

"""
from __future__ import print_function
import sys
import argparse
import pydocstring


def main():
    """
    CLI entrypoint
    """
    parser = argparse.ArgumentParser(prog="pydocstring")
    parser.add_argument("source",
                        type=str,
                        help="The Python document to process")
    parser.add_argument("position",
                        nargs="?",
                        type=int,
                        help="Position of the cursor in the document, defaults to the end")
    parser.add_argument("-f", "--formatter",
                        choices=pydocstring.formatters.__all__,
                        default=pydocstring.formatters.__all__[0],
                        type=str,
                        help="docstring formatter to use")
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {0}'.format(pydocstring.__version__))
    args = parser.parse_args()

    position = args.position if args.position else len(args.source)

    output = pydocstring.generate_docstring(args.source,
                                            position=position,
                                            formatter=args.formatter)
    if output != None:
        print('"""\n' + output + '"""\n')
    else:
        sys.stderr.write("Could not generate a docstring for the given source\n")
        sys.exit(1)
